# Guión y Pitch de Exposición: Sistema Híbrido de Recomendación de Laptops

**Autor:** Roger Vilcacari  
**Curso:** Sistemas de Recomendación — Proyecto Final  
**Institución:** Universidad Nacional del Altiplano (UNAP)  
**Tema:** Arquitectura en Cascada de 2 Niveles para E-Commerce de Hardware  
**Duración Total Sugerida:** 10 - 12 minutos  

---

## 📌 Diapositiva 1: Portada
**Título:** Sistema Híbrido de Recomendación de Laptops (Arquitectura en Cascada de 2 Niveles para E-Commerce de Hardware)

* **Tiempo estimado:** 30 segundos
* **Guión verbal:**
  > *"Buenas tardes profesor y miembros del jurado. Hoy les presentaré mi proyecto final titulado **'Sistema Híbrido de Recomendación de Laptops: Una Arquitectura en Cascada de 2 Niveles para E-Commerce de Hardware'**. En este trabajo abordamos el desafío de recomendar productos tecnológicos complejos donde un error en las especificaciones no solo genera insatisfacción, sino que invalida completamente la compra."*
* **Consejo de exposición:** Proyecta seguridad, haz una breve pausa al mencionar la arquitectura en cascada de 2 niveles.

---

## 📌 Diapositiva 2: Introducción y Motivación
**Título:** Introducción y Motivación

* **Tiempo estimado:** 45 segundos
* **Guión verbal:**
  > *"Comprarle una laptop a un usuario no es como recomendarle una película en Netflix. Una laptop involucra un alto costo económico y la necesidad estricta de acoplar hardware —como RAM, procesador o tarjeta gráfica— a perfiles de uso muy exigentes, desde un estudiante hasta un arquitecto o un diseñador 3D.  
  Actualmente, los motores tradicionales en e-commerce sufren de un **problema central**: recomiendan por popularidad o historial general. Esto provoca absurdos como recomendarle una laptop con procesador básico a un profesional de Render 3D solo porque 'se vende mucho'. Nuestro **objetivo** es desarrollar un sistema experto híbrido que garantice un 100% de cumplimiento en restricciones técnicas y resuelva la falta de historial inicial."*
* **Consejo de exposición:** Enfatiza el contraste entre dominios simples (cine/música) vs. dominios complejos de hardware.

---

## 📌 Diapositiva 3: Definición de los Retos Técnicos
**Título:** Definición de los Retos Técnicos

* **Tiempo estimado:** 1 minuto
* **Guión verbal:**
  > *"Para resolver esto, identificamos **tres retos clave**:  
  Primero, el **Cold Start o inicio en frío**: Las personas compran una laptop cada 3 a 5 años, por lo que el 90% de las veces el usuario entra como anónimo o nuevo sin historial previo, haciendo colapsar al filtrado colaborativo puro.  
  Segundo, las **Restricciones Duras (Constraints)**: Un falso positivo en hardware arruina la experiencia de compra. Si el sistema recomienda un equipo sin soporte CUDA a un desarrollador de IA, la recomendación fracasa por completo.  
  Tercero, el **Espacio Multidimensional**: La relevancia no se mide por marca, sino por una combinación vectorial de especificaciones como núcleos de CPU, RAM, tipo de GPU y resolución."*
* **Consejo de exposición:** Mantén la atención en por qué los algoritmos clásicos aislados fallan en este dominio.

---

## 📌 Diapositiva 4: El Dataset de Trabajo
**Título:** El Dataset de Trabajo

* **Tiempo estimado:** 45 segundos
* **Guión verbal:**
  > *"Para validar nuestra propuesta, trabajamos con el dataset 'Laptop Price Prediction' (2024), compuesto por 1,273 modelos de laptops reales en el mercado.  
  Aplicamos un **pipeline de preprocesamiento severo**: estandarizamos precios a USD, extrajimos mediante expresiones regulares (Regex) atributos críticos como gigabytes de RAM, núcleos de CPU, tipo de GPU y compatibilidad CUDA, además de crear un 'Screen Score' estandarizado.  
  Finalmente, generamos casi 3,000 interacciones sintéticas estructuradas en arquetipos reales (Gamers, Estudiantes, Editores) para entrenar los factores latentes del modelo."*
