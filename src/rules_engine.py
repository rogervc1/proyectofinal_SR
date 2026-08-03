import json
import os
import numpy as np
import pandas as pd

class LogicInferenceModel:
    def __init__(self, rules_path="data/knowledge_rules.json"):
        self.rules_path = rules_path
        self.rules = self._load_rules()
        
    def _load_rules(self):
        # Fallback default rules if file is missing
        default_rules = {
            "Deep Learning": {"min_vram": 6, "min_ram": 16, "cuda_required": True},
            "Arquitectura / Render 3D": {"min_cpu_cores": 8, "dedicated_gpu_required": True},
            "Desarrollo de Software": {"min_ram": 16, "min_cpu_cores": 6},
            "Uso de Oficina / Estudiante": {"min_ram": 8, "min_cpu_cores": 4}
        }
        
        if os.path.exists(self.rules_path):
            try:
                with open(self.rules_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading rules, using defaults. Error: {e}")
                return default_rules
        return default_rules

    def get_binary_mask(self, laptops_df, usage_type, budget, lifestyle_tags=None):
        """
        Calcula la máscara binaria M_rules(i) para cada laptop.
        Retorna una serie de Pandas o array de NumPy con valores 1 o 0.
        """
        # Inicializar máscara en 1 (todos pasan)
        mask = np.ones(len(laptops_df), dtype=int)
        
        # 1. Filtro duro de presupuesto (Precio <= Presupuesto)
        if budget is not None and budget > 0:
            mask = mask & (laptops_df["price"] <= budget).astype(int)
            
        # 2. Filtros duros de hardware según el caso de uso
        if usage_type in self.rules:
            rule = self.rules[usage_type]
            
            # RAM Mínima
            if "min_ram" in rule:
                mask = mask & (laptops_df["ram"] >= rule["min_ram"]).astype(int)
                
            # Núcleos de CPU Mínimos
            if "min_cpu_cores" in rule:
                mask = mask & (laptops_df["cpu_cores"] >= rule["min_cpu_cores"]).astype(int)
                
            # GPU Dedicada requerida
            if rule.get("dedicated_gpu_required", False):
                mask = mask & (laptops_df["dedicated_gpu"] == True).astype(int)
                
            # VRAM Mínima
            if "min_vram" in rule:
                mask = mask & (laptops_df["gpu_vram"] >= rule["min_vram"]).astype(int)
                
            # Soporte CUDA requerido (GPU Nvidia)
            if rule.get("cuda_required", False):
                mask = mask & (laptops_df["cuda_support"] == True).astype(int)
                
        # 3. Filtros secundarios por etiquetas de estilo de vida
        if lifestyle_tags:
            if "ultra_portable" in lifestyle_tags:
                mask = mask & (laptops_df["weight"] <= 1.5).astype(int)
            if "oled_screen" in lifestyle_tags:
                mask = mask & (laptops_df["screen_quality_score"] >= 0.8).astype(int)
            if "high_ram" in lifestyle_tags:
                mask = mask & (laptops_df["ram"] >= 16).astype(int)
            if "nvidia_gpu" in lifestyle_tags:
                mask = mask & (laptops_df["cuda_support"] == True).astype(int)
                
        return mask
