print("Prueba 4: Refrigeración y dashboard")

temperatura_maxima = 20

if temperatura_maxima >= 25:
    consumo = (temperatura_maxima - 25) * 10
else:
    consumo = 0

print("Temperatura máxima:", temperatura_maxima, "°C")
print("Consumo de refrigeración:", consumo, "kWh")