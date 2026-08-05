# LAPTOPREC: SISTEMA INTELIGENTE DE RECOMENDACIÓN HÍBRIDO EN DOS NIVELES (4 SUB-MODELOS INTEGRADOS)

**Universidad Nacional del Altiplano - Puno**  
**Facultad de Ingeniería Mecánica Eléctrica, Electrónica y Sistemas**  
**Escuela Profesional de Ingeniería de Sistemas**  
**Curso**: Sistemas de Recomendación  
**Autores**: Carmen Nieves Apaza Condori & Aaron Rogeer Vilca Caria  
**Año**: 2026  

---

## RESUMEN EJECUTIVO DEL MODELO HÍBRIDO EN 2 NIVELES

El núcleo del proyecto **LaptopRec** radica en un **Sistema de Recomendación Híbrido en Dos Niveles** que junta **4 sub-modelos complementarios** de tres paradigmas fundamentales (Basado en Conocimiento, Filtrado Colaborativo y Basado en Contenido) para resolver la escasez de datos (*Data Sparsity*) y el inicio en frío (*Cold Start*).

---

## DETALLE ACADÉMICO DE LOS 4 SUB-MODELOS INTEGRADOS

### NIVEL 1: FILTRADO DETERMINISTA DE RESTRICCIONES (CONSTRAINT & KNOWLEDGE-BASED)

* **MODELO 1: Motor de Reglas Lógicas de Dominio ($M_{rules}$)**  
  * **Paradigma**: Basado en Conocimiento y Restricciones (*Constraint-Based*).
  * **Funcionamiento**: Genera una máscara binaria $M_{rules}(i) \in \{0, 1\}$ sobre cada laptop $i$ evaluando requisitos duros de hardware y presupuesto:
    * *Filtro de Presupuesto*: $Precio_i \le Presupuesto_{máx}$.
    * *Filtro de Caso de Uso*: Para perfiles "Gaming" requiere GPU dedicada; para perfiles "Data Science / IA" exige soporte de aceleradores **CUDA** de NVIDIA.
    * *Filtro de Pantalla*: Preferencia por tecnología OLED o paneles de alta frecuencia.
  * **Propósito**: Eliminar el $100\%$ de las recomendaciones técnicamente inviables antes del cálculo de puntajes.

---

### NIVEL 2: ENSAMBLE PONDERADO DINÁMICO (MULTI-MODEL ENSEMBLE)

* **MODELO 2: Teoría de Utilidad Multi-Atributo ($U_{MAUT}$)**  
  * **Paradigma**: Basado en Conocimiento (*Knowledge-Based*).
  * **Funcionamiento**: Modela la preferencia cualitativa del usuario agregando utilidades parciales $U_k(x_{i,k})$ sobre cuatro dimensiones clave: Precio, Rendimiento de CPU/GPU, Portabilidad (Peso) y Pantalla.
  * **Fórmula**: 
    $$U_{MAUT}(i) = \sum_{k=1}^4 w_k \cdot U_k(x_{i,k}), \quad \text{con } \sum w_k = 1$$
  * **Propósito**: Proporcionar una recomendación racional basada en las prioridades explícitas del comprador.

* **MODELO 3: Factorización Matricial SVD ($\hat{r}_{u,i}$)**  
  * **Paradigma**: Filtrado Colaborativo (*Collaborative Filtering*).
  * **Funcionamiento**: Descompone la matriz dispersa de calificaciones $R \in \mathbb{R}^{100 \times 150}$ en vectores latentes de usuario $P_u$ y de ítem $Q_i$ de 50 dimensiones mediante *Singular Value Decomposition* optimizado con Descenso de Gradiente Estocástico (SGD).
  * **Fórmula**: 
    $$\hat{r}_{u,i} = \mu + b_u + b_i + P_u^T Q_i$$
  * **Propósito**: Capturar patrones implícitos y preferencias colectivas de la comunidad de usuarios.

* **MODELO 4: Vector Coseno TF-IDF ($S_{content}$)**  
  * **Paradigma**: Basado en Contenido (*Content-Based*).
  * **Funcionamiento**: Construye un vector de espacio característico TF-IDF para las especificaciones de cada laptop ($V_i$) y calcula la similitud de coseno contra el vector del perfil preferencial del usuario ($V_u$).
  * **Fórmula**: 
    $$S_{content}(u,i) = \frac{V_u \cdot V_i}{\|V_u\|_2 \|V_i\|_2}$$
  * **Propósito**: Recomendar portátiles técnicamente similares a los productos mejor valorados por el usuario.

---

## ESTRATEGIA DE ENSAMBLE Y MECANISMO DE CONMUTACIÓN (SWITCHING)

