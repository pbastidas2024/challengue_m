import pandas as pd
from datetime import datetime

# Leer el archivo CSV
input_csv = 'gpon_challengue.csv'  # Cambia esto por la ruta de tu archivo CSV
df = pd.read_csv(input_csv)

# Pasar todos los nombres de OLT a mayúscula
df['OLT_NAME'] = df['OLT_NAME'].str.upper()

# Convertir TIMESTAMP a datetime si no lo está ya
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])

# Agregar la columna DN con el formato "OLT/(nombre olt)"
df['DN'] = 'OLT/' + df['OLT_NAME']

# Establecer TIMESTAMP como índice
df.set_index('TIMESTAMP', inplace=True)

# Resamplear la información para mostrar una sumatoria de KPIs cada 15 minutos por OLT
kpi_columns = ['ESTABLISHED_CALLS', 'FAILED_CALLS', 'NEW_REG', 'EXPIRED_REG', 'FAILED_REG', 'GONE_REG',
               'UNAUTHORIZED_REG']
resampled_dfs = []

for olt_name, group in df.groupby('OLT_NAME'):
    # Resamplear a 5 minutos para tener los datos originales en esos intervalos
    group_resampled = group[kpi_columns].resample('5min').sum()

    # Aplicar la suma de los intervalos anteriores (3 intervalos de 5 minutos = 15 minutos)
    group_resampled = group_resampled.rolling(window=3).sum()

    # Resamplear a 15 minutos para obtener el nuevo índice de tiempo
    group_resampled = group_resampled.resample('15min').first()

    # Añadir de nuevo la columna de OLT_NAME y DN
    group_resampled['OLT_NAME'] = olt_name
    group_resampled['DN'] = 'OLT/' + olt_name
    resampled_dfs.append(group_resampled)

resampled_df = pd.concat(resampled_dfs).reset_index()

# Reordenar las columnas para que OLT_NAME y DN sean las segunda y tercera columnas
cols = ['TIMESTAMP', 'OLT_NAME', 'DN'] + kpi_columns
resampled_df = resampled_df[cols]

# Eliminar filas completamente vacías
resampled_df.dropna(how='all', subset=kpi_columns, inplace=True)

# Guardar el archivo CSV con nombre especificado
output_filename = f"GPON_CSV_OUTPUT-{datetime.now().strftime('%H-%M-%S')}.csv"
resampled_df.to_csv(output_filename, index=False)  # Guardar el DataFrame resampleado como CSV sin incluir el índice

print(f"Archivo guardado como {output_filename}")