* **Consejo de exposición:** Destaca la extracción mediante Regex, demuestra que el dataset no es plano sino enriquecido técnicamente.

---

## 📌 Diapositiva 5: Solución: Arquitectura Híbrida en Cascada
**Título:** Solución: Arquitectura Híbrida en Cascada

* **Tiempo estimado:** 1 minuto
* **Guión verbal:**
  > *"Aquí presentamos la **arquitectura central** de nuestra solución: un ensamble en cascada de 2 niveles.  
  El usuario ingresa su presupuesto y su perfil de uso.  
  En el **Nivel 1**, un **Motor Constraint-Based** filtra de forma tajante e incondicional todos los equipos que no cumplen con los requisitos mínimos o el presupuesto.  
  En el **Nivel 2**, los equipos sobrevivientes entran a un **Ensamble Dinámico Ponderado** que combina tres enfoques: Teoría de Utilidad Multi-Atributo ($U_{maut}$), Similitud Coseno sobre contenido ($S_{content}$) y Factorización Matricial SVD ($\hat{r}_{svd}$). Esto genera el ranking Top-K final."*
* **Consejo de exposición:** Apunta al diagrama. Destaca que el Nivel 1 funciona como un 'filtro de seguridad' antes del ranking.

---

## 📌 Diapositiva 6: Nivel 1: Inferencia Lógica (Filtro Duro)
**Título:** Nivel 1: Inferencia Lógica (Filtro Duro)

* **Tiempo estimado:** 45 segundos
* **Guión verbal:**
  > *"Profundizando en el **Nivel 1**, este actúa como una máscara binaria $M_{rules}$.  
  Matemáticamente, asigna 1 si la laptop está dentro del presupuesto y cumple las restricciones de RAM y GPU mínimas, y 0 si falla en cualquiera de ellas.  
  Por ejemplo, si la consulta requiere 'Data Science', se exige automáticamente RAM de 16GB o más y GPU con arquitectura CUDA. Cualquier equipo que no cumpla queda eliminado instantáneamente de la búsqueda, erradicando los falsos positivos."*
* **Consejo de exposición:** Refuerza la idea de que este filtro ahorra cómputo al Nivel 2 y garantiza 0% de incompatibilidad.

---

## 📌 Diapositiva 7: Nivel 2 (Sub-Modelo A): Teoría de Utilidad (MAUT)
**Título:** Nivel 2 (Sub-Modelo A): Teoría de Utilidad (MAUT)

* **Tiempo estimado:** 45 segundos
* **Guión verbal:**
  > *"Pasando al Nivel 2, el primer sub-modelo es **MAUT (Multi-Attribute Utility Theory)**, perteneciente a los sistemas basados en conocimiento.  
  MAUT nos permite evaluar laptops aunque **nunca nadie las haya comprado ni calificado**. El usuario asigna pesos a dimensiones clave (precio, rendimiento, pantalla, portabilidad), y el sistema calcula una función de utilidad normalizando técnicamente cada atributo en el rango de 0 a 1."*
* **Consejo de exposición:** Enfatiza que MAUT es la piedra angular para vencer el problema de Cold Start sin depender de ratings históricos.

---

## 📌 Diapositiva 8: Nivel 2 (Sub-Modelo B): Factorización SVD
**Título:** Nivel 2 (Sub-Modelo B): Factorización SVD

