
import csv
import json
from pathlib import Path


# Localiza los archivos de esta carpeta
carpeta = Path(__file__).resolve().parent
ruta_csv = carpeta / "datos_refrigeracion.csv"
ruta_html = carpeta / "dashboard.html"
ruta_salida = carpeta / "dashboard_generado.html"


# Lee los datos del CSV
fechas = []
temperaturas = []
consumos = []

with open(ruta_csv, "r", newline="", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        fechas.append(fila["Día"])
        temperaturas.append(float(fila["Temperatura máxima (°C)"]))
        consumos.append(float(fila["Consumo de refrigeración (kWh)"]))


# Prepara los datos para JavaScript
datos_html = (
    "const fechas = " + json.dumps(fechas, ensure_ascii=False) + ";\n"
    "        const temperaturas = " + json.dumps(temperaturas) + ";\n"
    "        const consumos = " + json.dumps(consumos) + ";"
)


# Lee la plantilla HTML
with open(ruta_html, "r", encoding="utf-8") as archivo:
    contenido_html = archivo.read()


# Inserta los datos del CSV en la plantilla
marcador = "// DATOS_GENERADOS_AQUI"

if marcador not in contenido_html:
    raise ValueError("No se ha encontrado el marcador en dashboard.html")

contenido_html = contenido_html.replace(marcador, datos_html)


# Guarda el dashboard generado
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    archivo.write(contenido_html)

print("Dashboard generado correctamente:", ruta_salida.name)
