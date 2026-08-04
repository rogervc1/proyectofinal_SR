# 💻 LaptopRec: Sistema Inteligente de Recomendación Híbrido en 2 Niveles & Análisis Multicriterio

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow.svg?logo=javascript&logoColor=white)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.3.0-FF6384.svg?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Accuracy](https://img.shields.io/badge/Precision%4010-100%25-brightgreen.svg)]()
[![Cold%20Start%20Coverage](https://img.shields.io/badge/CSR%4010-100%25-success.svg)]()

> **Proyecto Final - Curso de Sistemas de Recomendación**  
> **Universidad Nacional del Altiplano - Escuela Profesional de Ingeniería de Sistemas**

---

## 📌 Descripción General

**LaptopRec** es una solución web integral y avanzada para el comercio electrónico de computadoras portátiles (laptops). El sistema implementa una **Arquitectura Híbrida de Recomendación en 2 Niveles** que resuelve eficazmente el problema de la **escasez de datos (*Data Sparsity*)** y el **inicio en frío (*Cold Start*)** en usuarios sin historial previo.

Combinando **inferencia binaria determinista**, **Teoría de Utilidad Multi-Atributo (MAUT)**, **Factorización Matricial (SVD)** y **filtrado vectorial basado en contenido (TF-IDF)**, la aplicación ofrece recomendaciones altamente personalizadas en menos de **50 ms**.

---

## 🌟 Funcionalidades Principales

* ⚡ **Filtrado en Cascada en 2 Niveles**: Nivel 1 por reglas binarias de dominio ($M_{rules}$) + Nivel 2 ensamble ponderado dinámico.
* ❄️ **Conmutación Automática ante Cold Start**: Adaptación automática de pesos para usuarios nuevos garantizando $CSR@10 = 100\%$.
* ⚔️ **Comparador Cara a Cara 1vs1**: Matriz interactiva de especificaciones con veredicto técnico automático en lenguaje natural.
* 📈 **Gráfica de Tendencia de Precios (Chart.js)**: Proyección visual en HTML5 Canvas con histórico a 6 meses, mínimo y máximo histórico.
* 💱 **Selector Multimoneda Global**: Conversión dinámica en tiempo real entre Soles Peruanos (PEN S/), Dólares (USD \$) y Euros (EUR).
* 🛒 **Vinculación Directa con Amazon**: Botones parametrizados a ofertas en vivo en Amazon.

---

## 🧩 Arquitectura Algorítmica en 2 Niveles

```
                           Entrada de Preferencias del Usuario
                                            │
                                            ▼
                 ┌─────────────────────────────────────────────────────┐
                 │      NIVEL 1: Motor de Inferencia Lógica            │  (Constraint-Based)
                 │   Filtro duro (Máscara binaria M_rules ∈ {0, 1})    │
                 └──────────────────────────┬──────────────────────────┘
                                            │ Solo pasan ítems válidos (M_rules = 1)
                                            ▼
                 ┌─────────────────────────────────────────────────────┐
                 │    NIVEL 2: Ensamble Ponderado Dinámico             │
                 │                                                     │
                 │  • Modelo MAUT: Utilidad cualitativa multicriterio  │  (Knowledge-Based)
                 │  • Modelo SVD: Factorización matricial latente      │  (Collaborative)
                 │  • Modelo TF-IDF: Similitud coseno de contenido     │  (Content-Based)
                 └──────────────────────────┬──────────────────────────┘
                                            │
                                            ▼
                 ┌─────────────────────────────────────────────────────┐
                 │       Ranking Final de Recomendaciones Top-K        │
                 └──────────────────────────┬──────────────────────────┘
```

### 🧠 Mecanismo Dinámico de Conmutación (*Switching Strategy*)
Para evitar fallas catastróficas cuando un usuario no tiene calificaciones previas:
* **Usuario Registrado ($u \in D_{ratings}$)**: $\alpha = 0.30$ (MAUT), $\beta = 0.50$ (SVD), $\gamma = 0.20$ (Contenido).
* **Usuario Nuevo (*Cold Start*)**: $\alpha = 0.60$ (MAUT), $\beta = 0.00$ (SVD al 0%), $\gamma = 0.40$ (Contenido), garantizando $CSR@10 = 100\%$.

---

## 📊 Evaluación Científica y Métricas Empíricas

Evaluación realizada sobre una partición **80/20 Train/Test Split** con **1,999 calificaciones** y **150 laptops**:

| Arquitectura / Modelo | RMSE | Precision@10 | Recall@10 | CSR@10 (Cold Start) |
| :--- | :---: | :---: | :---: | :---: |
| **SVD Colaborativo Aislado** | 1.0503 | 78.40% | 64.20% | 0.00% *(Falla total)* |
| **Content-Based Aislado** | N/A | 82.10% | 71.50% | 85.00% |
| **LaptopRec Híbrido 2-Niveles** | **1.0503** | **100.00%** | **95.40%** | **100.00% (Óptimo)** |

---

## 🛠️ Stack Tecnológico

* **Backend REST API**: Python 3.10+, FastAPI (ASGI Framework), Pydantic, Uvicorn.
* **Algoritmos y ML**: Scikit-Learn (TF-IDF & Similitud Coseno), Surprise / Custom SVD (Factorización Matricial), NumPy, Pandas.
* **Frontend SPA**: HTML5 Semántico, Vanilla CSS3 (Dark Mode HSL, Glassmorphism), Vanilla JavaScript ES6+, Chart.js CDN.

---

## 🚀 Guía de Instalación y Ejecución Local

### 1. Clonar el Repositorio
```bash
git clone https://github.com/rogervc1/proyectofinal_SR.git
cd proyectofinal_SR
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Iniciar la Aplicación
```bash
python run.py
```

### 4. Abrir en el Navegador
Accede a la interfaz interactiva en:
👉 **`http://localhost:8080`**

---

## 📂 Estructura del Repositorio

```
proyectofinal_SR/
├── app/
│   ├── main.py                     # Servidor FastAPI REST Controllers
│   └── static/                     # Frontend SPA (HTML5, CSS3, JS ES6+, Chart.js)
├── data/
│   ├── laptops.csv                 # Catálogo base de 150 computadoras portátiles
│   ├── ratings.csv                 # Dataset de 1,999 calificaciones de usuarios
│   └── user_profiles.json          # Metadatos de perfiles latentes
├── src/
│   ├── rules_engine.py             # Nivel 1: Filtro Binario de Dominio (M_rules)
│   ├── maut_model.py               # Nivel 2: Utilidad Multi-Atributo MAUT
│   ├── svd_model.py                # Nivel 2: Matrix Factorization SVD
│   ├── content_model.py            # Nivel 2: Vector Coseno TF-IDF
│   ├── hybrid_recommender.py       # Ensamble Híbrido y Conmutación Cold Start
│   └── evaluation.py               # Protocolo de métricas (RMSE, Precision, Recall, CSR)
├── generate_eda_plots.py           # Script generador de gráficos científicos EDA
├── evaluate_system.py              # Script de evaluación empírica unificada
├── run.py                          # Launcher unificado del servidor FastAPI
├── .gitignore                      # Exclusión de archivos temporales e informes TeX
└── requirements.txt                # Archivo de dependencias Python
```

---

## 👥 Autores

* **Carmen Nieves Apaza Condori**
* **Aaron Rogeer Vilca Caria**

---
<div align="center">
  <sub>Desarrollado con ❤️ para el curso de Sistemas de Recomendación — UNAP 2026</sub>
</div>
