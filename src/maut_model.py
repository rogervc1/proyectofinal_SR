import numpy as np
import pandas as pd

class MAUTModel:
    def __init__(self):
        self.min_max_values = {}

    def fit(self, laptops_df):
        """
        Calcula y almacena los valores mínimos y máximos globales del catálogo
        para normalizar correctamente las especificaciones.
        """
        # 1. Parámetros de Precio
        self.min_max_values["price_min"] = laptops_df["price"].min()
        self.min_max_values["price_max"] = laptops_df["price"].max()
        
        # 2. Parámetros de Rendimiento (RAM, Cores, VRAM)
        self.min_max_values["ram_min"] = laptops_df["ram"].min()
        self.min_max_values["ram_max"] = laptops_df["ram"].max()
        self.min_max_values["cores_min"] = laptops_df["cpu_cores"].min()
        self.min_max_values["cores_max"] = laptops_df["cpu_cores"].max()
        self.min_max_values["vram_min"] = laptops_df["gpu_vram"].min()
        self.min_max_values["vram_max"] = laptops_df["gpu_vram"].max()
        
        # 3. Parámetros de Portabilidad (Peso)
        self.min_max_values["weight_min"] = laptops_df["weight"].min()
        self.min_max_values["weight_max"] = laptops_df["weight"].max()
        
        # 4. Parámetros de Pantalla (Tamaño)
        self.min_max_values["screen_min"] = laptops_df["screen_size"].min()
        self.min_max_values["screen_max"] = laptops_df["screen_size"].max()

    def _normalize(self, val, min_val, max_val, invert=False):
        if max_val == min_val:
            return 1.0 if not invert else 0.0
        norm = (val - min_val) / (max_val - min_val)
        return 1.0 - norm if invert else norm

    def compute_utility(self, laptops_df, weights):
        """
        Calcula U_Knowledge para cada laptop dada una ponderación de pesos.
        weights: dict con llaves 'price', 'perf', 'portability', 'screen'
        """
        # Validar y normalizar pesos del usuario para que sumen 1
        w_sum = sum(weights.values())
        if w_sum == 0:
            w = {k: 0.25 for k in weights}
        else:
            w = {k: v / w_sum for k, v in weights.items()}
            
        n_laptops = len(laptops_df)
        u_scores = np.zeros(n_laptops)
        
        for idx, row in laptops_df.reset_index(drop=True).iterrows():
            # 1. Utilidad de Precio (Menor precio es MEJOR utilidad)
            s_price = self._normalize(
                row["price"], 
                self.min_max_values["price_min"], 
                self.min_max_values["price_max"], 
                invert=True
            )
            
            # 2. Utilidad de Rendimiento (Mayor hardware es MEJOR utilidad)
            norm_ram = self._normalize(row["ram"], self.min_max_values["ram_min"], self.min_max_values["ram_max"])
            norm_cores = self._normalize(row["cpu_cores"], self.min_max_values["cores_min"], self.min_max_values["cores_max"])
            norm_vram = self._normalize(row["gpu_vram"], self.min_max_values["vram_min"], self.min_max_values["vram_max"])
            
            s_perf = 0.3 * norm_ram + 0.3 * norm_cores + 0.4 * norm_vram
            
            # 3. Utilidad de Portabilidad (Menor peso es MEJOR utilidad)
            s_portability = self._normalize(
                row["weight"], 
                self.min_max_values["weight_min"], 
                self.min_max_values["weight_max"], 
                invert=True
            )
            
            # 4. Utilidad de Pantalla (Mayor tamaño y calidad es MEJOR utilidad)
            norm_size = self._normalize(row["screen_size"], self.min_max_values["screen_min"], self.min_max_values["screen_max"])
            norm_quality = row["screen_quality_score"] # Ya está entre 0.4 y 1.0
            
            s_screen = 0.3 * norm_size + 0.7 * norm_quality
            
            # Calcular Utilidad Multi-Atributo Ponderada
            u_knowledge = (
                w.get("price", 0.25) * s_price +
                w.get("perf", 0.25) * s_perf +
                w.get("portability", 0.25) * s_portability +
                w.get("screen", 0.25) * s_screen
            )
            u_scores[idx] = u_knowledge
            
        return u_scores
