
import json
from urllib.request import urlopen
from urllib.parse import urlencode


# Calcula el uso estimado de iluminación
def calcular_uso_iluminacion(nubosidad):
    if nubosidad >= 50:
        uso = (nubosidad - 50) * 0.5
    else:
        uso = 0

    return uso



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
