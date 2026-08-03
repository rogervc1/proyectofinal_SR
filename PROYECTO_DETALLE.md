# Documentación Detallada del Proyecto: Sistema Híbrido de Recomendación de Laptops (2 Niveles)

## 📌 1. Visión General del Proyecto

El **Sistema Híbrido de Recomendación de Laptops** es una plataforma avanzada diseñada para asesorar a los usuarios en la selección del equipo portátil ideal, según sus necesidades técnicas, presupuesto e importancia asignada a características cualitativas (como rendimiento, portabilidad, pantalla y costo).

A diferencia de los sistemas de recomendación tradicionales que se basan en un único enfoque (por ejemplo, solo filtrado colaborativo o solo filtrado por contenido), este proyecto implementa una **arquitectura híbrida en 2 niveles** e integra funcionalidades avanzadas de comparación inspiradas en plataformas como *Compy*:
1. **Cold Start Problem (Usuario Nuevo)**: Cuando un usuario no posee calificaciones históricas en el sistema, la arquitectura ajusta dinámicamente sus ponderaciones internas para basarse en conocimiento experto y preferencias explícitas.
2. **Violación de Restricciones Duras (Hardware Insuficiente)**: Garantiza mediante un filtro de inferencia lógica que un usuario de uso pesado (e.g. *Deep Learning* o *Render 3D*) nunca reciba una recomendación que carezca de la GPU, VRAM o RAM mínima requerida.
3. **Comparador Cara a Cara (Head-to-Head 1vs1)**: Permite seleccionar 2 equipos del ranking y contrastarlos atributo por atributo con resaltado automático del ganador y generación de veredicto.
4. **Análisis Calidad/Precio (Value Score)**: Evalúa la relación costo-beneficio de cada laptop categorizándola en *Top Calidad/Precio*, *Precio Justo* o *Gama Premium*.
5. **Integración Multi-Tienda e Histórico de Ofertas**: Muestra precios históricos mínimos y ofertas disponibles por tienda.
6. **Exportación de Reportes PDF**: Generación inmediata de reportes imprimibles/descargables.

---

## 🏗️ 2. Arquitectura de Hibridación en 2 Niveles

La arquitectura del sistema sigue un modelo jerárquico de filtrado en cascada combinado con ensamble ponderado dinámico:

```
                               Entrada de Preferencias del Usuario
                        (Caso de Uso, Presupuesto, Sliders MAUT, User ID)
                                                │
                                                ▼
                     ┌─────────────────────────────────────────────────────┐
                     │      NIVEL 1: Motor de Inferencia Lógica            │
                     │  Filtro duro binario: M_rules ∈ {0, 1}             │
                     │  (Elimina computadoras que violan restricciones)    │
                     └──────────────────────────┬──────────────────────────┘
                                                │ Pasan únicamente ítems válidos (M_rules = 1)
                                                ▼
                     ┌─────────────────────────────────────────────────────┐
                     │    NIVEL 2: Ensamble Ponderado Dinámico             │
                     │                                                     │
                     │  • Modelo 2 (MAUT): Utilidad cualitativa (α)        │
                     │  • Modelo 3 (SVD): Preferencias latentes (β)        │
                     │  • Modelo 4 (Coseno): Similitud de specs (γ)        │
                     └──────────────────────────┬──────────────────────────┘
                                                │
                                                ▼
                     ┌─────────────────────────────────────────────────────┐
                     │       Ranking Final de Recomendaciones Top-K        │
                     └─────────────────────────────────────────────────────┘
```

---

## 🧩 3. Detalle de los 4 Sub-Modelos

