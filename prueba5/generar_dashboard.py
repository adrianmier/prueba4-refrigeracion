
import csv
import json
from pathlib import Path


# Obtiene la carpeta donde está este script
carpeta = Path(__file__).resolve().parent

# Define las rutas de los archivos
ruta_csv = carpeta / "datos_iluminacion.csv"
ruta_html = carpeta / "dashboard.html"
ruta_salida = carpeta / "dashboard_generado.html"


# Lee las filas del CSV
with open(ruta_csv, "r", newline="", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    filas = list(lector)

# Extrae los datos de cada columna
fechas = [fila["Día"] for fila in filas]
nubosidades = [float(fila["Nubosidad media (%)"]) for fila in filas]
usos = [float(fila["Uso estimado de iluminación (kWh)"]) for fila in filas]


# Convierte las listas a formato JSON
datos_fechas = json.dumps(fechas, ensure_ascii=False)
datos_nubosidades = json.dumps(nubosidades)
datos_usos = json.dumps(usos)


# Prepara el código JavaScript con los datos
codigo_graficos = f"""
const fechas = {datos_fechas};
const nubosidades = {datos_nubosidades};
const usos = {datos_usos};

// Configura el gráfico de nubosidad
const graficoNubosidad = echarts.init(document.getElementById("graficoNubosidad"));

graficoNubosidad.setOption({{
    title: {{
        text: "Nubosidad media diaria"
    }},
    tooltip: {{
        trigger: "axis"
    }},
    xAxis: {{
        type: "category",
        data: fechas,
        name: "Día"
    }},
    yAxis: {{
        type: "value",
        name: "Nubosidad (%)",
        min: 0,
        max: 100
    }},
    series: [{{
        name: "Nubosidad",
        type: "line",
        data: nubosidades,
        smooth: true
    }}]
}});

// Configura el gráfico de uso de iluminación
const graficoIluminacion = echarts.init(document.getElementById("graficoIluminacion"));

graficoIluminacion.setOption({{
    title: {{
        text: "Uso estimado de iluminación"
    }},
    tooltip: {{
        trigger: "axis"
    }},
    xAxis: {{
        type: "category",
        data: fechas,
        name: "Día"
    }},
    yAxis: {{
        type: "value",
        name: "Consumo (kWh)",
        min: 0
    }},
    series: [{{
        name: "Iluminación",
        type: "bar",
        data: usos
    }}]
}});
"""

# Lee la plantilla HTML
with open(ruta_html, "r", encoding="utf-8") as archivo:
    plantilla = archivo.read()

# Sustituye el marcador por los gráficos
html_final = plantilla.replace("// DATOS_GENERADOS_AQUI", codigo_graficos)

# Guarda el dashboard definitivo
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    archivo.write(html_final)

print("Dashboard generado correctamente:", ruta_salida)
