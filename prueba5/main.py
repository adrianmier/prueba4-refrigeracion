
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