* **Tiempo estimado:** 45 segundos
* **Guión verbal:**
  > *"El segundo sub-modelo del Nivel 2 es el **Filtrado Colaborativo mediante Factorización SVD (Singular Value Decomposition)**.  
  SVD predice la calificación $\hat{r}_{ui}$ descomponiendo la matriz de interacciones en vectores latentes para el usuario y el ítem, sumados al promedio global $\mu$ y a los sesgos $b_u$ y $b_i$, optimizado con Stochastic Gradient Descent (SGD).  
  Este modelo captura tendencias comunitarias implícitas —como preferencia de marca o reputación— y su resultado en escala de 1 a 5 estrellas se normaliza al rango $[0,1]$."*
* **Consejo de exposición:** Explica rápido la fórmula: promedio + sesgo usuario + sesgo ítem + factores ocultos.

---

## 📌 Diapositiva 9: Nivel 2 (Sub-Modelo C): Similitud Coseno
**Título:** Nivel 2 (Sub-Modelo C): Similitud Coseno

* **Tiempo estimado:** 45 segundos
* **Guión verbal:**
  > *"El tercer sub-modelo del Nivel 2 es **Content-Based Filtering basado en Similitud Coseno**.  
  Aquí construimos un vector ideal de exigencia técnica del usuario $v_u$ y lo comparamos angularmente contra el vector técnico real de cada laptop $v_i$.  
  Mide exclusivamente qué tan paralelas son las capacidades del equipo respecto a la demanda del usuario, independientemente del precio."*
* **Consejo de exposición:** Menciona que la similitud coseno da el alineamiento perfecto de características técnicas puras.

---

## 📌 Diapositiva 10: Ecuación Híbrida y Estrategia de Pesos Dinámicos
**Título:** Ecuación Híbrida y Estrategia de Pesos Dinámicos

* **Tiempo estimado:** 1 minuto
* **Guión verbal:**
  > *"La **fórmula final de puntuación** integra los tres modelos multiplicados por la máscara del Nivel 1.  
  Lo verdaderamente innovador aquí es nuestra **Estrategia de Pesos Dinámicos**:  
  Cuando entra un **Usuario Nuevo (Cold Start)**, el sistema ajusta $\alpha = 0.60$ para MAUT y $\gamma = 0.30$ para Contenido, reduciendo $\beta$ a $0.10$. Es decir, nos apoyamos en conocimiento explícito.  
  Cuando el usuario se convierte en **Frecuente** y registra historial, ajustamos $\beta = 0.50$, permitiendo que el Filtrado Colaborativo tome el control y aprenda de la comunidad."*
* **Consejo de exposición:** Señala cómo esta conmutación de pesos resuelve inteligentemente el ciclo de vida del usuario.

---

## 📌 Diapositiva 11: Implementación del Sistema Web (Dashboard)
**Título:** Implementación del Sistema Web (Dashboard)

* **Tiempo estimado:** 45 segundos
* **Guión verbal:**
  > *"Para demostrar la viabilidad práctica, desarrollamos un Dashboard Web de producción en e-commerce.  
  Utilizamos **FastAPI** en el backend para una ejecución asíncrona de subsegundo, pre-cargando los modelos en memoria.  
  En el frontend, construimos una Single Page Application moderna con diseño Glassmorphism donde el usuario puede interactuar con deslizadores, cambiar perfiles y probar la recomendación en tiempo real a través del endpoint `/api/recommend`."*
* **Consejo de exposición:** Si tienes la aplicación web en ejecución, es el momento perfecto para mostrarla brevemente.

---

## 📌 Diapositiva 12: Evaluación Científica: Constraint Satisfaction Rate (CSR)
**Título:** Evaluación Científica: Constraint Satisfaction Rate (CSR)

* **Tiempo estimado:** 1 minuto
* **Guión verbal:**
  > *"Para la validación empírica, creamos una métrica crucial para dominios con restricciones: el **Constraint Satisfaction Rate (CSR@10)**, que mide el porcentaje de ítems en el Top-10 que cumplen el 100% de los requisitos técnicos del usuario.  
  Como observan en la tabla: SVD puro solo alcanza un 31.7% de tasa de satisfacción porque recomienda laptops populares pero técnicamente incompatibles. Content-Based alcanza 48.3%.  
  Nuestra **Arquitectura Híbrida alcanza un 93.3% de CSR@10**, demostrando la superioridad radical de combinar inferencia lógica con ensamble dinámico."*
