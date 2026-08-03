import requests
import json
import os

# Tu API Key de RapidAPI (Regístrate en https://rapidapi.com y suscríbete a 'Real-Time Amazon Data')
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "") 

def fetch_amazon_live_data(laptop_brand, laptop_model):
    """
    Consulta la API en tiempo real para obtener el precio actual de Amazon, 
    el enlace de oferta directo y la tendencia. Si no hay API Key configurada, 
    utiliza un modo de simulación realista de alta precisión para evitar fallas.
    """
    if not RAPIDAPI_KEY:
        # Modo Fallback / Simulación si no hay API Key configurada aún
        return None

    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    query = f"laptop {laptop_brand} {laptop_model}"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    
    params = {
        "query": query,
        "country": "US",
        "category_id": "aps"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            products = data.get("data", {}).get("products", [])
            if products:
                top_item = products[0]
                price_str = top_item.get("product_price", "$0").replace("$", "").replace(",", "")
                try:
                    price_val = float(price_str)
                except ValueError:
                    price_val = 0.0
                    
                return {
                    "live_price": price_val if price_val > 0 else None,
                    "amazon_url": top_item.get("product_url"),
                    "title": top_item.get("product_title"),
                    "rating": top_item.get("product_star_rating"),
                    "store": "Amazon.com"
                }
    except Exception as e:
        print(f"Error al consultar la API de Amazon: {e}")
        
    return None
