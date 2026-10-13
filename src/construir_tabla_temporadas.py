"""
Construcción de la tabla equipo-temporada para la Pre-entrega 3 (modelos supervisados).

Qué hace
--------
1. Lee los CSV originales de data/raw/season_*.csv de forma robusta: por NOMBRE de columna
   (desde 2019 aparece la columna 'Time' que corre las posiciones) y quedándose solo con las
   columnas que se necesitan. En 2003/04 y 2004/05 las últimas ~45 filas traen columnas de más;
   con `on_bad_lines='skip'` esas filas se perdían (90 partidos en total).
2. Arma la tabla de posiciones de cada temporada (puntos, diferencia de gol, goles; desempate
   oficial de la Premier: diferencia de gol y luego goles a favor).
3. Agrega variables de TEMPORADAS ANTERIORES (lo que se sabe antes de que empiece la temporada)
   para predecir el Top 4 sin usar información del propio año.
4. Agrega el perfil del DT al inicio de la temporada tomándolo de dataset_final_modelo.csv,
   tratando "DT No Registrado" como dato faltante (en ese dataset a esos casos se les asignó
   es_britanico=1 hasta 2004 y 0 desde 2005, un valor imputado que depende solo del año).

Uso:  python src/construir_tabla_temporadas.py
Salida: data/processed/tabla_temporadas.csv
"""

import csv
import glob
import os

import numpy as np
import pandas as pd

# Nombres que dataset_final_modelo.csv reemplazó respecto de los CSV originales
MAPEO_NOMBRES = {
    "Man United": "Manchester United",
    "Man City": "Manchester City",
    "Spurs": "Tottenham Hotspur",
    "Nott'm Forest": "Nottingham Forest",
    "Wolves": "Wolverhampton Wanderers",
}


def raiz_del_repo():
    aqui = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(aqui, ".."))


def leer_partidos_crudos(ruta_raw):
    """Devuelve todos los partidos de data/raw/season_*.csv (Date, equipos, goles, FTR)."""
    columnas = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
    registros = []
    for archivo in sorted(glob.glob(os.path.join(ruta_raw, "season_*.csv"))):
        temporada = os.path.basename(archivo)
        with open(archivo, encoding="latin1", newline="") as fh:
            lector = csv.reader(fh)
            encabezado = [h.replace("﻿", "").replace("ï»¿", "").strip() for h in next(lector)]
            idx = {c: encabezado.index(c) for c in columnas}
            for fila in lector:
                if len(fila) <= max(idx.values()):
                    continue
                valores = [fila[idx[c]].strip() for c in columnas]
                if valores[5] in ("H", "D", "A") and valores[1] and valores[2]:
                    registros.append([temporada] + valores)
    partidos = pd.DataFrame(registros, columns=["temporada_origen"] + columnas)
    partidos["Date"] = pd.to_datetime(partidos["Date"], dayfirst=True, format="mixed")
    partidos["FTHG"] = partidos["FTHG"].astype(int)
    partidos["FTAG"] = partidos["FTAG"].astype(int)
    for col in ["HomeTeam", "AwayTeam"]:
        partidos[col] = partidos[col].replace(MAPEO_NOMBRES)
    partidos["temp_inicio"] = partidos["temporada_origen"].str[7:11].astype(int)
    return partidos


def tabla_de_posiciones(partidos):
    """Una fila por equipo y temporada con puntos, goles y posición final."""
    local = pd.DataFrame({
        "temp_inicio": partidos["temp_inicio"], "equipo": partidos["HomeTeam"],
        "pj": 1, "gf": partidos["FTHG"], "gc": partidos["FTAG"],
        "pts": np.select([partidos["FTR"] == "H", partidos["FTR"] == "D"], [3, 1], default=0),
    })
    visita = pd.DataFrame({
        "temp_inicio": partidos["temp_inicio"], "equipo": partidos["AwayTeam"],
        "pj": 1, "gf": partidos["FTAG"], "gc": partidos["FTHG"],
        "pts": np.select([partidos["FTR"] == "A", partidos["FTR"] == "D"], [3, 1], default=0),
    })
    tabla = (pd.concat([local, visita])
             .groupby(["temp_inicio", "equipo"], as_index=False)
             .agg(partidos_jugados=("pj", "sum"), puntos_totales=("pts", "sum"),
                  goles_favor=("gf", "sum"), goles_contra=("gc", "sum")))
    tabla["dif_gol"] = tabla["goles_favor"] - tabla["goles_contra"]
    tabla = tabla.sort_values(
        ["temp_inicio", "puntos_totales", "dif_gol", "goles_favor", "equipo"],
        ascending=[True, False, False, False, True])
    tabla["posicion"] = tabla.groupby("temp_inicio").cumcount() + 1
    tabla["top4"] = (tabla["posicion"] <= 4).astype(int)
    return tabla.reset_index(drop=True)


