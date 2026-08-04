import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 10})

FIG_DIR = os.path.join("Iinforme_tex", "figuras")
os.makedirs(FIG_DIR, exist_ok=True)

df_laptops = pd.read_csv(os.path.join("data", "laptops.csv"))
df_ratings = pd.read_csv(os.path.join("data", "ratings.csv"))

# 1. EDA: Distribución de Precios y Marcas
plt.figure(figsize=(9, 4.5))
sns.histplot(df_laptops['price'], kde=True, color='#4f46e5', bins=20)
plt.title('Distribución de Precios del Catálogo de Laptops (USD)', fontsize=12, fontweight='bold')
plt.xlabel('Precio ($ USD)')
plt.ylabel('Frecuencia de Laptops')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "eda_distribucion_precios.png"), dpi=300)
plt.close()

# 2. EDA: Marcas y Memoria RAM
plt.figure(figsize=(9, 4.5))
sns.countplot(data=df_laptops, x='brand', hue='ram', palette='viridis')
plt.title('Distribución de Capacidad de Memoria RAM por Marca', fontsize=12, fontweight='bold')
plt.xlabel('Marca de Laptop')
plt.ylabel('Cantidad de Modelos')
plt.legend(title='RAM (GB)')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "eda_distribucion_marcas_ram.png"), dpi=300)
plt.close()

# 3. EDA: Matriz de Correlación de Atributos de Hardware
plt.figure(figsize=(8, 5))
num_cols = ['price', 'cpu_cores', 'ram', 'gpu_vram', 'weight', 'rating_avg']
corr = df_laptops[num_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)
plt.title('Matriz de Correlación entre Atributos Numéricos de Hardware', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "eda_matriz_correlacion.png"), dpi=300)
plt.close()

# 4. EDA: Distribución de Ratings por Perfil de Usuario
user_profiles_path = os.path.join("data", "user_profiles.json")
profile_names = {0: "Gamer / Power User", 1: "Estudiante / Oficina", 2: "Científico de Datos / IA"}

if os.path.exists(user_profiles_path):
    with open(user_profiles_path, "r", encoding="utf-8") as f:
        user_prof_dict = json.load(f)
    df_ratings["profile_name"] = df_ratings["user_id"].map(lambda u: profile_names.get(user_prof_dict.get(u, 1), "Estudiante / Oficina"))
else:
    df_ratings["profile_name"] = "Estudiante / Oficina"

plt.figure(figsize=(9, 4.5))
sns.boxplot(data=df_ratings, x='profile_name', y='rating', palette='Set2')
plt.title('Distribución de Calificaciones por Perfil de Usuario Latente', fontsize=12, fontweight='bold')
plt.xlabel('Perfil de Usuario Latente')
plt.ylabel('Calificación (Estrellas 1 a 5)')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "eda_distribucion_ratings_perfiles.png"), dpi=300)
plt.close()

print("¡4 Gráficos EDA generados exitosamente en Iinforme_tex/figuras/!")
