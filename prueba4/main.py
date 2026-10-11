
import json
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

# Muestra los datos y el consumo de cada día
for fecha, temperatura in zip(fechas, temperaturas):
    consumo = calcular_consumo(temperatura)
    consumo = round(consumo, 2)  # Redondea el consumo a 2 decimales

    print("Día:", fecha)
    print("Temperatura máxima:", temperatura, "°C")
    print("Consumo de refrigeración:", consumo, "kWh")
    print("-----------------------------")