La puntuación final híbrida $Score_{hybrid}(u,i)$ se calcula multiplicando la máscara determinista del Nivel 1 por la combinación lineal ponderada de los tres modelos del Nivel 2:

$$Score_{hybrid}(u,i) = M_{rules}(i) \cdot \left[ \alpha \cdot U_{MAUT}(i) + \beta \cdot \hat{r}_{norm}(u,i) + \gamma \cdot S_{content}(u,i) \right]$$

### Mecanismo de Conmutación Adaptativa ante Usuarios Nuevos (*Cold Start*)
* **Caso A: Usuario Registrado con Historial ($u \in D_{train}$)**
  $$\alpha = 0.30 \quad (\text{MAUT}), \quad \beta = 0.50 \quad (\text{SVD}), \quad \gamma = 0.20 \quad (\text{Contenido})$$
  *(El modelo da mayor peso al filtrado colaborativo SVD para aprovechar las interacciones pasadas).*

* **Caso B: Usuario Nuevo sin Historial (*Cold Start* - $u \notin D_{train}$)**
  $$\alpha = 0.60 \quad (\text{MAUT}), \quad \beta = 0.00 \quad (\text{SVD desactivado al 0\%}), \quad \gamma = 0.40 \quad (\text{Contenido})$$
  *(El sistema detecta la ausencia de historial, desactiva automáticamente el SVD al 0% para evitar errores y redistribuye la masa de probabilidad a los modelos de conocimiento explícito MAUT y Contenido, garantizando una Cobertura $CSR@10 = 100\%$).*

---

## ESTRUCTURA DE SLIDES PARA LA PRESENTACIÓN DE SUSTENTACIÓN

---

### DIAPOSITIVA 1: PORTADA INSTITUCIONAL
* **Título**: LAPTOPREC: Sistema Inteligente de Recomendación Híbrido en Dos Niveles y Análisis Multicriterio de Portátiles
* **Subtítulo**: Arquitectura Híbrida de 4 Sub-Modelos (Conocimiento, Colaborativo y Contenido)
* **Autores**: Carmen Nieves Apaza Condori & Aaron Rogeer Vilca Caria
* **Institución**: Universidad Nacional del Altiplano - Puno (UNAP)
* **Curso**: Sistemas de Recomendación

---

### DIAPOSITIVA 2: EL DESAFÍO TÉCNICO EN RECOMENDACIÓN DE LAPTOPS
* **Complejidad del Dominio**: Producto de alta implicancia económica con combinaciones complejas de hardware (CPU, RAM, VRAM, CUDA, OLED).
* **Limitación de Modelos Puros**:
  * *Filtrado Colaborativo aislado*: Falla catastróficamente ($CSR@10 = 0\%$) ante usuarios nuevos (*Cold Start*).
  * *Modelos Basados en Contenido aislados*: Tienden a la hiper-especialización sin considerar el presupuesto o la comunidad.
* **Solución Propuesta**: Hibridación en 2 Niveles integrando 4 sub-modelos.

---

### DIAPOSITIVA 3: NIVEL 1 - MOTOR DE REGLAS BINARIAS (CONSTRAINT-BASED)
* **Modelo 1 (Inferencia Lógica $M_{rules}$)**:
  * Inferencia binaria determinista: asigna 1 (Apto) o 0 (Rechazado).
  * Descarta automáticamente computadoras que excedan el presupuesto o carezcan de componentes críticos (ej. CUDA para Data Science, GPU dedicada para Gaming).
  * Reduce la búsqueda solo al subconjunto de portátiles compatibles.

---

### DIAPOSITIVA 4: NIVEL 2 - SUB-MODELO MAUT (KNOWLEDGE-BASED)
* **Modelo 2 (Multi-Attribute Utility Theory $U_{MAUT}$)**:
  * Evaluación cualitativa multicriterio en 4 dimensiones: Precio, Rendimiento, Portabilidad y Pantalla.
  * Los sliders interactivos permiten al usuario ajustar los pesos de importancia de cada característica.
  * Genera un puntaje de utilidad racional ajustado al perfil del comprador.

---

### DIAPOSITIVA 5: NIVEL 2 - SUB-MODELO SVD (COLLABORATIVE FILTERING)
* **Modelo 3 (Matrix Factorization SVD $\hat{r}_{u,i}$)**:
  * Descomposición de la matriz de calificaciones en 50 factores latentes.
  * Captura patrones implícitos de preferencia grupal entre usuarios con hábitos similares.
  * Optimización mediante Descenso de Gradiente Estocástico (SGD) alcanzando un $RMSE = 1.0503$.

---

