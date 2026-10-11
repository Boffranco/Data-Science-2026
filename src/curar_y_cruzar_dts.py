"""
Script: curar_y_cruzar_dts.py
Limpia partidos_consolidados.csv y cruza directores tecnicos historicos sin colisiones de nombres.
"""

import os
import pandas as pd
import numpy as np

print("=== INICIANDO CURACIÓN Y CRUCE DE DATOS ===")

# 1. Rutas seguras
ruta_partidos = "data/processed/partidos_consolidados.csv"
if not os.path.exists(ruta_partidos):
    ruta_partidos = "partidos_consolidados.csv"

df_raw = pd.read_csv(ruta_partidos, low_memory=False)

# 2. Filtrar filas residuales de managers o filas sin datos de partido
df_partidos = df_raw[df_raw['temporada_origen'] != 'managers_transfermarkt.csv'].copy()
df_partidos = df_partidos.dropna(subset=['HomeTeam', 'AwayTeam', 'Date'])

# 3. SOLUCIÓN AL ERROR: Eliminar cualquier columna residual previa para evitar colisiones _x e _y
cols_residuales = [
    'dt_nombre', 'nacionalidad', 'fecha_inicio', 'fecha_fin', 'es_britanico', 'equipo',
    'dt_home', 'nacionalidad_dt_home', 'es_britanico_dt_home',
    'dt_away', 'nacionalidad_dt_away', 'es_britanico_dt_away'
]
df_partidos = df_partidos.drop(columns=[c for c in cols_residuales if c in df_partidos.columns])

# 4. Parsear fechas y ordenar
df_partidos['Date'] = pd.to_datetime(df_partidos['Date'].astype(str), format='mixed', dayfirst=True)
df_partidos = df_partidos.sort_values('Date').reset_index(drop=True)

print(f"✓ Partidos válidos a procesar: {len(df_partidos)}")

# 5. Normalizar nombres de equipos
mapeo_equipos = {
    'Man United': 'Manchester United',
    'Man City': 'Manchester City',
    'Spurs': 'Tottenham Hotspur',
    'Tottenham': 'Tottenham Hotspur',
    "Nott'm Forest": 'Nottingham Forest',
    'Wolves': 'Wolverhampton Wanderers'
}
df_partidos['HomeTeam'] = df_partidos['HomeTeam'].replace(mapeo_equipos)
df_partidos['AwayTeam'] = df_partidos['AwayTeam'].replace(mapeo_equipos)

