# Apuntes de estudio - Prueba 5: Iluminación

Estos apuntes explican los conceptos principales del código para poder entenderlo y explicarlo en clase.

## 1. Imports

```python
import json
import csv
from urllib.request import urlopen
from urllib.parse import urlencode
```

- `json`: convierte el texto JSON recibido de la API en estructuras de Python.
- `csv`: permite leer y escribir archivos CSV.
- `urlopen`: realiza la petición HTTP a la API.
- `urlencode`: convierte un diccionario de parámetros en una cadena válida para una URL.

En `generar_dashboard.py` también se utiliza `pathlib.Path` para construir rutas de archivos de forma cómoda.

## 2. Diccionarios y parámetros de la API

```python
parametros = {
    "latitude": 40.4168,
    "longitude": -3.7038,
    "daily": "cloud_cover_mean",
    "forecast_days": 7,
    "timezone": "Europe/Madrid"
}
```

Un diccionario almacena parejas de clave y valor. En este caso, indica a Open-Meteo las coordenadas de Madrid, la variable solicitada, el número de días y la zona horaria.

`cloud_cover_mean` representa la nubosidad media diaria, expresada en porcentaje.

## 3. Construir la URL y consultar la API

```python
url = "https://api.open-meteo.com/v1/forecast?" + urlencode(parametros)

with urlopen(url, timeout=15) as respuesta:
    datos = json.loads(respuesta.read().decode("utf-8"))
```

- `urlencode(parametros)` transforma los parámetros en texto para añadirlos a la URL.
- `urlopen(..., timeout=15)` solicita la información y establece un tiempo máximo de espera.
- `with` gestiona la apertura y el cierre del recurso.
- `respuesta.read()` lee el contenido recibido.
- `decode("utf-8")` convierte los bytes en texto.
- `json.loads(...)` transforma el JSON en datos de Python, normalmente diccionarios y listas.

La consulta necesita conexión a Internet.

## 4. Acceder a los datos recibidos

```python
fechas = datos["daily"]["time"]
nubosidades = datos["daily"]["cloud_cover_mean"]
```

Se accede a valores anidados de un diccionario mediante sus claves. `fechas` contiene las fechas y `nubosidades` contiene el valor de nubosidad asociado a cada día.

## 5. Funciones, parámetros, `if`, `else` y `return`

```python
def calcular_uso_iluminacion(nubosidad):
    if nubosidad >= 50:
        uso = (nubosidad - 50) * 0.5
    else:
        uso = 0

    return uso
```

- `def` define una función.
- `nubosidad` es el parámetro: el dato que recibe la función.
- `if` comprueba una condición.
- `else` indica qué hacer si la condición no se cumple.
- `return` devuelve el resultado al lugar desde el que se llamó a la función.

Ejemplos:
- Con un 30 % de nubosidad, el uso estimado es `0 kWh`.
- Con un 70 %, el cálculo es `(70 - 50) * 0.5 = 10 kWh`.
- Con un 90 %, el cálculo es `(90 - 50) * 0.5 = 20 kWh`.

## 6. Escribir el CSV

```python
with open("prueba5/datos_iluminacion.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Día", "Nubosidad media (%)", "Uso estimado de iluminación (kWh)"])
```

- `open(..., "w")` crea el archivo o sobrescribe su contenido si ya existe.
- `newline=""` evita líneas en blanco adicionales en algunos entornos.
- `encoding="utf-8"` permite guardar caracteres como tildes.
- `csv.writer()` crea un escritor de filas.
- `writerow()` escribe una fila en el archivo.

El programa escribe primero los encabezados y después una fila por cada día.

## 7. Bucles, `zip()` y redondeo

```python
for fecha, nubosidad in zip(fechas, nubosidades):
    uso = round(calcular_uso_iluminacion(nubosidad), 2)
    escritor.writerow([fecha, nubosidad, uso])
```

- `for` repite las instrucciones para cada pareja de valores.
- `zip(fechas, nubosidades)` recorre ambas listas a la vez y relaciona cada fecha con su nubosidad.
- `calcular_uso_iluminacion(nubosidad)` obtiene el uso estimado.
- `round(..., 2)` redondea el resultado a dos decimales.
- `writerow()` guarda los tres valores en el CSV.

