import numpy as np
import pandas as pd
import json
import os

def generate_datasets(dest_dir="data"):
    os.makedirs(dest_dir, exist_ok=True)
    
    # 1. Generate Laptops Cataloge
    np.random.seed(42)
    
    laptop_templates = [
        # Gamers / Heavy Render
        {"brand": "ASUS", "model": "ROG Strix G16", "type": "gaming", "base_price": 1600, "cpu": "Intel Core i9-13980HX", "cores": 24, "gpu": "NVIDIA RTX 4070", "vram": 8, "ram": 16, "weight": 2.5, "screen_size": 16.0, "res": "QHD (2560x1600)"},
        {"brand": "ASUS", "model": "ROG Zephyrus G14", "type": "gaming_light", "base_price": 1800, "cpu": "AMD Ryzen 9 7940HS", "cores": 8, "gpu": "NVIDIA RTX 4060", "vram": 8, "ram": 16, "weight": 1.65, "screen_size": 14.0, "res": "QHD (2560x1600)"},
        {"brand": "MSI", "model": "Katana 15", "type": "gaming", "base_price": 1100, "cpu": "Intel Core i7-13620H", "cores": 10, "gpu": "NVIDIA RTX 4060", "vram": 8, "ram": 16, "weight": 2.25, "screen_size": 15.6, "res": "FHD (1920x1080)"},
        {"brand": "MSI", "model": "Raider GE78", "type": "gaming_ultra", "base_price": 3200, "cpu": "Intel Core i9-13950HX", "cores": 24, "gpu": "NVIDIA RTX 4090", "vram": 16, "ram": 32, "weight": 3.1, "screen_size": 17.3, "res": "UHD/4K (3840x2160)"},
        {"brand": "Lenovo", "model": "Legion Pro 5", "type": "gaming", "base_price": 1400, "cpu": "AMD Ryzen 7 7745HX", "cores": 8, "gpu": "NVIDIA RTX 4060", "vram": 8, "ram": 16, "weight": 2.5, "screen_size": 16.0, "res": "QHD (2560x1600)"},
        {"brand": "Lenovo", "model": "Legion Slim 5", "type": "gaming", "base_price": 1250, "cpu": "AMD Ryzen 5 7640HS", "cores": 6, "gpu": "NVIDIA RTX 4050", "vram": 6, "ram": 16, "weight": 2.3, "screen_size": 16.0, "res": "FHD (1920x1200)"},
        {"brand": "Razer", "model": "Blade 16", "type": "gaming_ultra", "base_price": 3000, "cpu": "Intel Core i9-13950HX", "cores": 24, "gpu": "NVIDIA RTX 4080", "vram": 12, "ram": 32, "weight": 2.45, "screen_size": 16.0, "res": "QHD (2560x1600)"},
        {"brand": "Acer", "model": "Predator Helios 16", "type": "gaming", "base_price": 1500, "cpu": "Intel Core i7-13700HX", "cores": 16, "gpu": "NVIDIA RTX 4070", "vram": 8, "ram": 16, "weight": 2.6, "screen_size": 16.0, "res": "QHD (2560x1600)"},
        {"brand": "Acer", "model": "Nitro V 15", "type": "gaming_budget", "base_price": 850, "cpu": "Intel Core i5-13420H", "cores": 8, "gpu": "NVIDIA RTX 4050", "vram": 6, "ram": 8, "weight": 2.1, "screen_size": 15.6, "res": "FHD (1920x1080)"},
        {"brand": "HP", "model": "Victus 16", "type": "gaming", "base_price": 950, "cpu": "Intel Core i7-13700H", "cores": 14, "gpu": "NVIDIA RTX 4050", "vram": 6, "ram": 16, "weight": 2.3, "screen_size": 16.1, "res": "FHD (1920x1080)"},
        {"brand": "HP", "model": "Omen 16", "type": "gaming", "base_price": 1550, "cpu": "AMD Ryzen 7 7840HS", "cores": 8, "gpu": "NVIDIA RTX 4070", "vram": 8, "ram": 16, "weight": 2.4, "screen_size": 16.1, "res": "QHD (2560x1440)"},
        {"brand": "Gigabyte", "model": "G5 KF", "type": "gaming_budget", "base_price": 900, "cpu": "Intel Core i5-12500H", "cores": 12, "gpu": "NVIDIA RTX 4060", "vram": 8, "ram": 8, "weight": 2.0, "screen_size": 15.6, "res": "FHD (1920x1080)"},

        # Premium Ultrabooks / Portability
        {"brand": "Apple", "model": "MacBook Air M3", "type": "premium", "base_price": 1100, "cpu": "Apple M3", "cores": 8, "gpu": "Apple M3 GPU (8-core)", "vram": 0, "ram": 8, "weight": 1.24, "screen_size": 13.6, "res": "Retina (2560x1664)"},
        {"brand": "Apple", "model": "MacBook Air M3 15", "type": "premium", "base_price": 1300, "cpu": "Apple M3", "cores": 8, "gpu": "Apple M3 GPU (10-core)", "vram": 0, "ram": 16, "weight": 1.51, "screen_size": 15.3, "res": "Retina (2880x1864)"},
        {"brand": "Apple", "model": "MacBook Pro 14 M3 Max", "type": "workstation_apple", "base_price": 3200, "cpu": "Apple M3 Max", "cores": 14, "gpu": "Apple M3 Max GPU (30-core)", "vram": 0, "ram": 36, "weight": 1.62, "screen_size": 14.2, "res": "Liquid Retina XDR (3024x1964)"},
        {"brand": "Apple", "model": "MacBook Pro 16 M3 Pro", "type": "workstation_apple", "base_price": 2500, "cpu": "Apple M3 Pro", "cores": 12, "gpu": "Apple M3 Pro GPU (18-core)", "vram": 0, "ram": 18, "weight": 2.14, "screen_size": 16.2, "res": "Liquid Retina XDR (3456x2234)"},
        {"brand": "Dell", "model": "XPS 13 9315", "type": "premium", "base_price": 1000, "cpu": "Intel Core i5-1230U", "cores": 10, "gpu": "Intel Iris Xe", "vram": 0, "ram": 8, "weight": 1.17, "screen_size": 13.4, "res": "FHD (1920x1200)"},
        {"brand": "Dell", "model": "XPS 15 9530", "type": "premium_work", "base_price": 2100, "cpu": "Intel Core i7-13700H", "cores": 14, "gpu": "NVIDIA RTX 4060", "vram": 8, "ram": 32, "weight": 1.92, "screen_size": 15.6, "res": "OLED 3.5K (3456x2160)"},
        {"brand": "Lenovo", "model": "ThinkPad X1 Carbon Gen 11", "type": "premium_office", "base_price": 1900, "cpu": "Intel Core i7-1365U", "cores": 10, "gpu": "Intel Iris Xe", "vram": 0, "ram": 32, "weight": 1.12, "screen_size": 14.0, "res": "FHD (1920x1200)"},
        {"brand": "Lenovo", "model": "Yoga Slim 7", "type": "premium", "base_price": 950, "cpu": "AMD Ryzen 7 7840S", "cores": 8, "gpu": "AMD Radeon 780M", "vram": 0, "ram": 16, "weight": 1.35, "screen_size": 14.5, "res": "3K (2944x1840)"},
        {"brand": "HP", "model": "Spectre x360 14", "type": "premium", "base_price": 1450, "cpu": "Intel Core i7-1355U", "cores": 10, "gpu": "Intel Iris Xe", "vram": 0, "ram": 16, "weight": 1.36, "screen_size": 14.0, "res": "OLED 3K (2880x1800)"},
        {"brand": "HP", "model": "Envy x360 15", "type": "premium_budget", "base_price": 800, "cpu": "AMD Ryzen 5 7530U", "cores": 6, "gpu": "AMD Radeon Graphics", "vram": 0, "ram": 12, "weight": 1.75, "screen_size": 15.6, "res": "FHD (1920x1080)"},
        {"brand": "ASUS", "model": "Zenbook 14 OLED", "type": "premium", "base_price": 900, "cpu": "Intel Core i7-1360P", "cores": 12, "gpu": "Intel Iris Xe", "vram": 0, "ram": 16, "weight": 1.39, "screen_size": 14.0, "res": "OLED 2.8K (2880x1800)"},

        # Budget / Basic Office / Students
        {"brand": "Acer", "model": "Aspire 3", "type": "budget", "base_price": 420, "cpu": "Intel Core i3-1215U", "cores": 6, "gpu": "Intel UHD Graphics", "vram": 0, "ram": 8, "weight": 1.7, "screen_size": 15.6, "res": "FHD (1920x1080)"},
        {"brand": "Acer", "model": "Aspire 5", "type": "budget", "base_price": 550, "cpu": "AMD Ryzen 5 7520U", "cores": 4, "gpu": "AMD Radeon 610M", "vram": 0, "ram": 8, "weight": 1.8, "screen_size": 15.6, "res": "FHD (1920x1080)"},
        {"brand": "Lenovo", "model": "IdeaPad Slim 3", "type": "budget", "base_price": 480, "cpu": "Intel Core i5-12450H", "cores": 8, "gpu": "Intel UHD Graphics", "vram": 0, "ram": 8, "weight": 1.62, "screen_size": 15.6, "res": "FHD (1920x1080)"},
        {"brand": "Lenovo", "model": "IdeaPad Flex 5", "type": "budget_office", "base_price": 680, "cpu": "AMD Ryzen 7 7730U", "cores": 8, "gpu": "AMD Radeon Graphics", "vram": 0, "ram": 16, "weight": 1.55, "screen_size": 14.0, "res": "FHD (1920x1200)"},
        {"brand": "HP", "model": "15-dy2095la", "type": "budget", "base_price": 450, "cpu": "Intel Core i5-1135G7", "cores": 4, "gpu": "Intel Iris Xe", "vram": 0, "ram": 8, "weight": 1.69, "screen_size": 15.6, "res": "FHD (1920x1080)"},
        {"brand": "Dell", "model": "Inspiron 15 3520", "type": "budget", "base_price": 500, "cpu": "Intel Core i5-1235U", "cores": 10, "gpu": "Intel UHD Graphics", "vram": 0, "ram": 8, "weight": 1.65, "screen_size": 15.6, "res": "FHD (1920x1080)"},
        {"brand": "ASUS", "model": "Vivobook 15", "type": "budget", "base_price": 460, "cpu": "Intel Core i3-1220P", "cores": 10, "gpu": "Intel UHD Graphics", "vram": 0, "ram": 8, "weight": 1.7, "screen_size": 15.6, "res": "FHD (1920x1080)"}
    ]

    # Generate 150 items by mutating base templates
    laptops = []
    id_counter = 1
    
    # We will replicate the templates with slight spec mutations (RAM upgrades, Storage space, price differences)
    for i in range(5): # Create 5 variations of each template
        for t in laptop_templates:
            # Random variations
            price_factor = np.random.uniform(0.92, 1.12)
            ram_opts = [8, 16, 32] if t["type"] != "budget" else [8, 12, 16]
            if "Apple" in t["brand"]:
                ram_opts = [8, 16, 24] if "Air" in t["model"] else [18, 36, 48]
            
            # Select random RAM
            ram = int(np.random.choice(ram_opts))
            
            # Adjust price based on RAM variation and random factor
            base_ram = t["ram"]
            ram_diff = (ram - base_ram) * 10 if "Apple" in t["brand"] else (ram - base_ram) * 5
            price = round((t["base_price"] + ram_diff) * price_factor)
            
            # Resolution quality mapping
            res = t["res"]
            screen_qual = 0.6
            if "4K" in res or "Retina" in res or "3K" in res:
                screen_qual = 0.95
            elif "QHD" in res or "OLED 2.8K" in res:
                screen_qual = 0.8
            elif "FHD" in res:
                screen_qual = 0.65
            else:
                screen_qual = 0.5
            
            # Compute a general average rating
            rating_avg = round(np.random.uniform(3.7, 4.9), 2)
            
            is_dedicated = t["vram"] > 0
            is_cuda = "NVIDIA" in t["gpu"]
            
            stores = ["Amazon.com", "Falabella", "PC Componentes", "MercadoLibre"]
            selected_store = np.random.choice(stores, p=[0.5, 0.2, 0.15, 0.15]) # Mayoría Amazon
            
            clean_query = f"{t['brand']}+{t['model'].replace(' ', '+')}+{ram}GB"
            amazon_url = f"https://www.amazon.com/s?k={clean_query}"
            
            if selected_store == "Amazon.com":
                buy_url = amazon_url
            elif selected_store == "Falabella":
                buy_url = f"https://www.falabella.com.pe/falabella-pe/search?Ntt=laptop+{clean_query}"
            elif selected_store == "PC Componentes":
                buy_url = f"https://www.pccomponentes.com/buscar/?query=laptop+{clean_query}"
            else:
                buy_url = f"https://listado.mercadolibre.com.pe/laptop-{clean_query}"

            hist_low = int(round(price * np.random.uniform(0.84, 0.92)))
            hist_high = int(round(price * np.random.uniform(1.08, 1.18)))
            hist_avg = int(round((price * 2 + hist_low + hist_high) / 4))
            
            diff_from_avg = round(((price - hist_avg) / hist_avg) * 100)
            
            if price <= hist_low * 1.03:
                trend_tag = f"¡Mínimo Histórico! (${hist_low} USD)"
            elif diff_from_avg < 0:
                trend_tag = f"{abs(diff_from_avg)}% por debajo del promedio (${hist_avg} USD)"
            else:
                trend_tag = f"Precio regular (Prom: ${hist_avg} USD)"

            # Serie temporal de 6 meses (Marzo a Agosto)
            p_m1 = int(round(hist_high))
            p_m2 = int(round(hist_high * np.random.uniform(0.95, 0.99)))
            p_m3 = int(round(hist_avg * np.random.uniform(1.01, 1.05)))
            p_m4 = int(round(hist_avg))
            p_m5 = int(round(hist_low * np.random.uniform(1.02, 1.06)))
            p_m6 = int(round(price))
            price_history_json = json.dumps([p_m1, p_m2, p_m3, p_m4, p_m5, p_m6])

            laptops.append({
                "id": id_counter,
                "brand": t["brand"],
                "name": f"{t['brand']} {t['model']} ({ram}GB RAM)",
                "price": price,
                "cpu": t["cpu"],
                "cpu_cores": t["cores"],
                "ram": ram,
                "gpu": t["gpu"],
                "gpu_vram": t["vram"],
                "dedicated_gpu": is_dedicated,
                "cuda_support": is_cuda,
                "weight": round(t["weight"] + np.random.uniform(-0.1, 0.1), 2),
                "screen_size": t["screen_size"],
                "screen_resolution": res,
                "screen_quality_score": screen_qual,
                "rating_avg": rating_avg,
                "best_store": selected_store,
                "historical_low": hist_low,
                "historical_high": hist_high,
                "historical_avg": hist_avg,
                "price_trend_tag": trend_tag,
                "price_history_json": price_history_json,
                "buy_url": buy_url,
                "amazon_url": amazon_url,
                "description": f"Laptop {t['brand']} diseñada para uso tipo {t['type']} con procesador {t['cpu']}, {ram}GB de memoria RAM y pantalla de {t['screen_size']} pulgadas."
            })
            id_counter += 1
            if id_counter > 150:
                break
        if id_counter > 150:
            break
            
    df_laptops = pd.DataFrame(laptops)
    df_laptops.to_csv(os.path.join(dest_dir, "laptops.csv"), index=False, encoding='utf-8')
    print(f"Generadas {len(df_laptops)} laptops.")

    # 2. Generate 100 User Ratings
    n_users = 100
    ratings = []
    
    # Assign each user a profile type: 0 = Gamer/Power, 1 = Portability/Student, 2 = AI/DS
    # Each profile has clear preferences to make collaborative filtering learn
    user_profiles = np.random.choice([0, 1, 2], size=n_users, p=[0.3, 0.4, 0.3])
    
    for u in range(n_users):
        u_profile = user_profiles[u]
        
        # Select 15-25 random laptops for the user to rate
        n_ratings = np.random.randint(15, 26)
        rated_laptops = np.random.choice(df_laptops["id"].values, size=n_ratings, replace=False)
        
        for l_id in rated_laptops:
            laptop = df_laptops[df_laptops["id"] == l_id].iloc[0]
            
            # Base rating based on laptop average rating
            base_rating = laptop["rating_avg"]
            
            # Adjust rating according to user profile preferences
            noise = np.random.normal(0, 0.4)
            rating_adj = base_rating
            
            if u_profile == 0:  # Gamer/Power User
                if laptop["dedicated_gpu"]:
                    rating_adj += np.random.uniform(0.3, 0.8)  # Likes dedicated GPUs
                    if laptop["gpu_vram"] >= 8:
                        rating_adj += 0.3
                else:
                    rating_adj -= np.random.uniform(1.0, 2.0)  # Hates integrated GPUs
                    
            elif u_profile == 1:  # Portability & Price Conscious Student
                if laptop["weight"] < 1.5:
                    rating_adj += np.random.uniform(0.4, 1.0)  # Likes light laptops
                elif laptop["weight"] > 2.2:
                    rating_adj -= np.random.uniform(0.8, 1.8)  # Dislikes heavy laptops
                if laptop["price"] > 1800:
                    rating_adj -= 0.8  # Dislikes very expensive
                elif laptop["price"] < 800:
                    rating_adj += 0.5  # Likes cheap
                    
            elif u_profile == 2:  # Data Science / AI Engineer
                if laptop["cuda_support"]:
                    rating_adj += np.random.uniform(0.5, 1.2)  # High preference for Nvidia CUDA
                else:
                    rating_adj -= np.random.uniform(1.2, 2.2)  # Requires Nvidia CUDA
                if laptop["ram"] >= 16:
                    rating_adj += 0.4
                else:
                    rating_adj -= 1.0
                    
            # Clamp rating between 1 and 5
            final_rating = round(float(np.clip(rating_adj + noise, 1.0, 5.0)))
            ratings.append({
                "user_id": f"U{u+1:03d}",
                "laptop_id": int(l_id),
                "rating": final_rating
            })
            
    df_ratings = pd.DataFrame(ratings)
    df_ratings.to_csv(os.path.join(dest_dir, "ratings.csv"), index=False, encoding='utf-8')
    print(f"Generadas {len(df_ratings)} calificaciones de usuarios.")
    
    # Save profiles metadata for tracking (optional, helper)
    profiles_dict = {f"U{i+1:03d}": int(p) for i, p in enumerate(user_profiles)}
    with open(os.path.join(dest_dir, "user_profiles.json"), "w") as f:
        json.dump(profiles_dict, f)

if __name__ == "__main__":
    generate_datasets()
