#!/bin/bash

# Ruta al directorio donde se encuentra tu script y el CSV generado
BASE_DIR="/home/pbastidas/scripts"
REPO_DIR="/home/pbastidas/repos/challengue_m"  # Ruta local al repositorio de GitHub

# Ejecutar el script Python para generar el CSV
python3 /mnt/c/prueba/data_challengue.py

# Generar el nombre del archivo CSV con fecha y hora actual
current_time=$(date +'%H-%M-%S')
output_filename="$REPO_DIR/GPON_CSV_OUTPUT-$current_time.csv"

# Verificar si el archivo CSV existe antes de intentar moverlo
if [ -f "$output_filename" ]; then
    echo "Inicio del script"
    echo "Archivo CSV leído"
    echo "Datos transformados y resampleados"
    echo "Archivo guardado como $output_filename"

    # Mover el archivo CSV al repositorio de GitHub
    mv "$output_filename" "$REPO_DIR"

    # Cambiar directorio al repositorio
    cd "$REPO_DIR" || exit

    # Agregar y confirmar cambios en Git
    git add .
    git commit -m "Agregado CSV generado por cronjob"

    # Subir cambios al repositorio remoto en GitHub
    git push origin master
else
    echo "El archivo $output_filename no existe."
fi