### 3.1. Modelo 1: Inferencia Lógica Basada en Restricciones (Constraint-Based)
- **Ubicación en Código**: [`src/rules_engine.py`](file:///E:/X%20SEMESTER/Sistemas%20de%20Recomendaacion/sr2/proyectofinal_SR/src/rules_engine.py)
- **Función**: Actúa como la primera barrera de contención (Nivel 1). Evalúa el catálogo de laptops contra reglas estrictas de dominio declaradas en [`data/knowledge_rules.json`](file:///E:/X%20SEMESTER/Sistemas%20de%20Recomendaacion/sr2/proyectofinal_SR/data/knowledge_rules.json).
- **Filtros Aplicados**:
  - **Presupuesto**: $Precio_i \le Presupuesto_{usuario}$
  - **Deep Learning**: $VRAM \ge 6GB$, $RAM \ge 16GB$, $GPU_{Nvidia} = True$ (Soporte CUDA).
  - **Arquitectura / Render 3D**: $CPU_{Cores} \ge 8$, $GPU_{Dedicada} = True$.
  - **Desarrollo de Software**: $RAM \ge 16GB$, $CPU_{Cores} \ge 6$.
  - **Oficina / Estudiante**: $RAM \ge 8GB$, $CPU_{Cores} \ge 4$.
- **Salida**: Genera una **máscara binaria** $M_{rules}(i) \in \{0, 1\}$ para cada laptop $i$ del catálogo. Si la laptop no cumple cualquiera de los requisitos duros, $M_{rules}(i) = 0$.

---

### 3.2. Modelo 2: Teoría de Utilidad Multi-Atributo - MAUT (Knowledge-Based)
- **Ubicación en Código**: [`src/maut_model.py`](file:///E:/X%20SEMESTER/Sistemas%20de%20Recomendaacion/sr2/proyectofinal_SR/src/maut_model.py)
- **Función**: Evalúa la utilidad cualitativa $U_{MAUT}(i) \in [0, 1]$ de cada laptop en función de las prioridades declaradas por el usuario a través de cuatro ejes (sliders):
  1. **Precio** ($w_{precio}$): Normalización min-max invertida (a menor precio, mayor utilidad).
  2. **Rendimiento** ($w_{perf}$): Promedio ponderado de normalizaciones de RAM (30%), CPU Cores (30%) y VRAM (40%).
  3. **Portabilidad** ($w_{port}$): Normalización min-max invertida del peso de la laptop.
  4. **Pantalla** ($w_{screen}$): Combinación del tamaño de pantalla (30%) y la calidad del panel (70%).
- **Fórmula**:
  $$U_{MAUT}(i) = w_{precio} \cdot S_{precio}(i) + w_{perf} \cdot S_{perf}(i) + w_{port} \cdot S_{port}(i) + w_{screen} \cdot S_{screen}(i)$$

---

### 3.3. Modelo 3: Factorización Matricial SVD (Collaborative Filtering)
- **Ubicación en Código**: [`src/svd_model.py`](file:///E:/X%20SEMESTER/Sistemas%20de%20Recomendaacion/sr2/proyectofinal_SR/src/svd_model.py)
- **Función**: Captura patrones de preferencia implícitos y opiniones de la comunidad a través de la descomposición en factores latentes.
- **Algoritmo**: Implementado desde cero utilizando **NumPy** y optimizado mediante **Descenso de Gradiente Estocástico (SGD)**.
- **Ecuación de Predicción**:
  $$\hat{r}_{u,i} = \mu + b_u + b_i + P_u \cdot Q_i^T$$
  - $\mu$: Promedio global de calificaciones.
  - $b_u, b_i$: Términos de sesgo (bias) del usuario $u$ y del ítem $i$.
  - $P_u, Q_i$: Vectores de factores latentes en $\mathbb{R}^k$ ($k=10$).
- **Normalización**: Escala la predicción $\hat{r}_{u,i} \in [1, 5]$ al intervalo $[0, 1]$ mediante:
  $$r_{SVD\_norm}(u, i) = \frac{\hat{r}_{u,i} - 1.0}{4.0}$$

---

### 3.4. Modelo 4: Similitud Coseno de Atributos (Content-Based)
- **Ubicación en Código**: [`src/content_model.py`](file:///E:/X%20SEMESTER/Sistemas%20de%20Recomendaacion/sr2/proyectofinal_SR/src/content_model.py)
- **Función**: Mide la cercanía en el espacio vectorial entre la especificación técnica de la laptop ($v_i$) y el vector de aspiración ideal proyectado del usuario ($v_u$).
- **Vector de Laptop ($v_i$)**: Incluye precio invertido, RAM, cores, VRAM, presencia de GPU dedicada, soporte CUDA, peso invertido y tamaño de pantalla normalizados.
- **Vector del Usuario ($v_u$)**: Se proyecta dinámicamente según el tipo de uso seleccionado y la sensibilidad de los sliders MAUT.
- **Fórmula de Similitud Coseno**:
  $$S_{Content}(i) = \cos(v_u, v_i) = \frac{v_u \cdot v_i}{\|v_u\|_2 \cdot \|v_i\|_2}$$

---

## ⚡ 4. Ensamble Híbrido y Adaptabilidad Dinámica al Cold Start

- **Ubicación en Código**: [`src/hybrid_recommender.py`](file:///E:/X%20SEMESTER/Sistemas%20de%20Recomendaacion/sr2/proyectofinal_SR/src/hybrid_recommender.py)

El cálculo del puntaje final del sistema híbrido combina la máscara del Nivel 1 y los scores ponderados del Nivel 2:

$$Score_{Híbrido}(i) = M_{rules}(i) \cdot \Big( \alpha \cdot U_{MAUT}(i) + \beta \cdot r_{SVD\_norm}(i) + \gamma \cdot S_{Content}(i) \Big)$$

Donde $\alpha + \beta + \gamma = 1.0$.

### Estrategia de Pesos Dinámicos segun el Tipo de Usuario:

| Perfil de Usuario | $\alpha$ (MAUT) | $\beta$ (SVD) | $\gamma$ (Content) | Razón de Diseño |
| :--- | :---: | :---: | :---: | :--- |
| **Usuario Frecuente** (Con historial) | **0.30** | **0.50** | **0.20** | Prioriza las opiniones comunitarias e historial colaborativo acumulado del usuario. |
| **Cold Start** (Usuario Nuevo) | **0.60** | **0.10** | **0.30** | Desactiva el peso colaborativo (al no haber historial) y confía en el modelo de conocimiento (MAUT) y similitud de contenido. |

---

## 📊 5. Evaluación Científica y Métricas de Rendimiento

El módulo [`src/evaluation.py`](file:///E:/X%20SEMESTER/Sistemas%20de%20Recomendaacion/sr2/proyectofinal_SR/src/evaluation.py) realiza una suite de pruebas comparativas en un split 80/20 de train/test:

1. **Constraint Satisfaction Rate (CSR@10)**:
   - **Sistema Híbrido**: **100.0%** (Garantiza que el 100% de los elementos recomendados cumplan con las restricciones duras de hardware y presupuesto).
   - **Content-Based Puro**: **65.0%** (Suele recomendar laptops que sobrepasan el presupuesto o carecen de GPU dedicada).
   - **SVD Colaborativo Puro**: **53.3%** (Sufre de sesgo de popularidad, recomendando laptops populares que violan requerimientos).
2. **RMSE en Predicción de Ratings (SVD)**:
   - **Score**: **~1.1283** en el conjunto de prueba.
3. **Precision@10 y Recall@10**:
   - El ensamble híbrido logra re-ordenar el catálogo superando la precisión de SVD Puro al eliminar ítems irrelevantes mediante la ponderación cualitativa.

---

## 📁 6. Estructura Completa del Proyecto

```
proyectofinal_SR/
│
├── data/                         # Almacenamiento de datasets y reglas
│   ├── laptops.csv               # Catálogo de 150 laptops generadas con specs completas
│   ├── ratings.csv               # 1,997 calificaciones (1 a 5 estrellas) de usuarios
│   ├── user_profiles.json        # Perfiles latentes de usuarios (Gamer, Estudiante, Data Scientist)
│   └── knowledge_rules.json      # Reglas explícitas de negocio y requerimientos de hardware
│
├── src/                          # Código fuente central del recomendador
│   ├── data_generator.py         # Sintetizador de catálogo y matriz rala de interacción
│   ├── rules_engine.py           # Modelo 1: Inferencia Lógica (Constraint-Based)
│   ├── maut_model.py             # Modelo 2: Utilidad Multi-Atributo (MAUT)
│   ├── svd_model.py              # Modelo 3: Factorización Matricial SVD con SGD
│   ├── content_model.py          # Modelo 4: Embeddings y Similitud Coseno
│   ├── hybrid_recommender.py     # Orquestador del ensamble en 2 niveles
│   └── evaluation.py             # Suite de evaluación de RMSE, CSR@10, Precision@10 y Recall@10
│
├── app/                          # Servidor Web y Frontend
│   ├── main.py                   # API REST desarrollada en FastAPI
│   └── static/                   # SPA Frontend (HTML5, Glassmorphism CSS, JS dinámico)
│       ├── index.html            # Interfaz interactiva principal
│       ├── css/style.css         # Estilos visuales con estética moderna y responsive
│       ├── js/app.js             # Lógica de consumo de API REST
│       └── plots/                # Gráficos generados de la evaluación científica
│
├── requirements.txt              # Dependencias del proyecto (fastapi, uvicorn, numpy, pandas, matplotlib, seaborn)
├── run.py                        # Script unificado de inicialización y ejecución de la aplicación
└── README.md                     # Documentación de inicio rápido
```

---

## 🌐 7. Endpoints de la API REST (`app/main.py`)

- `POST /api/recommend`: Recibe el perfil del usuario, tipo de uso, presupuesto y pesos MAUT; devuelve el ranking Top-9 con desglose de puntajes de cada modelo.
- `GET /api/metrics`: Genera y retorna las métricas de rendimiento evaluadas (RMSE, CSR, Precisión, Recall) e imágenes comparativas.
- `GET /api/users`: Lista los usuarios disponibles para simulaciones.
- `GET /api/laptops`: Retorna el catálogo completo de laptops.

---

## 💻 8. Instrucciones de Ejecución

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Iniciar la aplicación**:
   ```bash
   python run.py
   ```
3. **Acceder a la aplicación Web**:
   Navegar a `http://127.0.0.1:8080/` para explorar el recomendador híbrido interactivo y sus gráficos de evaluación científica.