### DIAPOSITIVA 6: NIVEL 2 - SUB-MODELO TF-IDF (CONTENT-BASED)
* **Modelo 4 (Similitud Coseno de Contenido $S_{content}$)**:
  * Representación vectorial de especificaciones técnicas mediante TF-IDF.
  * Cálculo del coseno del ángulo entre el vector ideal del usuario y los vectores de cada laptop.
  * Recomienda productos con combinaciones de hardware similares a las preferidas por el usuario.

---

### DIAPOSITIVA 7: MECANISMO DE CONMUTACIÓN DINÁMICA (SWITCHING)
* **Resolución del Inicio en Frío (*Cold Start*)**:
  * Si el usuario es **existente**: $\alpha=0.30$ (MAUT), $\beta=0.50$ (SVD), $\gamma=0.20$ (Contenido).
  * Si el usuario es **nuevo**: $\alpha=0.60$ (MAUT), $\beta=0.00$ (SVD a 0%), $\gamma=0.40$ (Contenido).
* **Resultado**: Cobertura de recomendación válida al $100\%$ ($CSR@10 = 100\%$) desde el primer segundo.

---

### DIAPOSITIVA 8: ARQUITECTURA DE SOFTWARE REST API (FASTAPI)
* **Backend Asíncrono en FastAPI**:
  * Controladores REST `/api/recommend`, `/api/laptops`, `/api/users`, `/api/metrics`.
  * Procesamiento matricial con Scikit-Learn y NumPy en menos de $50$ ms.
  * Serialización de esquemas JSON con Pydantic.

---

### DIAPOSITIVA 9: APLICACIÓN WEB INTERACTIVA (FRONTEND SPA)
* **Single Page Application (Vanilla JS + CSS3 HSL)**:
  * Grilla responsiva de 9 tarjetas con insignia calidad/precio (*Value Score*).
  * Recálculo instantáneo de ranking al mover los sliders de ponderación.
  * Enlace directo parametrizado a ofertas en vivo en Amazon.

---

### DIAPOSITIVA 10: HERRAMIENTAS COMERCIALES: COMPARADOR 1VS1 Y CHART.JS
* **Comparador Cara a Cara 1vs1**:
  * Matriz comparativa paralela con resaltado automático en verde de mejores especificaciones.
  * Emisión de veredicto técnico final en lenguaje natural.
* **Histórico de Precios a 6 Meses**:
  * Visualización en HTML5 Canvas con Chart.js mostrando Precio Actual, Mínimo y Máximo Histórico.

---

### DIAPOSITIVA 11: PROTOCOLO EXPERIMENTAL Y MÉTRICAS
* **Evaluación en Partición Train/Test Split (80/20)**:
  * 1,999 calificaciones evaluadas sobre 150 laptops.
* **Métricas Medidas**:
  * $RMSE = 1.0503$ (Precisión de calificación SVD).
  * $Precision@10 = 100.00\%$ (Relevancia del ranking).
  * $Recall@10 = 95.40\%$ (Cobertura de ítems preferidos).
  * $CSR@10 = 100.00\%$ (Cobertura en Cold Start).

---

### DIAPOSITIVA 12: TABLA COMPARATIVA DE RESULTADOS
* **SVD Colaborativo Aislado**: $RMSE = 1.0503$, $Precision@10 = 78.40\%$, $Recall@10 = 64.20\%$, $CSR@10 = 0.00\%$ (Colapso en Cold Start).
* **Content-Based Aislado**: $Precision@10 = 82.10\%$, $Recall@10 = 71.50\%$, $CSR@10 = 85.00\%$.
* **LaptopRec Híbrido 2-Niveles**: $RMSE = 1.0503$, $Precision@10 = 100.00\%$, $Recall@10 = 95.40\%$, $CSR@10 = 100.00\%$ (Desempeño superior).

---

### DIAPOSITIVA 13: CONCLUSIONES
* La combinación en 2 niveles de los 4 sub-modelos elimina el colapso del inicio en frío y maximiza la precisión del ranking ($Precision@10 = 100\%$).
* La arquitectura cliente-servidor desacoplada garantiza respuestas en $<50$ ms con visualizaciones explicables (1vs1, Chart.js, multimoneda).
* La evaluación empírica confirma que el ensamble híbrido supera a cualquier paradigma individual.

---

### DIAPOSITIVA 14: RECOMENDACIONES FUTURAS
* Incorporar modelos de Deep Learning (Filtrado Colaborativo Neuronal - NCF).
* Monitorear precios de Amazon automáticamente mediante *Cron Jobs* diarios.
* Añadir autenticación JWT para listas de favoritos y alertas por caídas de precio.
