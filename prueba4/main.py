

import json
import csv
from urllib.request import urlopen
from urllib.parse import urlencode


# Calcula el consumo según la temperatura máxima
def calcular_consumo(temperatura_maxima):
    if temperatura_maxima >= 25:
        consumo = (temperatura_maxima - 25) * 10
    else:
        consumo = 0

    return consumo


# Coordenadas de Madrid y parámetros de la API
parametros = {
    "latitude": 40.4168,
    "longitude": -3.7038,
    "daily": "temperature_2m_max",
    "forecast_days": 7,
    "timezone": "Europe/Madrid"
}

# Construye la URL con los parámetros
url = "https://api.open-meteo.com/v1/forecast?" + urlencode(parametros)

# Consulta la API y lee la respuesta
with urlopen(url, timeout=15) as respuesta:
    datos = json.loads(respuesta.read().decode("utf-8"))

# Extrae las fechas y las temperaturas máximas
fechas = datos["daily"]["time"]
temperaturas = datos["daily"]["temperature_2m_max"]


# Abre el CSV para escribir los resultados
with open("prueba4/datos_refrigeracion.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)

    # Escribe los nombres de las columnas
    escritor.writerow([
        "Día",
        "Temperatura máxima (°C)",
        "Consumo de refrigeración (kWh)"
    ])

    # Calcula y guarda los datos de cada día
    for fecha, temperatura in zip(fechas, temperaturas):
        consumo = round(calcular_consumo(temperatura), 2)

        escritor.writerow([fecha, temperatura, consumo])

        # Muestra los resultados en la terminal
        print("Día:", fecha)
        print("Temperatura máxima:", temperatura, "°C")
        print("Consumo de refrigeración:", consumo, "kWh")
        print("-----------------------------")

print("Archivo CSV creado correctamente.")