* **Consejo de exposición:** Remarca el salto abismal de 31.7% a 93.3%. Este es el resultado estrella del proyecto.

---

## 📌 Diapositiva 13: Evaluación Científica: Precisión y RMSE
**Título:** Evaluación Científica: Precisión y RMSE

* **Tiempo estimado:** 45 segundos
* **Guión verbal:**
  > *"En cuanto a predictividad estándar, el modelo SVD obtuvo un **RMSE de 1.033** en el conjunto de prueba, demostrando una excelente capacidad de estimar valoraciones con un margen menor a 1 estrella.  
  Asimismo, en las métricas de Precision@10 y Recall@10 en Cold Start, comprobamos que aunque el filtrado colaborativo se degrada sin historial, la integración del score de conocimiento MAUT sostiene la relevancia objetiva del ranking."*
* **Consejo de exposición:** Responde anticipadamente a preguntas metodológicas sobre evaluación cuantitativa.

---

## 📌 Diapositiva 14: Conclusiones y Trabajo Futuro
**Título:** Conclusiones y Trabajo Futuro

* **Tiempo estimado:** 1 minuto
* **Guión verbal:**
  > *"En **conclusión**:  
  1. La hibridación en cascada demostró ser indispensable en e-commerce de alta complejidad técnica. Los modelos puros de IA no garantizan restricciones duras por sí solos.  
  2. Transformar especificaciones crudas en una función de utilidad normalizada (MAUT) resolvió el problema del Cold Start.  
  Como **trabajo futuro**, planteamos integrar Procesamiento de Lenguaje Natural (NLP) con LLMs para que el usuario ingrese sus necesidades en lenguaje natural (ej. 'busco laptop para renderizar en Blender con $1200'), y migrar hacia bases de datos vectoriales como Milvus o Pinecone para escalar a catálogos de millones de productos."*
* **Consejo de exposición:** Cierra con una visión clara de futuro e impacto.

---

## 📌 Diapositiva 15: Cierre
**Título:** ¡Muchas Gracias!

* **Tiempo estimado:** 15 segundos
* **Guión verbal:**
  > *"Muchas gracias por su atención. Quedo atento a sus preguntas y comentarios."*
* **Consejo de exposición:** Mantén postura abierta y firme para la ronda de preguntas.

---

## 💡 Preguntas Clave del Jurado y Respuestas Recomendadas

### 1. ¿Cómo resuelves el problema de Cold Start cuando llega un usuario totalmente nuevo?
> *"Con la **estrategia de conmutación de pesos dinámicos**: ajustamos $\alpha = 0.60$ para dar mayor peso al modelo MAUT (basado en conocimiento explícito) y $\gamma = 0.30$ para similitud de contenido, reduciendo el peso de SVD ($\beta$) a $0.10$. De este modo, la recomendación no depende de calificaciones previas sino de la utilidad matemática de los atributos."*

### 2. ¿Por qué no usar simplemente un Filtrado Colaborativo tradicional (SVD)?
> *"Porque el filtrado colaborativo recomienda productos populares en función del comportamiento histórico de la comunidad, pero ignora las restricciones técnicas duras. En nuestros experimentos, SVD obtuvo solo un **31.7% de CSR@10**, lo que significa que casi el 70% de sus recomendaciones no servían para el perfil técnico consultado."*

### 3. ¿Por qué separaron el sistema en 2 niveles en lugar de meter todo en una sola fórmula?
> *"El **Nivel 1** actúa como un filtro binario que reduce el espacio de búsqueda drásticamente eliminando equipos incompatibles o fuera de presupuesto. Esto no solo garantiza el 100% de coherencia técnica, sino que optimiza el rendimiento computacional del **Nivel 2**, el cual solo procesa scoring y ranking sobre los ítems que verdaderamente son viables."*