# 6. Base curada histórica de DTs principales (1993 - 2026)
dts_historicos = [
    # Manchester United
    ('Manchester United', 'Alex Ferguson', 'Scotland', 1, '1986-11-06', '2013-05-19'),
    ('Manchester United', 'David Moyes', 'Scotland', 1, '2013-07-01', '2014-04-22'),
    ('Manchester United', 'Louis van Gaal', 'Netherlands', 0, '2014-07-16', '2016-05-23'),
    ('Manchester United', 'Jose Mourinho', 'Portugal', 0, '2016-05-27', '2018-12-18'),
    ('Manchester United', 'Ole Gunnar Solskjaer', 'Norway', 0, '2018-12-19', '2021-11-21'),
    ('Manchester United', 'Erik ten Hag', 'Netherlands', 0, '2022-05-23', '2024-10-28'),
    ('Manchester United', 'Ruben Amorim', 'Portugal', 0, '2024-11-01', '2026-06-30'),

    # Arsenal
    ('Arsenal', 'George Graham', 'Scotland', 1, '1986-05-14', '1995-02-21'),
    ('Arsenal', 'Bruce Rioch', 'Scotland', 1, '1995-06-08', '1996-08-12'),
    ('Arsenal', 'Arsene Wenger', 'France', 0, '1996-10-01', '2018-05-13'),
    ('Arsenal', 'Unai Emery', 'Spain', 0, '2018-05-23', '2019-11-29'),
    ('Arsenal', 'Mikel Arteta', 'Spain', 0, '2019-12-22', '2026-06-30'),

    # Chelsea
    ('Chelsea', 'Glenn Hoddle', 'England', 1, '1993-06-04', '1996-05-10'),
    ('Chelsea', 'Ruud Gullit', 'Netherlands', 0, '1996-05-10', '1998-02-12'),
    ('Chelsea', 'Gianluca Vialli', 'Italy', 0, '1998-02-12', '2000-09-12'),
    ('Chelsea', 'Claudio Ranieri', 'Italy', 0, '2000-09-18', '2004-05-31'),
    ('Chelsea', 'Jose Mourinho', 'Portugal', 0, '2004-06-02', '2007-09-20'),
    ('Chelsea', 'Carlo Ancelotti', 'Italy', 0, '2009-06-01', '2011-05-22'),
    ('Chelsea', 'Antonio Conte', 'Italy', 0, '2016-07-03', '2018-07-13'),
    ('Chelsea', 'Maurizio Sarri', 'Italy', 0, '2018-07-14', '2019-06-16'),
    ('Chelsea', 'Frank Lampard', 'England', 1, '2019-07-04', '2021-01-25'),
    ('Chelsea', 'Thomas Tuchel', 'Germany', 0, '2021-01-26', '2022-09-07'),
    ('Chelsea', 'Graham Potter', 'England', 1, '2022-09-08', '2023-04-02'),
    ('Chelsea', 'Mauricio Pochettino', 'Argentina', 0, '2023-07-01', '2024-05-21'),
    ('Chelsea', 'Enzo Maresca', 'Italy', 0, '2024-06-03', '2026-06-30'),

    # Liverpool
    ('Liverpool', 'Graeme Souness', 'Scotland', 1, '1991-04-16', '1994-01-28'),
    ('Liverpool', 'Roy Evans', 'England', 1, '1994-01-31', '1998-11-12'),
    ('Liverpool', 'Gerard Houllier', 'France', 0, '1998-07-16', '2004-05-24'),
    ('Liverpool', 'Rafael Benitez', 'Spain', 0, '2004-06-16', '2010-06-03'),
    ('Liverpool', 'Roy Hodgson', 'England', 1, '2010-07-01', '2011-01-08'),
    ('Liverpool', 'Kenny Dalglish', 'Scotland', 1, '2011-01-08', '2012-05-16'),
    ('Liverpool', 'Brendan Rodgers', 'Northern Ireland', 1, '2012-06-01', '2015-10-04'),
    ('Liverpool', 'Jurgen Klopp', 'Germany', 0, '2015-10-08', '2024-05-19'),
    ('Liverpool', 'Arne Slot', 'Netherlands', 0, '2024-06-01', '2026-06-30'),

    # Manchester City
    ('Manchester City', 'Brian Horton', 'England', 1, '1993-08-28', '1995-05-16'),
    ('Manchester City', 'Alan Ball', 'England', 1, '1995-07-03', '1996-08-26'),
    ('Manchester City', 'Joe Royle', 'England', 1, '1998-02-18', '2001-05-21'),
    ('Manchester City', 'Kevin Keegan', 'England', 1, '2001-05-24', '2005-03-11'),
    ('Manchester City', 'Stuart Pearce', 'England', 1, '2005-03-21', '2007-05-14'),
    ('Manchester City', 'Sven-Goran Eriksson', 'Sweden', 0, '2007-07-06', '2008-06-02'),
    ('Manchester City', 'Mark Hughes', 'Wales', 1, '2008-06-04', '2009-12-19'),
    ('Manchester City', 'Roberto Mancini', 'Italy', 0, '2009-12-19', '2013-05-13'),
    ('Manchester City', 'Manuel Pellegrini', 'Chile', 0, '2013-06-14', '2016-06-30'),
    ('Manchester City', 'Pep Guardiola', 'Spain', 0, '2016-07-01', '2026-06-30'),

    # Newcastle United
    ('Newcastle United', 'Kevin Keegan', 'England', 1, '1992-02-05', '1997-01-08'),
    ('Newcastle United', 'Kenny Dalglish', 'Scotland', 1, '1997-01-14', '1998-08-27'),
    ('Newcastle United', 'Ruud Gullit', 'Netherlands', 0, '1998-08-28', '1999-08-28'),
    ('Newcastle United', 'Bobby Robson', 'England', 1, '1999-09-02', '2004-08-30'),
    ('Newcastle United', 'Alan Pardew', 'England', 1, '2010-12-09', '2015-01-02'),
    ('Newcastle United', 'Rafael Benitez', 'Spain', 0, '2016-03-11', '2019-06-30'),
    ('Newcastle United', 'Steve Bruce', 'England', 1, '2019-07-17', '2021-10-20'),
    ('Newcastle United', 'Eddie Howe', 'England', 1, '2021-11-08', '2026-06-30'),

    # Aston Villa
    ('Aston Villa', 'Ron Atkinson', 'England', 1, '1991-07-07', '1994-11-10'),
    ('Aston Villa', 'Brian Little', 'England', 1, '1994-11-25', '1998-02-24'),
    ('Aston Villa', 'John Gregory', 'England', 1, '1998-02-25', '2002-01-24'),
    ('Aston Villa', 'Martin O\'Neill', 'Northern Ireland', 1, '2006-08-04', '2010-08-09'),
    ('Aston Villa', 'Dean Smith', 'England', 1, '2018-10-10', '2021-11-07'),
    ('Aston Villa', 'Steven Gerrard', 'England', 1, '2021-11-11', '2022-10-20'),
    ('Aston Villa', 'Unai Emery', 'Spain', 0, '2022-11-01', '2026-06-30'),

    # Tottenham Hotspur
    ('Tottenham Hotspur', 'Osvaldo Ardiles', 'Argentina', 0, '1993-06-19', '1994-11-01'),
    ('Tottenham Hotspur', 'Gerry Francis', 'England', 1, '1994-11-15', '1997-11-19'),
    ('Tottenham Hotspur', 'Christian Gross', 'Switzerland', 0, '1997-11-20', '1998-09-05'),
    ('Tottenham Hotspur', 'George Graham', 'Scotland', 1, '1998-10-01', '2001-03-16'),
    ('Tottenham Hotspur', 'Glenn Hoddle', 'England', 1, '2001-04-02', '2003-09-21'),
    ('Tottenham Hotspur', 'Martin Jol', 'Netherlands', 0, '2004-11-05', '2007-10-25'),
    ('Tottenham Hotspur', 'Juande Ramos', 'Spain', 0, '2007-10-27', '2008-10-25'),
    ('Tottenham Hotspur', 'Harry Redknapp', 'England', 1, '2008-10-26', '2012-06-13'),
    ('Tottenham Hotspur', 'Andre Villas-Boas', 'Portugal', 0, '2012-07-03', '2013-12-16'),
    ('Tottenham Hotspur', 'Mauricio Pochettino', 'Argentina', 0, '2014-05-27', '2019-11-19'),
    ('Tottenham Hotspur', 'Jose Mourinho', 'Portugal', 0, '2019-11-20', '2021-04-19'),
    ('Tottenham Hotspur', 'Antonio Conte', 'Italy', 0, '2021-11-02', '2023-03-26'),
    ('Tottenham Hotspur', 'Ange Postecoglou', 'Australia', 0, '2023-06-06', '2026-06-30')
]

