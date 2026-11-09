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

## 4. Hallazgos del análisis exploratorio
Entre los 33 campeones, 13 tuvieron DT británico, pero ninguno desde 2013/14. Detectamos que en cerca del 70% de los equipos-temporada el DT figura como "No Registrado" y el dataset le asigna un origen según el año; por eso los análisis de nacionalidad usan solo los DT registrados.

## 5. Modelos ajustados
**Supervisado:** predecimos si un equipo termina Top 4 usando solo información de temporadas anteriores, con partición y validación temporal. Comparamos cinco modelos contra un baseline; el mejor fue la regresión logística (acertó 9 de 16 cupos en el test). Con un modelo Beta-Binomial proyectamos los campeones británicos: menos de 1 en 10 años con la historia reciente y cerca de 4 con toda la historia; el backtest mostró que el método falla, por eso son escenarios.

**No supervisado:** K-Means separó los equipos-temporada en "Dominante" y "Resto de la liga" (Silhouette 0,354 tras la mejora). El grupo Dominante concentra 102 de los 104 Top 4. DBSCAN no encontró grupos por densidad, así que los equipos forman un continuo de niveles.

## 6. Conclusiones y limitaciones
Los DT extranjeros dominan hoy la cima, pero no podemos afirmar causalidad: también cambiaron la época y el tamaño de los clubes. Limitaciones: solo 30% de los equipos-temporada tiene DT registrado, el test es chico (80 filas) y "Top 4" aproxima la clasificación real a Champions.

## 🛠 7. Estructura del repositorio
```text
├── data/
│   ├── raw/                         # CSV por temporada (Football-Data.co.uk)
│   └── processed/                   # Datasets curados y tablas para modelar
│       ├── dataset_final_modelo.csv
│       ├── tabla_temporadas.csv         # posición, puntos y Top 4 por equipo-temporada
│       ├── tabla_equipo_temporada.csv   # variables de juego para clustering
│       ├── features_clustering.csv      # variables escaladas para K-Means
│       └── clusters_kmeans_base.csv
├── notebooks/
│   ├── juntar_csv.ipynb                   # Unión de las temporadas
│   ├── exploracion_dataset.ipynb          # Pre-entrega 2: AED
│   ├── 02_modelos_supervisados.ipynb      # Pre-entrega 3: clasificación, regresión y proyección
│   ├── 03_modelos_no_supervisados.ipynb   # Pre-entrega 4 (parte 1): AED y preprocesamiento
│   ├── 03b_kmeans_base.ipynb              # Pre-entrega 4 (parte 2): K-Means base y elección de k
│   └── 03c_mejora_interpretacion.ipynb    # Pre-entrega 4 (parte 3): mejora, interpretación y DBSCAN
├── src/
│   ├── download_datos.py                  # Descarga de temporadas
│   ├── procesar_dts.py                    # Obtención de DT
│   ├── curar_y_cruzar_dts.py              # Limpieza y cruce de DT por fecha
│   └── construir_tabla_temporadas.py      # Tabla equipo-temporada con posición oficial
├── requirements.txt
└── README.md
```