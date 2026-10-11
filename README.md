# 🏆 Premier League: Análisis Predictivo de Clasificación a Champions League y Perfiles de DTs (1993 - 2026)

## 📌 1. Resumen del Proyecto
Este proyecto analiza más de 30 temporadas de la Premier League inglesa (1993-2026), explorando la evolución competitiva y táctica de los equipos y sus cuerpos técnicos. Se investiga la transformación histórica de la liga —desde una presencia mayoritaria de entrenadores británicos en los años 90 hacia una creciente internacionalización táctica— y su impacto en el acceso a las plazas de la élite europea.

Mediante un flujo integral de Data Science, el estudio modela el rendimiento competitivo por partido y por temporada para **proyectar a 10 años la probabilidad y proporción de directores técnicos británicos vs. extranjeros clasificados a la UEFA Champions League (Top 4)**.

---

## 🎯 2. Objetivos del Proyecto

### Objetivo General
Modelar el rendimiento histórico de los equipos en la Premier League para estimar y proyectar a 10 años el porcentaje y la probabilidad de clasificación a la UEFA Champions League (Top 4) de equipos comandados por directores técnicos británicos vs. extranjeros.

### Objetivos Específicos por Etapa

* **Pre-entrega 2 (Análisis Exploratorio de Datos):**
  * Limpiar y consolidar la base histórica de más de 12.000 partidos disputados entre 1993 y 2026.
  * Examinar la evolución histórica en la contratación de DTs británicos y extranjeros en el banquillo.
  * Analizar la brecha de rendimiento en puntos por partido (PPG), volumen ofensivo (goles, tiros) y ventaja de localía entre ambos perfiles en la disputa por los primeros puestos.

* **Pre-entrega 3 (Aprendizaje Supervisado):**
  * **Regresión:** Estimar la cantidad de puntos totales por temporada que obtendrá cada equipo para evaluar si supera el umbral histórico necesario para acceder a Champions League (~71 puntos).
  * **Clasificación:** Predecir de forma directa si un equipo conseguirá la clasificación a UEFA Champions League (`1: Top 4`, `0: Fuera de Champions`), optimizando hiperparámetros y evaluando mediante métricas robustas (curvas ROC-AUC, F1-Score y matriz de confusión).

* **Pre-entrega 4 (Aprendizaje No Supervisado - Clustering):**
  * Aplicar algoritmos de clustering (K-Means) para caracterizar estilos tácticos de juego (volumen ofensivo, efectividad de remates, solidez defensiva y disciplina), identificando si los técnicos locales conforman un clúster diferenciado frente a la élite europea.

* **Entrega Final (Storytelling y Proyección):**
  * Desarrollar una proyección analítica a 10 años que estime cuántos directores técnicos británicos lograrán clasificar a la Champions League, comunicando conclusiones mediante visualizaciones orientadas a la toma de decisiones deportivas.

---

## 3. Datasets Utilizados
* **Resultados y Estadísticas de Partidos:** Registros extraídos de [Football-Data.co.uk](https://www.football-data.co.uk/) (1993 a 2026), incluyendo goles, tiros al arco, faltas, córners y cuotas de mercado.
* **Directores Técnicos:** Base curada de entrenadores, nacionalidades (británicos vs. extranjeros) y períodos de gestión temporal vinculados a cada encuentro.

---

## 🛠 4. Estructura del Repositorio
```text
├── data/
│   ├── raw/                       # Archivos CSV por temporada descargados
│   └── processed/                 # Dataset curado y unificado para modelar
├── notebooks/
│   ├── 01_analisis_exploratorio.ipynb     # Pre-entrega 2: AED y calidad de datos
│   ├── 02_modelos_supervisados.ipynb      # Pre-entrega 3: Clasificación y Regresión
│   └── 03_clustering_no_supervisado.ipynb  # Pre-entrega 4: Agrupamiento de estilos
├── src/
│   ├── download_datos.py          # Descarga automatizada de temporadas
│   └── curar_y_cruzar_dts.py      # Limpieza y cruce cronológico de entrenadores
├── requirements.txt               # Dependencias del entorno
└── README.md            # Documentación general del proyecto