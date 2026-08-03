import pandas as pd
import numpy as np
import re
import os

def load_and_clean_data(raw_csv_path="data/laptopData.csv", output_csv_path="data/laptops.csv"):
    print(f"Cargando dataset crudo desde: {raw_csv_path}")
    df = pd.read_csv(raw_csv_path)
    
    # Asegurarnos de que no haya filas totalmente nulas
    df = df.dropna(subset=['Company', 'TypeName', 'Cpu', 'Ram', 'Gpu', 'Weight', 'Price'])
    
    # 1. ID y Nombres
    df['id'] = range(1, len(df) + 1)
    df['brand'] = df['Company']
    df['model'] = df['Company'] + " " + df['TypeName']
    
    # 2. Precio (Aparentemente está en INR. 1 USD ~= 83 INR)
    # Algunos CSVs de Kaggle con este formato usan Euros, pero valores como 71378 indican INR.
    # Vamos a verificar. Si el max es > 5000, asumimos INR.
    if df['Price'].max() > 5000:
        df['price'] = (df['Price'] / 83.0).round(2)
    else:
        # Podría ser Euros o USD, lo dejamos tal cual o aproximado
        df['price'] = df['Price'].round(2)
        
    # 3. RAM (quitar "GB" y pasar a int)
    df['ram'] = df['Ram'].str.replace('GB', '').astype(int)
    
    # 4. Weight (quitar "kg" y pasar a float, manejar posibles valores erróneos)
    df['weight'] = df['Weight'].str.replace('kg', '').str.replace('?', '').str.strip()
    # Algunos tienen errores, convertimos a float forzado
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
    df['weight'] = df['weight'].fillna(df['weight'].mean()).round(2)
    
    # 5. Screen Size y Resolution
    df['screen_size'] = pd.to_numeric(df['Inches'], errors='coerce')
    # Extraer "1920x1080" de "IPS Panel Retina Display 2560x1600"
    df['screen_resolution'] = df['ScreenResolution'].str.extract(r'(\d+x\d+)')
    df['screen_resolution'] = df['screen_resolution'].fillna("1366x768")
    
    def calc_screen_quality(res_str):
        if '3840' in str(res_str): return 1.0 # 4K
        if '2560' in str(res_str) or '2880' in str(res_str): return 0.8 # 2K / Retina
        if '1920' in str(res_str): return 0.6 # FHD
        return 0.4 # HD
    df['screen_quality_score'] = df['screen_resolution'].apply(calc_screen_quality)
    
    # 6. CPU y CPU Cores (Heurística)
    df['cpu'] = df['Cpu']
    def estimate_cpu_cores(cpu_str):
        cpu_str = str(cpu_str).lower()
        if 'i7' in cpu_str or 'i9' in cpu_str or 'ryzen 7' in cpu_str or 'ryzen 9' in cpu_str:
            return 8
        elif 'i5' in cpu_str or 'ryzen 5' in cpu_str:
            return 4
        elif 'i3' in cpu_str or 'ryzen 3' in cpu_str:
            return 2
        else:
            return 2
    df['cpu_cores'] = df['Cpu'].apply(estimate_cpu_cores)
    
    # 7. GPU, VRAM, Dedicated, CUDA
    df['gpu'] = df['Gpu']
    def extract_gpu_features(gpu_str):
        gpu_str = str(gpu_str).lower()
        cuda = True if 'nvidia' in gpu_str or 'geforce' in gpu_str or 'quadro' in gpu_str else False
        dedicated = True
        vram = 4 # default for dedicated
        
        # Integradas
        if 'intel' in gpu_str or 'hd graphics' in gpu_str or 'uhd' in gpu_str or 'iris' in gpu_str:
            dedicated = False
            vram = 0
            cuda = False
        elif 'amd radeon r' in gpu_str and 'rx' not in gpu_str:
            # Algunas AMD R5/R7 son integradas
            dedicated = False
            vram = 0
            
        # Estimación de VRAM
        if '1050' in gpu_str or 'mx150' in gpu_str or 'mx250' in gpu_str:
            vram = 2
        elif '1060' in gpu_str or '1650' in gpu_str or 'rx 560' in gpu_str:
            vram = 4
        elif '1070' in gpu_str or '2060' in gpu_str or '3060' in gpu_str or 'rx 570' in gpu_str:
            vram = 6
        elif '1080' in gpu_str or '2070' in gpu_str or '2080' in gpu_str or '3070' in gpu_str or '3080' in gpu_str:
            vram = 8
            
        return pd.Series([vram, dedicated, cuda])
        
    df[['gpu_vram', 'dedicated_gpu', 'cuda_support']] = df['Gpu'].apply(extract_gpu_features)
    
    # 8. Extraer categoría base
    df['category'] = df['TypeName']
    
    # Renombrar/Filtrar columnas finales para coincidir con nuestro modelo
    final_cols = ['id', 'brand', 'model', 'category', 'price', 'cpu', 'cpu_cores', 
                  'ram', 'gpu', 'gpu_vram', 'dedicated_gpu', 'cuda_support', 
                  'weight', 'screen_size', 'screen_resolution', 'screen_quality_score']
    
    final_df = df[final_cols]
    
    # Guardar
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    final_df.to_csv(output_csv_path, index=False)
    print(f"OK Datos reales transformados guardados en: {output_csv_path} ({len(final_df)} registros)")
    return final_df