def agregar_historial(tabla):
    """Variables conocidas ANTES de la temporada: resultados de las 1, 2 y 3 temporadas previas."""
    base = tabla.set_index(["temp_inicio", "equipo"])
    prev, prev2, top4_acum = [], [], []
    for temp, equipo in zip(tabla["temp_inicio"], tabla["equipo"]):
        p1 = base.loc[(temp - 1, equipo)] if (temp - 1, equipo) in base.index else None
        p2 = base.loc[(temp - 2, equipo)] if (temp - 2, equipo) in base.index else None
        prev.append(p1)
        prev2.append(p2)
        top4_acum.append(sum(
            int(base.loc[(temp - k, equipo), "top4"]) if (temp - k, equipo) in base.index else 0
            for k in (1, 2, 3)))
    tabla = tabla.copy()
    tabla["prev_puntos"] = [p["puntos_totales"] if p is not None else np.nan for p in prev]
    tabla["prev_posicion"] = [p["posicion"] if p is not None else np.nan for p in prev]
    tabla["prev_dif_gol"] = [p["dif_gol"] if p is not None else np.nan for p in prev]
    tabla["prev_goles_favor"] = [p["goles_favor"] if p is not None else np.nan for p in prev]
    tabla["prev_goles_contra"] = [p["goles_contra"] if p is not None else np.nan for p in prev]
    tabla["prev_top4"] = [p["top4"] if p is not None else np.nan for p in prev]
    tabla["prev2_puntos"] = [p["puntos_totales"] if p is not None else np.nan for p in prev2]
    tabla["top4_ult3"] = top4_acum
    tabla["ascendido"] = tabla["prev_puntos"].isna().astype(int)  # no jugó la Premier la temporada anterior
    return tabla


def agregar_dt_inicio(tabla, ruta_procesado):
    """DT del primer partido de cada equipo en la temporada (NaN si 'DT No Registrado')."""
    df = pd.read_csv(ruta_procesado, low_memory=False,
                     usecols=["temporada_origen", "Date", "HomeTeam", "AwayTeam", "dt_home", "dt_away",
                              "es_britanico_dt_home", "es_britanico_dt_away"])
    df["Date"] = pd.to_datetime(df["Date"])
    local = df.rename(columns={"HomeTeam": "equipo", "dt_home": "dt", "es_britanico_dt_home": "brit"})
    visita = df.rename(columns={"AwayTeam": "equipo", "dt_away": "dt", "es_britanico_dt_away": "brit"})
    cols = ["temporada_origen", "Date", "equipo", "dt", "brit"]
    largo = pd.concat([local[cols], visita[cols]]).sort_values("Date")
    primero = largo.groupby(["temporada_origen", "equipo"], as_index=False).first()
    primero["temp_inicio"] = primero["temporada_origen"].str[7:11].astype(int)
    primero["dt_registrado"] = (primero["dt"] != "DT No Registrado").astype(int)
    primero["dt_britanico"] = primero["brit"].where(primero["dt_registrado"] == 1)
    primero = primero.rename(columns={"dt": "dt_inicio"})
    return tabla.merge(primero[["temp_inicio", "equipo", "dt_inicio", "dt_registrado", "dt_britanico"]],
                       on=["temp_inicio", "equipo"], how="left")


def construir(raiz=None):
    raiz = raiz or raiz_del_repo()
    partidos = leer_partidos_crudos(os.path.join(raiz, "data", "raw"))
    tabla = tabla_de_posiciones(partidos)
    tabla = agregar_historial(tabla)
    tabla = agregar_dt_inicio(tabla, os.path.join(raiz, "data", "processed", "dataset_final_modelo.csv"))
    tabla["temporada"] = (tabla["temp_inicio"].astype(str) + "-" +
                          ((tabla["temp_inicio"] + 1) % 100).astype(str).str.zfill(2))
    return partidos, tabla


if __name__ == "__main__":
    raiz = raiz_del_repo()
    partidos, tabla = construir(raiz)
    salida = os.path.join(raiz, "data", "processed", "tabla_temporadas.csv")
    tabla.to_csv(salida, index=False)
    print(f"{len(partidos)} partidos -> {len(tabla)} filas equipo-temporada guardadas en {salida}")
