import os
import time
import subprocess
import threading
from playwright.sync_api import sync_playwright

DEST_DIR = os.path.join(os.getcwd(), "capturas_informe")
os.makedirs(DEST_DIR, exist_ok=True)

def start_server():
    print("[*] Iniciando servidor FastAPI...")
    os.system("python run.py")

def main():
    # Arrancar el servidor en un hilo secundario
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    print("[*] Esperando 5 segundos a que el servidor FastAPI responda en 127.0.0.1:8081...")
    time.sleep(5)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        url = "http://127.0.0.1:8081/"
        print(f"[*] Navegando a {url}...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # 1. Dashboard Principal
        print("[+] Guardando 01_dashboard_principal_hibrido.png")
        page.screenshot(path=os.path.join(DEST_DIR, "01_dashboard_principal_hibrido.png"), full_page=False)
        
        # 2. Hacer clic en "Calcular Recomendaciones"
        page.click("#btn-calculate")
        time.sleep(2)
        
        print("[+] Guardando 02_tarjeta_laptop_oferta_amazon.png")
        page.screenshot(path=os.path.join(DEST_DIR, "02_tarjeta_laptop_oferta_amazon.png"), full_page=False)
        
        # 3. Gráfica de tendencia de precios (Modal Chart.js)
        print("[*] Abriendo modal de Gráfica de Precios...")
        trend_btns = page.query_selector_all(".btn-trend-modal")
        if trend_btns and len(trend_btns) > 0:
            trend_btns[0].click()
            time.sleep(1.5)
            print("[+] Guardando 04_grafica_tendencia_precios_chartjs.png")
            page.screenshot(path=os.path.join(DEST_DIR, "04_grafica_tendencia_precios_chartjs.png"), full_page=False)
            page.click("#btn-close-price-modal")
            time.sleep(1)
            
        # 4. Comparativa 1vs1 (Head-to-Head)
        print("[*] Seleccionando 2 laptops para comparativa 1vs1...")
        chks = page.query_selector_all(".compare-chk")
        if chks and len(chks) >= 2:
            chks[0].check()
            chks[1].check()
            time.sleep(1)
            page.click("#btn-open-compare")
            time.sleep(1.5)
            print("[+] Guardando 03_comparador_head_to_head_1vs1.png")
            page.screenshot(path=os.path.join(DEST_DIR, "03_comparador_head_to_head_1vs1.png"), full_page=False)
            page.click("#btn-close-modal")
            time.sleep(1)
            
        # 5. Selector de Moneda en Soles (PEN S/)
        print("[*] Cambiando moneda a PEN (S/ Soles)...")
        page.select_option("#currency-selector", "PEN")
        time.sleep(1)
        print("[+] Guardando 05_selector_monedas_soles_pen.png")
        page.screenshot(path=os.path.join(DEST_DIR, "05_selector_monedas_soles_pen.png"), full_page=False)
        
        # 6. Filtros de estilo de vida
        print("[*] Activando filtros de estilo de vida...")
        tag_inputs = page.query_selector_all(".tag-input")
        if tag_inputs and len(tag_inputs) > 0:
            tag_inputs[0].check()
            if len(tag_inputs) > 2:
                tag_inputs[2].check()
        page.click("#btn-calculate")
        time.sleep(1.5)
        print("[+] Guardando 06_filtros_estilo_de_vida_lifestyle.png")
        page.screenshot(path=os.path.join(DEST_DIR, "06_filtros_estilo_de_vida_lifestyle.png"), full_page=False)
        
        # 7. Pestaña de Catálogo Completo
        print("[*] Navegando a la pestaña Catálogo Completo...")
        page.click("button[data-tab='tab-catalog']")
        time.sleep(1.5)
        print("[+] Guardando 07_catalogo_completo_150_laptops.png")
        page.screenshot(path=os.path.join(DEST_DIR, "07_catalogo_completo_150_laptops.png"), full_page=False)
        
        # 8. Pestaña de Evaluación Científica
        print("[*] Navegando a la pestaña Evaluación Científica...")
        page.click("button[data-tab='tab-metrics']")
        time.sleep(2.5)
        print("[+] Guardando 08_evaluacion_cientifica_metricas_csr.png")
        page.screenshot(path=os.path.join(DEST_DIR, "08_evaluacion_cientifica_metricas_csr.png"), full_page=False)
        
        browser.close()
        print("\n[SUCCESS] ¡Todas las capturas de pantalla fueron generadas exitosamente!")

if __name__ == "__main__":
    main()