def generate_realistic_ratings(laptops_df, output_csv_path="data/ratings.csv"):
    print("Generando matriz de ratings basada en perfiles de usuarios...")
    # Simulamos 100 usuarios con diferentes perfiles
    np.random.seed(42)
    users = []
    for user_id in range(1, 101):
        # Perfiles: 0 = Gamer, 1 = Estudiante, 2 = Profesional/Dev, 3 = Ofimática
        profile = np.random.choice([0, 1, 2, 3])
        num_ratings = np.random.randint(15, 40)
        
        # Elegir laptops aleatorias para puntuar
        rated_laptops = laptops_df.sample(num_ratings)
        
        for _, row in rated_laptops.iterrows():
            laptop_id = row['id']
            base_rating = 3.0
            
            # Lógica heurística de preferencia
            if profile == 0: # Gamer
                if row['dedicated_gpu'] and row['gpu_vram'] >= 4 and row['cpu_cores'] >= 4:
                    base_rating += np.random.uniform(1.0, 2.0)
                else:
                    base_rating -= np.random.uniform(0.5, 2.0)
            
            elif profile == 1: # Estudiante
                if row['price'] <= 800 and row['weight'] <= 1.8:
                    base_rating += np.random.uniform(1.0, 2.0)
                elif row['price'] > 1500:
                    base_rating -= np.random.uniform(1.0, 2.5)
                    
            elif profile == 2: # Profesional / Dev
                if row['ram'] >= 16 and row['cpu_cores'] >= 4:
                    base_rating += np.random.uniform(1.0, 2.0)
                else:
                    base_rating -= np.random.uniform(0.5, 1.5)
            
            elif profile == 3: # Ofimática / Básica
                if row['price'] <= 600 and row['ram'] >= 4:
                    base_rating += np.random.uniform(0.5, 1.5)
                elif row['price'] > 1200:
                    base_rating -= np.random.uniform(1.0, 2.0)
            
            # Añadir ruido aleatorio
            base_rating += np.random.normal(0, 0.4)
            # Acotar entre 1 y 5
            final_rating = max(1.0, min(5.0, round(base_rating, 1)))
            
            users.append({
                'user_id': user_id,
                'laptop_id': laptop_id,
                'rating': final_rating
            })
            
    ratings_df = pd.DataFrame(users)
    ratings_df.to_csv(output_csv_path, index=False)
    print(f"OK Ratings generados guardados en: {output_csv_path} ({len(ratings_df)} interacciones)")
    return ratings_df

if __name__ == "__main__":
    laptops = load_and_clean_data()
    ratings = generate_realistic_ratings(laptops)
