import os
import requests

# Carpeta de destino dentro de tu proyecto
output_folder = "data/raw"
os.makedirs(output_folder, exist_ok=True)

# Descarga temporadas desde 1993/1994 hasta 2025/2026
for start_year in range(1993, 2026):
    end_year = start_year + 1
    
    # Formatos de 2 dígitos y 4 dígitos
    s_start_2d = str(start_year)[-2:]
    s_end_2d = str(end_year)[-2:]
    
    # Código interno que usa Football-Data en la URL (ej: '9394')
    code = f"{s_start_2d}{s_end_2d}"
    url = f"https://www.football-data.co.uk/mmz4281/{code}/E0.csv"
    
    # Nombre del archivo con guión:
    # Opción 1 (año completo): season_1993-1994.csv
    filename = f"season_{start_year}-{end_year}.csv"

    file_path = os.path.join(output_folder, filename)
    res = requests.get(url)
    
    if res.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(res.content)
        print(f"✓ Guardado: {filename}")
    else:
        print(f"✗ No disponible: temporada {code} (Código HTTP {res.status_code})")

print("\n¡Descarga completa en data/raw/!")