df_dts = pd.DataFrame(dts_historicos, columns=['equipo', 'dt_nombre', 'nacionalidad', 'es_britanico', 'fecha_inicio', 'fecha_fin'])
df_dts['fecha_inicio'] = pd.to_datetime(df_dts['fecha_inicio'])
df_dts['fecha_fin'] = pd.to_datetime(df_dts['fecha_fin'])

# 7. Cruce temporal estricto sin pérdida de filas
def cruzar_dt(df_base, df_entrenadores, col_equipo, prefijo):
    m = pd.merge(df_base, df_entrenadores, left_on=col_equipo, right_on='equipo', how='left')
    
    # Condición de fecha de gestión
    valid = m[(m['Date'] >= m['fecha_inicio']) & (m['Date'] <= m['fecha_fin'])].drop_duplicates(subset=['Date', col_equipo])
    
    # Left join con el dataset base de partidos
    res = pd.merge(df_base, valid[['Date', col_equipo, 'dt_nombre', 'nacionalidad', 'es_britanico']], on=['Date', col_equipo], how='left')
    
    # Imputación de contexto: antes de 2005 los entrenadores eran mayoritariamente británicos (>90%)
    default_brit = (res['Date'].dt.year < 2005).astype(float)
    res['es_britanico'] = res['es_britanico'].fillna(pd.Series(default_brit, index=res.index))
    res['nacionalidad'] = np.where(res['nacionalidad'].isna(), 
                                   np.where(res['es_britanico'] == 1.0, 'United Kingdom', 'Other'),
                                   res['nacionalidad'])
    res['dt_nombre'] = res['dt_nombre'].fillna('DT No Registrado')
    
    return res.rename(columns={
        'dt_nombre': f'dt_{prefijo}',
        'nacionalidad': f'nacionalidad_dt_{prefijo}',
        'es_britanico': f'es_britanico_dt_{prefijo}'
    })

print("Cruzando directores técnicos locales y visitantes...")
df_final = cruzar_dt(df_partidos, df_dts, 'HomeTeam', 'home')
df_final = cruzar_dt(df_final, df_dts, 'AwayTeam', 'away')

# 8. Exportar dataset final
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)
salida = os.path.join(output_dir, "dataset_final_modelo.csv")
df_final.to_csv(salida, index=False)

print(f"\n✓ CRUCE COMPLETADO EXITOSAMENTE: {salida}")
print(f"Total de partidos conservados: {len(df_final)} filas (100% de los datos)")
print(f"\nDistribución de DTs Locales Británicos:")
print(df_final['es_britanico_dt_home'].value_counts())