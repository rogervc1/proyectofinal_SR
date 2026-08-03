import os
import sys
import uvicorn

# Asegurar PYTHONPATH correcto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_generator import generate_datasets
from src.evaluation import evaluate_metrics

def main():
    print("==============================================================")
    print("   Laptop Hybrid Recommender System - Script de Lanzamiento   ")
    print("==============================================================")
    
    # 1. Verificar y generar datos si es necesario
    laptops_path = os.path.join("data", "laptops.csv")
    ratings_path = os.path.join("data", "ratings.csv")
    
    if not os.path.exists(laptops_path) or not os.path.exists(ratings_path):
        print("\n[*] Archivos de datos faltantes. Generando catálogo y ratings sintéticos...")
        generate_datasets(dest_dir="data")
    else:
        print("\n[+] Base de datos de laptops y calificaciones encontrada.")
        
    # 2. Ejecutar evaluación inicial y gráficos
    plots_path = os.path.join("app", "static", "plots", "evaluation_csr.png")
    if not os.path.exists(plots_path):
        print("\n[*] Gráficos de evaluación faltantes. Iniciando evaluación científica...")
        evaluate_metrics(data_dir="data", output_plot_dir=os.path.join("app", "static", "plots"))
    else:
        print("[+] Gráficos de rendimiento y métricas científicas listos.")
        
    # 3. Arrancar Servidor FastAPI
    print("\n[+] Iniciando el servidor FastAPI en http://127.0.0.1:8081 ...")
    print("[+] Abre tu navegador en http://127.0.0.1:8081/ para interactuar con la aplicación.\n")
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=8081, reload=False, ws="none")

if __name__ == "__main__":
    main()
