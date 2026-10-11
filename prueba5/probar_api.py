
import json
from urllib.request import urlopen
from urllib.parse import urlencode


# Parámetros de la consulta a la API
parametros = {
    "latitude": 40.4168,
    "longitude": -3.7038,
    "daily": "cloud_cover_mean",
    "forecast_days": 7,
    "timezone": "Europe/Madrid"
}

# Construye la URL con los parámetros
url = "https://api.open-meteo.com/v1/forecast?" + urlencode(parametros)

# Consulta la API y lee la respuesta
with urlopen(url, timeout=15) as respuesta:
    datos = json.loads(respuesta.read().decode("utf-8"))

# Extrae las fechas y la nubosidad media
fechas = datos["daily"]["time"]
nubosidades = datos["daily"]["cloud_cover_mean"]

# Muestra los resultados
for fecha, nubosidad in zip(fechas, nubosidades):
    print("Día:", fecha)
    print("Nubosidad media:", nubosidad, "%")
    print("-----------------------------")
