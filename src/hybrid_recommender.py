import pandas as pd
import numpy as np
import os
from src.rules_engine import LogicInferenceModel
from src.maut_model import MAUTModel
from src.svd_model import MatrixFactorizationSVD
from src.content_model import ContentBasedModel

class HybridRecommender:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.laptops_df = None
        self.ratings_df = None
        
        # Instanciar Sub-Modelos
        self.model_rules = LogicInferenceModel(os.path.join(data_dir, "knowledge_rules.json"))
        self.model_maut = MAUTModel()
        self.model_svd = MatrixFactorizationSVD()
        self.model_content = ContentBasedModel()
        
    def load_data_and_train(self):
        """
        Carga los datos del catálogo y de valoraciones, y entrena los modelos.
        """
        laptops_path = os.path.join(self.data_dir, "laptops.csv")
        ratings_path = os.path.join(self.data_dir, "ratings.csv")
        
        if not os.path.exists(laptops_path) or not os.path.exists(ratings_path):
            raise FileNotFoundError("Los archivos de datos laptops.csv o ratings.csv no existen. Ejecuta primero src/data_generator.py.")
            
        self.laptops_df = pd.read_csv(laptops_path)
        self.ratings_df = pd.read_csv(ratings_path)
        
        # Ajustar límites de datos para MAUT y Content-Based
        self.model_maut.fit(self.laptops_df)
        self.model_content.fit(self.laptops_df)
        
        # Entrenar modelo SVD
        self.model_svd.fit(self.ratings_df)
        
    def get_recommendations(self, user_id, usage_type, budget, maut_weights, top_k=10, is_cold_start=None, lifestyle_tags=None):
        """
        Genera recomendaciones híbridas personalizadas en base a 2 niveles.
        - user_id: ID del usuario (e.g. 'U001', o uno nuevo)
        - usage_type: Tipo de uso ('Deep Learning', 'Arquitectura / Render 3D', etc.)
        - budget: Presupuesto máximo (float)
        - maut_weights: dict con pesos cualitativos de MAUT
        - is_cold_start: boolean (fuerza comportamiento de cold start). Si es None, se autodetecta según ratings.
        - lifestyle_tags: lista opcional de etiquetas de estilo de vida ('ultra_portable', 'oled_screen', etc.)
        """
        if self.laptops_df is None or self.ratings_df is None:
            self.load_data_and_train()
            
        n_laptops = len(self.laptops_df)
        
        # 1. NIVEL 1: Filtrado en Cascada (M_rules)
        m_rules = self.model_rules.get_binary_mask(self.laptops_df, usage_type, budget, lifestyle_tags=lifestyle_tags)
        
        # 2. NIVEL 2: Calcular componentes individuales para todo el catálogo
        u_knowledge = self.model_maut.compute_utility(self.laptops_df, maut_weights)
        s_content = self.model_content.compute_similarity(self.laptops_df, usage_type, budget, maut_weights)
        
        # Calcular SVD y detectar si es Cold Start
        is_user_known = user_id in self.model_svd.user_to_idx
        
        if is_cold_start is None:
            # Si el usuario no tiene registros históricos de calificaciones, es Cold Start
            is_cold_start = not is_user_known
            
        svd_scores = np.zeros(n_laptops)
        for idx, row in self.laptops_df.iterrows():
            svd_scores[idx] = self.model_svd.predict_normalized(user_id, row["id"])
            
        # 3. Asignar pesos dinámicamente según Cold Start
        if is_cold_start:
            # Enfocado en reglas de negocio (MAUT) y similaridad de contenido
            alpha = 0.60  # MAUT (Knowledge)
            gamma = 0.30  # Content-based
            beta = 0.10   # SVD
            profile_name = "Cold Start (Usuario Nuevo)"
        else:
            # Enfocado en filtrado colaborativo (SVD)
            alpha = 0.30  # MAUT (Knowledge)
            gamma = 0.20  # Content-based
            beta = 0.50   # SVD
            profile_name = "Usuario Frecuente (Colaborativo)"
            
        # 4. Cálculo del Score Híbrido Ensamblado
        final_scores = m_rules * (alpha * u_knowledge + beta * svd_scores + gamma * s_content)
        
        # 5. Cálculo del Value Score (Relación Calidad / Precio)
        p_min = self.laptops_df["price"].min()
        p_max = self.laptops_df["price"].max()
        p_norm = (self.laptops_df["price"] - p_min) / (p_max - p_min + 1e-6) + 0.1
        val_scores = u_knowledge / p_norm
        
        val_tags = []
        for idx, row in self.laptops_df.iterrows():
            vs = val_scores[idx]
            pr = row["price"]
            if pr > 2200:
                val_tags.append("Gama Premium")
            elif vs > 1.2:
                val_tags.append("Top Calidad/Precio")
            else:
                val_tags.append("Precio Justo")

        # 6. Estructurar Resultados
        results = self.laptops_df.copy()
        results["m_rules"] = m_rules
        results["u_knowledge"] = u_knowledge
        results["s_content"] = s_content
        results["svd_score_norm"] = svd_scores
        results["svd_rating_pred"] = [self.model_svd.predict(user_id, l_id) for l_id in results["id"]]
        results["hybrid_score"] = final_scores
        results["value_score"] = val_scores
        results["value_tag"] = val_tags
        
        # Filtrar laptops con score final > 0 (es decir, m_rules == 1)
        valid_results = results[results["hybrid_score"] > 0].copy()
        
        # Ordenar por puntaje final descendente
        valid_results = valid_results.sort_values(by="hybrid_score", ascending=False)
        
        top_recommendations = valid_results.head(top_k)
        
        # Metadatos del cálculo para retornar
        meta = {
            "user_id": user_id,
            "is_cold_start": is_cold_start,
            "profile_type": profile_name,
            "weights": {
                "alpha_maut": alpha,
                "beta_svd": beta,
                "gamma_content": gamma
            },
            "total_items_catalog": n_laptops,
            "items_passed_rules": int(np.sum(m_rules)),
            "usage_type": usage_type,
            "budget": budget,
            "lifestyle_tags": lifestyle_tags or []
        }
        
        return top_recommendations, meta
