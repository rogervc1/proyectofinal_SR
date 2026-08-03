# Sistema Híbrido de Recomendación de Laptops (2 Niveles)

Este repositorio contiene la implementación de un **Sistema de Recomendación Híbrido de Laptops** diseñado en dos niveles, combinando modelos basados en conocimiento, filtrado colaborativo y procesamiento basado en contenido.

Este sistema responde directamente a los requisitos académicos del syllabus, resolviendo problemas de **Cold Start** (Usuario Nuevo) mediante adaptabilidad dinámica y satisfaciendo restricciones de hardware duras en tiempo real.

---

## 🧩 Arquitectura del Sistema

El recomendador opera en una estructura de **Hibridación en 2 Niveles**:

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
             │  • Modelo 2 (MAUT): Utilidad cualitativa            │  (Knowledge-Based)
             │  • Modelo 3 (SVD): Preferencias latentes            │  (Collaborative)
             │  • Modelo 4 (Coseno): Similitud de specs            │  (Content-Based)
             └──────────────────────────┬──────────────────────────┘
                                        │
                                        ▼
             ┌─────────────────────────────────────────────────────┐
             │       Ranking Final de Recomendaciones Top-K        │
             └─────────────────────────────────────────────────────┘
```

### Los 4 Sub-Modelos:

1. **Modelo 1: Inferencia Lógica (Constraint-Based)**: Evalúa si una laptop es viable según el uso (e.g., *Deep Learning* requiere GPU Nvidia, VRAM $\ge$ 6GB, RAM $\ge$ 16GB) y el presupuesto. Genera una máscara binaria $M_{rules} \in \{0, 1\}$.
2. **Modelo 2: MAUT Utility Theory (Knowledge-Based)**: Normaliza y pondera características según la importancia que asigne el usuario (Precio, Rendimiento, Portabilidad, Pantalla).
3. **Modelo 3: Matrix Factorization SVD (Collaborative Filtering)**: Predice el rating implícito del usuario basándose en opiniones históricas de la comunidad. Optimizado con SGD.
4. **Modelo 4: Similitud Coseno de Atributos (Content-Based)**: Compara el vector de especificaciones de la laptop ($v_i$) frente al vector ideal de usuario ($v_u$) aplicando la similitud coseno.

---

## 📂 Estructura del Workspace

- `data/`: Contiene los datasets generados (`laptops.csv`, `ratings.csv`), la configuración de reglas (`knowledge_rules.json`) y metadatos de usuarios.
- `src/`: Lógica central del sistema de recomendación:
  - `data_generator.py`: Genera un catálogo de 150 laptops realistas y 1,997 ratings divididos en perfiles de usuarios.
  - `rules_engine.py`: Implementa el filtrado duro de restricciones (Modelo 1).
  - `maut_model.py`: Calcula la utilidad cualitativa de laptops mediante MAUT (Modelo 2).
  - `svd_model.py`: Implementa SVD en NumPy con optimización SGD (Modelo 3).
  - `content_model.py`: Genera embeddings y calcula similitud coseno (Modelo 4).
  - `hybrid_recommender.py`: Ensambla el flujo híbrido dinámico.
  - `evaluation.py`: Mide RMSE, CSR (Constraint Satisfaction Rate), Precision y Recall.
- `app/`: Servidor de aplicación y frontend:
  - `main.py`: Servidor FastAPI con endpoints REST `/api/recommend`, `/api/metrics`, etc.
  - `static/`: Frontend SPA premium (HTML5, CSS3 avanzado con Glassmorphism, JS interactivo).
- `notebooks/`: Jupyter Notebook explicativo (`proyecto_final.ipynb`).
- `requirements.txt`: Dependencias del sistema.
- `run.py`: Script unificado para inicializar datos, entrenar modelos e iniciar la aplicación.

---

## 🚀 Instalación y Ejecución

### 1. Clonar o descargar el proyecto
Asegúrate de que estás en la carpeta raíz del proyecto.

### 2. Instalar dependencias
Instala los paquetes necesarios en tu entorno Python:
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
Ejecuta el script principal `run.py`. Éste verificará la base de datos, entrenará el recomendador SVD colaborativo y levantará el servidor web en el puerto `8080`:
```bash
python run.py
```

### 4. Acceder al Dashboard
Una vez que el servidor reporte estar listo, abre tu navegador web favorito y accede a:
```
http://127.0.0.1:8080/
```

Ahí podrás interactuar con la aplicación, ajustar los sliders de utilidad, cambiar los perfiles de usuario (viendo cómo cambian dinámicamente las ponderaciones del ensamble híbrido para prevenir el Cold Start) y consultar las métricas científicas.

---

## 📈 Evaluación del Sistema (Resultados Científicos)

Nuestra evaluación comparativa frente a baselines independientes arrojó los siguientes resultados:
* **Tasa de Satisfacción de Restricciones (CSR@10)**:
  - **Sistema Híbrido**: **100.0%** (Garantiza que ningún usuario reciba hardware insuficiente).
  - **Content-Based Puro**: **65.0%** (Viola restricciones frecuentemente).
  - **SVD Colaborativo Puro**: **53.3%** (Falla casi en la mitad de las recomendaciones debido al sesgo de popularidad).
* **RMSE de SVD**: **~1.1283** (Precisión de predicción de calificaciones en split 80/20).
* **Precision@10**: El recomendador híbrido supera consistentemente a SVD Puro al re-ordenar el catálogo basándose en el vector de contenido y MAUT.

*(Los gráficos comparativos se generan en tiempo real y se visualizan en la sección "Evaluación Científica" de la interfaz web).*
*(Los gráficos comparativos se generan en tiempo real y se visualizan en la sección "Evaluación Científica" de la interfaz web).*
