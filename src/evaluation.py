import numpy as np
import pandas as pd
import os
import sys
import json

# Asegurar que la raíz del proyecto está en el PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import seaborn as sns
from src.svd_model import MatrixFactorizationSVD
from src.rules_engine import LogicInferenceModel
from src.maut_model import MAUTModel
from src.content_model import ContentBasedModel
from src.hybrid_recommender import HybridRecommender

def train_test_split_ratings(ratings_df, test_ratio=0.2, random_state=42):
    np.random.seed(random_state)
    mask = np.random.rand(len(ratings_df)) < (1 - test_ratio)
    train_df = ratings_df[mask].copy()
    test_df = ratings_df[~mask].copy()
    return train_df, test_df

def evaluate_svd_rmse(train_df, test_df, n_factors=10, lr=0.005, reg=0.02, epochs=35):
    """
    Entrena el modelo SVD y calcula el RMSE en el conjunto de prueba.
    """
    model = MatrixFactorizationSVD(n_factors=n_factors, lr=lr, reg=reg, epochs=epochs)
    model.fit(train_df)
    
    squared_errors = []
    for _, row in test_df.iterrows():
        user_id = row["user_id"]
        laptop_id = row["laptop_id"]
        actual_rating = row["rating"]
        
        pred_rating = model.predict(user_id, laptop_id)
        squared_errors.append((actual_rating - pred_rating) ** 2)
        
    rmse = np.sqrt(np.mean(squared_errors))
    return rmse, model

