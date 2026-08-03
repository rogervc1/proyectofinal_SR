import numpy as np
import pandas as pd

class ContentBasedModel:
    def __init__(self):
        self.min_max = {}
        
    def fit(self, laptops_df):
        """
        Calcula rangos para normalizar los vectores de atributos.
        """
        self.min_max["price_min"] = laptops_df["price"].min()
        self.min_max["price_max"] = laptops_df["price"].max()
        self.min_max["ram_min"] = laptops_df["ram"].min()
        self.min_max["ram_max"] = laptops_df["ram"].max()
        self.min_max["cores_min"] = laptops_df["cpu_cores"].min()
        self.min_max["cores_max"] = laptops_df["cpu_cores"].max()
        self.min_max["vram_min"] = laptops_df["gpu_vram"].min()
        self.min_max["vram_max"] = laptops_df["gpu_vram"].max()
        self.min_max["weight_min"] = laptops_df["weight"].min()
        self.min_max["weight_max"] = laptops_df["weight"].max()
        self.min_max["screen_min"] = laptops_df["screen_size"].min()
        self.min_max["screen_max"] = laptops_df["screen_size"].max()
        
    def _norm(self, val, min_val, max_val, invert=False):
        if max_val == min_val:
            return 1.0 if not invert else 0.0
        n = (val - min_val) / (max_val - min_val)
        return 1.0 - n if invert else n

    def build_laptop_vectors(self, laptops_df):
        """
        Construye una matriz de vectores v_i para todas las laptops.
        v_i = [price_norm_inv, ram_norm, cores_norm, vram_norm, dedicated_gpu, cuda_support, weight_norm_inv, screen_norm]
        """
        vectors = []
        for _, row in laptops_df.iterrows():
            vec = [
                self._norm(row["price"], self.min_max["price_min"], self.min_max["price_max"], invert=True),
                self._norm(row["ram"], self.min_max["ram_min"], self.min_max["ram_max"]),
                self._norm(row["cpu_cores"], self.min_max["cores_min"], self.min_max["cores_max"]),
                self._norm(row["gpu_vram"], self.min_max["vram_min"], self.min_max["vram_max"]),
                1.0 if row["dedicated_gpu"] else 0.0,
                1.0 if row["cuda_support"] else 0.0,
                self._norm(row["weight"], self.min_max["weight_min"], self.min_max["weight_max"], invert=True),
                self._norm(row["screen_size"], self.min_max["screen_min"], self.min_max["screen_max"])
            ]
            vectors.append(vec)
        return np.array(vectors)

    def build_user_vector(self, usage_type, budget, maut_weights):
        """
        Construye el vector ideal de usuario v_u basado en su uso, presupuesto y preferencias cualitativas.
        maut_weights: dict con pesos de 'price', 'perf', 'portability', 'screen'
        """
        # Inicializar vector ideal v_u
        # v_u = [price, ram, cores, vram, dedicated_gpu, cuda, weight, screen]
        
        # 1. Componente de Precio (v_u[0])
        # Si el presupuesto es bajo, el usuario es muy sensible al precio (quiere maximizar el precio invertido = menor precio real)
        if budget is not None and budget > 0:
            # Mapear presupuesto al rango normalizado inverso
            price_target = self._norm(budget, self.min_max["price_min"], self.min_max["price_max"], invert=True)
        else:
            price_target = 0.5  # Neutral
            
        # 2. Componentes de Hardware según el caso de uso
        ram_target = 0.2
        cores_target = 0.2
        vram_target = 0.0
        dedicated_target = 0.0
        cuda_target = 0.0
        
        if usage_type == "Deep Learning":
            ram_target = 0.8  # Prefiere 32GB+
            cores_target = 0.8
            vram_target = 0.8  # Prefiere 8GB+ VRAM
            dedicated_target = 1.0
            cuda_target = 1.0
        elif usage_type == "Arquitectura / Render 3D":
            ram_target = 0.6
            cores_target = 1.0  # Máximo de núcleos
            vram_target = 0.6
            dedicated_target = 1.0
            cuda_target = 0.5
        elif usage_type == "Desarrollo de Software":
            ram_target = 0.7  # 16GB-32GB
            cores_target = 0.6
            vram_target = 0.0
            dedicated_target = 0.0
            cuda_target = 0.0
        elif usage_type == "Uso de Oficina / Estudiante":
            ram_target = 0.25  # 8GB es suficiente
            cores_target = 0.25
            vram_target = 0.0
            dedicated_target = 0.0
            cuda_target = 0.0

        # 3. Componente de Portabilidad (v_u[6])
        # Influenciado por el peso de portabilidad de MAUT
        portability_weight = maut_weights.get("portability", 0.25)
        # Si el peso de portabilidad es alto, queremos un peso muy bajo en la laptop (portabilidad alta = 1.0)
        portability_target = portability_weight
        
        # 4. Componente de Pantalla (v_u[7])
        # Influenciado por el peso de pantalla de MAUT
        screen_weight = maut_weights.get("screen", 0.25)
        screen_target = screen_weight
        
        # Ajustes adicionales de hardware según el peso de performance
        perf_weight = maut_weights.get("perf", 0.25)
        if perf_weight > 0.4:
            ram_target = max(ram_target, 0.7)
            cores_target = max(cores_target, 0.7)
            
        v_u = np.array([
            price_target,
            ram_target,
            cores_target,
            vram_target,
            dedicated_target,
            cuda_target,
            portability_target,
            screen_target
        ])
        
        return v_u

    def compute_similarity(self, laptops_df, usage_type, budget, maut_weights):
        """
        Calcula la similitud coseno S_content(i) para cada laptop respecto al perfil del usuario.
        """
        laptop_vectors = self.build_laptop_vectors(laptops_df)
        user_vector = self.build_user_vector(usage_type, budget, maut_weights)
        
        # Similitud coseno: (v_u . v_i) / (||v_u|| * ||v_i||)
        dot_product = np.dot(laptop_vectors, user_vector)
        norm_laptops = np.linalg.norm(laptop_vectors, axis=1)
        norm_user = np.linalg.norm(user_vector)
        
        # Evitar divisiones por cero
        norm_laptops[norm_laptops == 0] = 1e-9
        if norm_user == 0:
            norm_user = 1e-9
            
        cosine_similarities = dot_product / (norm_laptops * norm_user)
        
        # Asegurar rango [0, 1] (el coseno entre vectores positivos ya está entre 0 y 1)
        return np.clip(cosine_similarities, 0.0, 1.0)
