
import json
import csv
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


# Abre el CSV para escribir los resultados
with open("prueba5/datos_iluminacion.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)

    # Escribe los nombres de las columnas
    escritor.writerow([
        "Día",
        "Nubosidad media (%)",
        "Uso estimado de iluminación (kWh)"
    ])

    # Calcula y guarda los datos de cada día
    for fecha, nubosidad in zip(fechas, nubosidades):
        uso = round(calcular_uso_iluminacion(nubosidad), 2)

        escritor.writerow([fecha, nubosidad, uso])

        # Muestra los resultados en la terminal
        print("Día:", fecha)
        print("Nubosidad media:", nubosidad, "%")
        print("Uso estimado de iluminación:", uso, "kWh")
        print("-----------------------------")

print("Archivo CSV creado correctamente.")