## 8. Leer el CSV con `DictReader`

En `generar_dashboard.py`:

```python
with open(ruta_csv, "r", newline="", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    filas = list(lector)
```

`csv.DictReader()` interpreta la primera fila como encabezados y permite acceder a los valores por el nombre de columna, por ejemplo `fila["Día"]`. `list(lector)` guarda las filas para poder recorrerlas después.

Las columnas numéricas se convierten a `float` para utilizarlas como números en los gráficos.

## 9. Rutas con `pathlib`

```python
carpeta = Path(__file__).resolve().parent
ruta_csv = carpeta / "datos_iluminacion.csv"
```

- `__file__` identifica el archivo Python actual.
- `resolve()` obtiene una ruta absoluta.
- `parent` obtiene la carpeta que contiene el script.
- El operador `/` de `Path` combina partes de una ruta.

Así, `generar_dashboard.py` encuentra sus archivos dentro de `prueba5`, aunque se ejecute desde la raíz del repositorio.

**Importante:** en cambio, la ruta del CSV escrita en `main.py` es relativa a la carpeta actual de la terminal. Por eso se ejecuta `python3 prueba5/main.py` desde la raíz del repositorio.

## 10. Convertir datos de Python a JavaScript con JSON

```python
datos_fechas = json.dumps(fechas, ensure_ascii=False)
datos_nubosidades = json.dumps(nubosidades)
datos_usos = json.dumps(usos)
```

`json.dumps()` convierte listas de Python en texto JSON. Ese formato puede utilizarse directamente en JavaScript. `ensure_ascii=False` conserva los caracteres Unicode en lugar de convertirlos en secuencias escapadas.

## 11. Plantilla HTML y sustitución del marcador

La plantilla `dashboard.html` contiene:

```javascript
// DATOS_GENERADOS_AQUI
```

El script lee la plantilla y sustituye ese texto por el JavaScript que contiene los datos y la configuración de los gráficos:

```python
html_final = plantilla.replace("// DATOS_GENERADOS_AQUI", codigo_graficos)
```

Después guarda el resultado en `dashboard_generado.html`. La plantilla original se conserva, por lo que no hace falta editarla para cada actualización.

## 12. HTML, CSS, JavaScript y ECharts

- **HTML** define la estructura de la página, el título y los dos contenedores de gráficos.
- **CSS** controla el diseño visual: fondo, tipografía, márgenes y dimensiones.
- **JavaScript** prepara los datos y configura el comportamiento de los gráficos.
- **ECharts** dibuja los gráficos en el navegador.

`echarts.init(...)` inicializa un gráfico dentro de un elemento HTML y `setOption(...)` define sus títulos, ejes, series y datos.

El primer gráfico es de líneas y representa la nubosidad. El segundo es de barras y representa el uso estimado de iluminación. Ambos utilizan la misma lista de fechas en el eje X.

ECharts se carga desde un CDN, por lo que el navegador necesita conexión a Internet.

## 13. Orden de ejecución

Ejecuta los comandos desde la carpeta raíz `pruebasPracticas`:

```bash
python3 prueba5/probar_api.py
python3 prueba5/main.py
python3 prueba5/generar_dashboard.py
open prueba5/dashboard_generado.html
```

1. `probar_api.py` comprueba la consulta a la API.
2. `main.py` obtiene los datos y genera el CSV.
3. `generar_dashboard.py` lee el CSV y crea el HTML final.
4. `open` abre el dashboard en el navegador.

## 14. Errores frecuentes

- **No se encuentra el archivo Python:** comprueba la carpeta actual y la ruta del archivo.
- **No se encuentra el CSV:** ejecuta primero `main.py` desde la raíz del repositorio.
- **La API no responde:** revisa la conexión a Internet y vuelve a intentarlo.
- **El dashboard está vacío o no muestra gráficos:** genera de nuevo el HTML y comprueba que el navegador tenga conexión a Internet para cargar ECharts.
- **Los datos no se actualizan:** ejecuta primero `main.py` y después `generar_dashboard.py`.
