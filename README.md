# Premier League Data Science Project: Proyección Histórica y Predictiva de DTs Británicos vs. Extranjeros (1993 - 2026)

## 1. Resumen del Proyecto
Este proyecto analiza más de 30 años de competencia en la Premier League inglesa (1993 a 2026), integrando resultados oficiales de partidos, estadísticas de rendimiento en cancha y el historial de nacionalidades de los directores técnicos. 

El foco del estudio radica en la transformación estructural de la liga: de un dominio absoluto de directores técnicos británicos en la década de 1990 hacia la internacionalización táctica moderna. A través de un flujo integral de Data Science, se modela el rendimiento competitivo por partido y por temporada para **proyectar a 10 años la probabilidad y porcentaje de entrenadores locales (británicos) vs. extranjeros de coronarse campeones**.

---

## 2. Objetivos del Proyecto

### Objetivo General
Desarrollar un sistema analítico y predictivo mediante modelos de Machine Learning para estimar el rendimiento competitivo de los equipos según el origen de su cuerpo técnico, evaluando la tendencia de éxito y proyectando el porcentaje de clasificación a Champions League (top 4) británicos vs. extranjeros para la próxima década.

### Objetivos Específicos
1. **Análisis Exploratorio de Datos (AED - Pre-entrega 2):**
   * Examinar la evolución histórica de la proporción de DTs británicos y extranjeros en el banquillo.
   * Identificar la relación entre la nacionalidad del DT, el volumen de juego (goles, tiros, efectividad defensiva) y los puntos obtenidos.
   * Evaluar la ventaja de localía (*home advantage*) y el impacto disciplinario (tarjetas, faltas) a lo largo de las décadas.
2. **Modelos de Aprendizaje Supervisado (Pre-entrega 3):**
   * **Clasificación:** Predecir el resultado de los partidos (`FTR`: Local, Empate, Visitante) incorporando features tácticas y de dirección técnica, optimizando hiperparámetros y evitando el sobreajuste.
   * **Regresión:** Estimar los puntos acumulados por temporada para evaluar la probabilidad final de campeonato de cada equipo.
3. **Modelos de Aprendizaje No Supervisado (Pre-entrega 4):**
   * Implementar algoritmos de agrupamiento (*clustering*) sobre los directores técnicos y equipos para caracterizar perfiles de juego (ofensivo, reactivo, posesión) y evaluar si los estilos correlacionan con la nacionalidad.
4. **Proyección y Storytelling (Entrega Final):**
   * Modelar series temporales y escenarios de simulación a 10 años sobre la presencia y probabilidad de título para técnicos locales vs. extranjeros.

---

## 📂 3. Datasets Utilizados
* **Resultados y Estadísticas de Partidos:** Descargados desde [Football-Data.co.uk](https://www.football-data.co.uk/), que contiene el registro detallado fecha a fecha, goles al descanso y final, tiros al arco, faltas, córners y cuotas de apuestas desde 1993/94 hasta 2025/26.
* **Historial de Directores Técnicos:** Extracción y consolidación de periodos de gestión de entrenadores (fecha de inicio, fecha de fin y nacionalidad), cruzado con la fecha exacta de cada partido disputado.

---

## 🛠️️ 4. Estructura del Repositorio
```text
├── data/
│   ├── raw/                      # Archivos CSV por temporada y registros originales
│   └── processed/                # Datasets consolidados y cruzados por fecha
├── notebooks/
│   ├── 01_analisis_exploratorio.ipynb    # Pre-entrega 2: AED, calidad de datos y visualización
│   ├── 02_modelos_supervisados.ipynb     # Pre-entrega 3: Clasificación y Regresión
│   └── 03_clustering_no_supervisado.ipynb # Pre-entrega 4: Agrupamiento de estilos tácticos
├── src/
│   ├── download_datos.py         # Descarga automatizada de temporadas
│   └── procesar_dts.py           # Cruce y estandarización de partidos y directores técnicos
├── requirements.txt              # Librerías y dependencias
└── README.md                     # Documentación general del proyecto