"""
Script de Extracción y Cruce de Directores Técnicos (Premier League)

El historial de entrenadores desde Transfermarkt de los equipos de la Premier League. Cruza esa información 
con el dataset histórico de partidos para asignar el DT local y visitante a cada encuentro 
basándose en la fecha exacta en la que se disputó.
"""

import requests
from bs4 import BeautifulSoup #BeautifulSoup para buscar la tabla HTML
import pandas as pd
import time

print("--- INICIANDO PROCESO DE EXTRACCIÓN DE DTs ---")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

equipos_tm = {
    "Arsenal": "11",
    "Aston Villa": "405",
    "Bournemouth": "989",
    "Brentford": "1148",
    "Brighton": "1237",
    "Burnley": "1132",
    "Chelsea": "631",
    "Crystal Palace": "873",
    "Everton": "29",
    "Fulham": "931",
    "Leeds United": "399",
    "Leicester City": "1003",
    "Liverpool": "31",
    "Luton Town": "1031",
    "Manchester City": "281",
    "Manchester United": "985",
    "Newcastle United": "762",
    "Nottingham Forest": "703",
    "Sheffield United": "350",
    "Tottenham Hotspur": "148",
    "West Ham United": "379",
    "Wolverhampton Wanderers": "543",
    "Southampton": "180",
    "Norwich City": "1123",
    "Watford": "1010",
    "Swansea City": "2288",
    "Stoke City": "512",
    "West Bromwich Albion": "984",
    "Sunderland": "289",
    "Hull City": "3008",
    "Middlesbrough": "641",
    "Blackburn Rovers": "164",
    "Bolton Wanderers": "355",
    "Portsmouth": "1020",
    "Wigan Athletic": "1071",
    "Charlton Athletic": "358",
    "Birmingham City": "337",
    "Derby County": "22",
    "Ipswich Town": "677",
    "Queens Park Rangers": "1039",
    "Sheffield Wednesday": "1035",
    "Coventry City": "990",
    "Reading": "1032",
    "Barnsley": "349",
    "Blackpool": "1181",
    "Bradford City": "1027",
    "Cardiff City": "603",
    "Huddersfield Town": "1110",
    "Oldham Athletic": "1078",
    "Swindon Town": "352",
    "Wimbledon FC": "133"
}

lista_dts = []

for equipo, club_id in equipos_tm.items():
    print(f"Extrayendo historial de: {equipo}...")
    url = f"https://www.transfermarkt.com/-/mitarbeiterhistorie/verein/{club_id}/personalie_id/1"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tabla = soup.find('table', {'class': 'items'})
            
            if tabla:
                filas = tabla.find('tbody').find_all('tr')
                for fila in filas:
                    columnas = fila.find_all('td') # extrae todas las columnas de una fila específica dentro de una tabla web HTML.
                    if len(columnas) >= 6:
                        try:
                            dt_nombre = columnas[0].find_all('a')[-1].text.strip()
                            bandera = columnas[2].find('img')
                            nacionalidad = bandera['title'] if bandera else 'Desconocida'
                            fecha_inicio = columnas[3].text.strip()
                            fecha_fin = columnas[4].text.strip()
                            
                            lista_dts.append({
                                "equipo": equipo,
                                "dt_nombre": dt_nombre,
                                "nacionalidad": nacionalidad,
                                "fecha_inicio": fecha_inicio,
                                "fecha_fin": fecha_fin
                            })
                        except IndexError:
                            continue
        else:
             print(f"  Error {response.status_code} al acceder a {equipo}")
    except Exception as e:
        print(f"  Ocurrió un error con {equipo}: {e}")
        
    time.sleep(2)

# Convertir a DataFrame e identificar nacionalidad británica
df_dts = pd.DataFrame(lista_dts)
naciones_britanicas = ['England', 'Scotland', 'Wales', 'Northern Ireland']
df_dts['es_britanico'] = df_dts['nacionalidad'].isin(naciones_britanicas).astype(int)

# Guardar los DTs
df_dts.to_csv('data/raw/managers_transfermarkt.csv', index=False)
print(f"\nDataset de DTs guardado en: data/raw/managers_transfermarkt.csv")

print("\n--- INICIANDO CRUCE DE DATOS ---")

# Leer los partidos consolidados que guardamos en el Paso 1
try:
    df_partidos = pd.read_csv('data/processed/partidos_consolidados.csv', low_memory=False)
except FileNotFoundError:
    print("Error: No se encontró data/processed/partidos_consolidados.csv. Asegúrate de ejecutar la celda anterior.")
    raise

# Estandarización a objetos datetime para permitir operaciones matemáticas con fechas
# errors='coerce' para que los "N/A" se conviertan en nulos sin romper el código
df_partidos['Date'] = pd.to_datetime(df_partidos['Date'], format='mixed', errors='coerce')
df_dts['fecha_inicio'] = pd.to_datetime(df_dts['fecha_inicio'], format='mixed', errors='coerce')
# los nulos los reemplazo por la fecha actual
df_dts['fecha_fin'] = pd.to_datetime(df_dts['fecha_fin'], format='mixed').fillna(pd.to_datetime('today'))

# Estandarizar nombres de equipos
mapeo_equipos = {
    'Man United': 'Manchester United',
    'Man City': 'Manchester City',
    'Spurs': 'Tottenham Hotspur',
    'Nott\'m Forest': 'Nottingham Forest',
    'Wolves': 'Wolverhampton Wanderers'
}
df_partidos['HomeTeam'] = df_partidos['HomeTeam'].replace(mapeo_equipos)
df_partidos['AwayTeam'] = df_partidos['AwayTeam'].replace(mapeo_equipos)

def cruzar_dt(df_base, df_entrenadores, tipo_equipo):
    """
    Cruza el dataset de partidos con el dataset de entrenadores validando la fecha exacta.
    """
    prefijo = 'home' if tipo_equipo == 'HomeTeam' else 'away'
    
    # Elimina columnas residuales de cruces previos para evitar colisiones
    columnas_dts = ['equipo', 'fecha_inicio', 'fecha_fin', 'dt_nombre', 'nacionalidad', 'es_britanico']
    for col in columnas_dts:
        if col in df_base.columns:
            df_base = df_base.drop(columns=[col])

    # Cruce inicial por nombre del equipo
    df_temp = pd.merge(df_base, df_entrenadores, left_on=tipo_equipo, right_on='equipo', how='left')

    #Conservamos solo al DT que dirigía el día del partido 
    condicion_fecha = (df_temp['Date'] >= df_temp['fecha_inicio']) & (df_temp['Date'] <= df_temp['fecha_fin'])
    df_temp = df_temp[condicion_fecha].drop_duplicates(subset=['Date', tipo_equipo])
    
    df_temp = df_temp.rename(columns={
        'dt_nombre': f'dt_{prefijo}',
        'nacionalidad': f'nacionalidad_dt_{prefijo}',
        'es_britanico': f'es_britanico_dt_{prefijo}'
    })
    df_temp = df_temp.drop(columns=['equipo', 'fecha_inicio', 'fecha_fin'])
    
    return df_temp

print("Cruzando DTs para el equipo local...")
df_final = cruzar_dt(df_partidos, df_dts, 'HomeTeam')

print("Cruzando DTs para el equipo visitante...")
df_final = cruzar_dt(df_final, df_dts, 'AwayTeam')

df_final.to_csv('data/processed/dataset_final_modelo.csv', index=False)

print(f"\n¡Proceso completado con éxito!")
print("El dataset final se encuentra en: data/processed/dataset_final_modelo.csv")