def evaluate_metrics(data_dir="data", output_plot_dir="app/static/plots"):
    os.makedirs(output_plot_dir, exist_ok=True)
    
    laptops_df = pd.read_csv(os.path.join(data_dir, "laptops.csv"))
    ratings_df = pd.read_csv(os.path.join(data_dir, "ratings.csv"))
    
    # 1. EVALUAR RMSE DE SVD
    train_df, test_df = train_test_split_ratings(ratings_df, test_ratio=0.2)
    rmse, trained_svd = evaluate_svd_rmse(train_df, test_df)
    print(f"SVD Test RMSE: {rmse:.4f}")
    
    # 2. COMPARAR CSR (Constraint Satisfaction Rate)
    # Simulamos múltiples consultas de usuarios con requerimientos estrictos y evaluamos qué
    # porcentaje de las Top-K recomendaciones cumplen con los filtros de negocio.
    np.random.seed(42)
    test_cases = [
        {"usage": "Deep Learning", "budget": 1500.0, "weights": {"price": 0.2, "perf": 0.6, "portability": 0.1, "screen": 0.1}},
        {"usage": "Arquitectura / Render 3D", "budget": 2000.0, "weights": {"price": 0.1, "perf": 0.7, "portability": 0.1, "screen": 0.1}},
        {"usage": "Desarrollo de Software", "budget": 1200.0, "weights": {"price": 0.3, "perf": 0.4, "portability": 0.2, "screen": 0.1}},
        {"usage": "Uso de Oficina / Estudiante", "budget": 800.0, "weights": {"price": 0.5, "perf": 0.2, "portability": 0.2, "screen": 0.1}},
        # Más casos
        {"usage": "Deep Learning", "budget": 2500.0, "weights": {"price": 0.1, "perf": 0.5, "portability": 0.2, "screen": 0.2}},
        {"usage": "Arquitectura / Render 3D", "budget": 1300.0, "weights": {"price": 0.3, "perf": 0.5, "portability": 0.1, "screen": 0.1}},
    ]
    
    recommender = HybridRecommender(data_dir)
    recommender.load_data_and_train()
    
    csr_hybrid = []
    csr_svd_pure = []
    csr_content_pure = []
    
    # Modelos Baselines puros sin filtrado de reglas duras
    # SVD Puro: Recomienda laptops basado únicamente en la calificación predicha por SVD.
    # Content Puro: Recomienda basado en similitud coseno únicamente.
    
    rules_engine = LogicInferenceModel(os.path.join(data_dir, "knowledge_rules.json"))
    
    K = 10
    for case in test_cases:
        usage = case["usage"]
        budget = case["budget"]
        weights = case["weights"]
        
        # Máscara binaria real para validar
        mask_val = rules_engine.get_binary_mask(laptops_df, usage, budget)
        laptops_temp = laptops_df.copy()
        laptops_temp["valid"] = mask_val
        
        # 1. Híbrido
        top_hybrid, _ = recommender.get_recommendations("U001", usage, budget, weights, top_k=K, is_cold_start=True)
        # CSR
        satisfied_hybrid = laptops_temp[laptops_temp["id"].isin(top_hybrid["id"])]["valid"].sum()
        csr_hybrid.append(satisfied_hybrid / K)
        
        # 2. SVD Puro (predice ratings y ordena)
        svd_scores = []
        for _, row in laptops_df.iterrows():
            svd_scores.append(trained_svd.predict("U001", row["id"]))
        laptops_temp["svd_score"] = svd_scores
        top_svd = laptops_temp.sort_values(by="svd_score", ascending=False).head(K)
        satisfied_svd = top_svd["valid"].sum()
        csr_svd_pure.append(satisfied_svd / K)
        
        # 3. Content Puro (similitud coseno y ordena)
        content_model = ContentBasedModel()
        content_model.fit(laptops_df)
        cosine_sim = content_model.compute_similarity(laptops_df, usage, budget, weights)
        laptops_temp["cosine_sim"] = cosine_sim
        top_content = laptops_temp.sort_values(by="cosine_sim", ascending=False).head(K)
        satisfied_content = top_content["valid"].sum()
        csr_content_pure.append(satisfied_content / K)
        
    avg_csr_hybrid = np.mean(csr_hybrid)
    avg_csr_svd = np.mean(csr_svd_pure)
    avg_csr_content = np.mean(csr_content_pure)
    
    print(f"CSR@10 Hybrid: {avg_csr_hybrid*100:.1f}%")
    print(f"CSR@10 SVD Pure: {avg_csr_svd*100:.1f}%")
    print(f"CSR@10 Content Pure: {avg_csr_content*100:.1f}%")
    
    # 3. EVALUACIÓN DE PRECISION@K Y RECALL@K EN EL SPLIT DE PRUEBA
    # Definimos relevancia histórica: laptop calificada >= 4 por el usuario en el conjunto test_df
    # Evaluamos solo para usuarios con al menos 3 calificaciones relevantes en test_df.
    precisions = []
    recalls = []
    
    # Baselines
    precisions_svd = []
    recalls_svd = []
    
    test_users = test_df[test_df["rating"] >= 4]["user_id"].unique()
    
    for u_id in test_users:
        # Laptops relevantes del usuario en test set
        u_test = test_df[test_df["user_id"] == u_id]
        u_relevant_laptops = set(u_test[u_test["rating"] >= 4]["laptop_id"].values)
        
        if len(u_relevant_laptops) < 2:
            continue
            
        # Generar Top K recomendaciones (Híbrido - Usuario Recurrente)
        # Usamos pesos estándar equilibrados
        std_weights = {"price": 0.25, "perf": 0.25, "portability": 0.25, "screen": 0.25}
        
        # Consultar su uso asignado en el perfil
        # Para simplificar la evaluación, tomamos su uso según el perfil real
        # Si no lo sabemos, usamos oficina/estudiante. En nuestro dataset tenemos user_profiles.json
        profiles_path = os.path.join(data_dir, "user_profiles.json")
        usage_type = "Uso de Oficina / Estudiante"
        if os.path.exists(profiles_path):
            with open(profiles_path, "r") as f:
                p_data = json.load(f)
                prof = p_data.get(u_id, 1)
                if prof == 0:
                    usage_type = "Arquitectura / Render 3D"
                elif prof == 2:
                    usage_type = "Deep Learning"
        
        # 1. Recomendaciones Híbridas
        top_hybrid, _ = recommender.get_recommendations(u_id, usage_type, 3500.0, std_weights, top_k=10, is_cold_start=False)
        rec_ids_hybrid = set(top_hybrid["id"].values)
        
        hits_hybrid = len(rec_ids_hybrid.intersection(u_relevant_laptops))
        precisions.append(hits_hybrid / 10)
        recalls.append(hits_hybrid / len(u_relevant_laptops))
        
        # 2. SVD Puro
        laptops_temp = laptops_df.copy()
        svd_scores = [trained_svd.predict(u_id, row["id"]) for _, row in laptops_temp.iterrows()]
        laptops_temp["svd_score"] = svd_scores
        top_svd = laptops_temp.sort_values(by="svd_score", ascending=False).head(10)
        rec_ids_svd = set(top_svd["id"].values)
        
        hits_svd = len(rec_ids_svd.intersection(u_relevant_laptops))
        precisions_svd.append(hits_svd / 10)
        recalls_svd.append(hits_svd / len(u_relevant_laptops))
        
    avg_precision_hybrid = np.mean(precisions) if precisions else 0
    avg_recall_hybrid = np.mean(recalls) if recalls else 0
    avg_precision_svd = np.mean(precisions_svd) if precisions_svd else 0
    avg_recall_svd = np.mean(recalls_svd) if recalls_svd else 0
    
    print(f"Hybrid Precision@10: {avg_precision_hybrid:.4f}, Recall@10: {avg_recall_hybrid:.4f}")
    print(f"SVD Pure Precision@10: {avg_precision_svd:.4f}, Recall@10: {avg_recall_svd:.4f}")
    
    # 4. GENERAR GRÁFICOS Y GUARDARLOS
    sns.set_theme(style="darkgrid")
    
    # Gráfico 1: Constraint Satisfaction Rate (CSR)
    plt.figure(figsize=(8, 5))
    models = ['Híbrido (En Cascada)', 'Content-Based Puro', 'SVD Colaborativo Puro']
    csr_values = [avg_csr_hybrid * 100, avg_csr_content * 100, avg_csr_svd * 100]
    
    colors = ['#4e73df', '#1cc88a', '#e74a3b']
    bars = plt.bar(models, csr_values, color=colors, width=0.6)
    
    # Agregar etiquetas de porcentaje arriba de las barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
        
    plt.title('Constraint Satisfaction Rate (CSR@10) comparativo', fontsize=14, pad=15)
    plt.ylabel('% de Laptops en Top-10 que cumplen Reglas de Negocio')
    plt.ylim(0, 110)
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "evaluation_csr.png"), dpi=150)
    plt.close()
    
    # Gráfico 2: Precision@10 & Recall@10
    plt.figure(figsize=(8, 5))
    metrics_label = ['Precision@10', 'Recall@10']
    
    x = np.arange(len(metrics_label))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    rects1 = ax.bar(x - width/2, [avg_precision_hybrid, avg_recall_hybrid], width, label='Híbrido (Propuesto)', color='#4e73df')
    rects2 = ax.bar(x + width/2, [avg_precision_svd, avg_recall_svd], width, label='SVD Puro (Baseline)', color='#e74a3b')
    
    ax.set_ylabel('Score')
    ax.set_title('Precisión y Recall Comparativo (Top-10)', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_label)
    ax.legend()
    # Permitimos que pyplot auto-escale el eje Y para que las barras bajas no desaparezcan
    max_val = max(avg_precision_hybrid, avg_recall_hybrid, avg_precision_svd, avg_recall_svd)
    ax.set_ylim(0, max(max_val * 1.3, 0.1))
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')
                        
    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "evaluation_precision_recall.png"), dpi=150)
    plt.close()
    
    print("Gráficos de evaluación generados y guardados en app/static/plots/")
    
    # Devolver métricas para su uso en la app o scripts
    return {
        "svd_rmse": float(rmse),
        "csr_hybrid": float(avg_csr_hybrid),
        "csr_svd": float(avg_csr_svd),
        "csr_content": float(avg_csr_content),
        "precision_hybrid": float(avg_precision_hybrid),
        "recall_hybrid": float(avg_recall_hybrid),
        "precision_svd": float(avg_precision_svd),
        "recall_svd": float(avg_recall_svd)
    }

if __name__ == "__main__":
    import json
    evaluate_metrics()
