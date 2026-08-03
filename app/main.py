import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Optional, List

# Asegurar que la raíz del proyecto está en el PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.hybrid_recommender import HybridRecommender
from src.evaluation import evaluate_metrics

app = FastAPI(
    title="Laptop Hybrid Recommender System",
    description="Sistema de recomendación híbrido de laptops en 2 niveles (Inferencia, MAUT, SVD, Content-Based)",
    version="1.0.0"
)

# Permitir peticiones CORS de cualquier origen (para desarrollo local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar recomendador híbrido
recommender = HybridRecommender(data_dir="data")

# Variables para almacenar métricas cacheadas
cached_metrics = None

@app.on_event("startup")
async def startup_event():
    # Entrenar y cargar datos en el arranque
    try:
        recommender.load_data_and_train()
        print("Modelos cargados y entrenados con éxito en FastAPI.")
    except Exception as e:
        print(f"Error cargando modelos en FastAPI: {e}")

class MautWeights(BaseModel):
    price: float
    perf: float
    portability: float
    screen: float

class RecommendRequest(BaseModel):
    user_id: str
    usage_type: str
    budget: float
    maut_weights: MautWeights
    is_cold_start: Optional[bool] = None

@app.get("/api/laptops")
def get_laptops():
    """
    Retorna el catálogo completo de laptops.
    """
    if recommender.laptops_df is None:
        recommender.load_data_and_train()
    # Convertir NaN o infinitos a formatos legibles por JSON si los hubiera
    return recommender.laptops_df.fillna("").to_dict(orient="records")

@app.get("/api/users")
def get_users():
    """
    Retorna una lista de IDs de usuarios históricos y su tipo de perfil.
    """
    if recommender.ratings_df is None:
        recommender.load_data_and_train()
    
    unique_users = sorted(recommender.ratings_df["user_id"].unique())
    
    # Intentar cargar perfiles del json
    profiles_path = "data/user_profiles.json"
    profiles = {}
    if os.path.exists(profiles_path):
        import json
        with open(profiles_path, "r") as f:
            profiles = json.load(f)
            
    # Mapeo de nombres de perfiles
    profile_mapping = {
        0: "Gamer / Power User",
        1: "Estudiante / Oficina",
        2: "Científico de Datos / IA"
    }
    
    users_info = []
    for u in unique_users:
        p_id = profiles.get(u, 1)
        users_info.append({
            "user_id": int(u),
            "profile_name": profile_mapping.get(p_id, "Estudiante / Oficina")
        })
        
    return users_info

@app.post("/api/recommend")
def get_recommendations(req: RecommendRequest):
    """
    Genera el ranking híbrido del Top-K de laptops según las preferencias.
    """
    try:
        weights_dict = {
            "price": req.maut_weights.price,
            "perf": req.maut_weights.perf,
            "portability": req.maut_weights.portability,
            "screen": req.maut_weights.screen
        }
        
        top_recs, meta = recommender.get_recommendations(
            user_id=req.user_id,
            usage_type=req.usage_type,
            budget=req.budget,
            maut_weights=weights_dict,
            top_k=9,  # Grid de 3x3 en el frontend
            is_cold_start=req.is_cold_start
        )
        
        # Formatear el DataFrame a lista de diccionarios JSON
        recs_list = top_recs.to_dict(orient="records")
        
        return {
            "meta": meta,
            "recommendations": recs_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")

@app.get("/api/metrics")
def get_metrics():
    """
    Retorna las métricas del recomendador (RMSE, CSR, Precision, Recall).
    Las cachea para evitar re-cálculos costosos.
    """
    global cached_metrics
    if cached_metrics is None:
        try:
            # Ejecutar evaluación y generar gráficos
            cached_metrics = evaluate_metrics()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al evaluar métricas: {str(e)}")
    return cached_metrics

# Servir carpeta estática con el frontend
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
