# Apuntes de estudio: Prueba 4 --- Refrigeración y dashboard

Este documento resume los conceptos de Python, API, CSV y ECharts que
aparecen en el proyecto. Está pensado para repasar el código y poder
explicar qué hace cada bloque.

## 1. Importaciones

``` python
import json
import csv
from urllib.request import urlopen
from urllib.parse import urlencode
```

-   `json`: convierte el texto JSON recibido de la API en estructuras
    que Python puede consultar, como diccionarios y listas.
-   `csv`: permite escribir y leer filas de un archivo CSV.
-   `urlopen`: realiza una petición a una URL y permite leer la
    respuesta.
-   `urlencode`: convierte los parámetros de la consulta en un formato
    adecuado para incorporarlos a una URL.

Son módulos de la biblioteca estándar de Python; no hay que instalarlos
por separado.

## 2. Funciones: `def`, parámetros y `return`

``` python
def calcular_consumo(temperatura_maxima):
    if temperatura_maxima >= 25:
        consumo = (temperatura_maxima - 25) * 10
    else:
        consumo = 0

    return consumo
```

-   `def` define una función.
-   `calcular_consumo` es el nombre de la función.
-   `temperatura_maxima` es un parámetro: el valor que recibe la
    función.
-   `if` comprueba una condición.
-   `else` define qué hacer cuando la condición no se cumple.
-   `return` devuelve el resultado al lugar donde se llamó a la función.

Ejemplos:

``` python
calcular_consumo(28)  # Devuelve 30
calcular_consumo(25)  # Devuelve 0
calcular_consumo(20)  # Devuelve 0
```

La función solo calcula el consumo. No consulta Internet, no lee el CSV
y no imprime resultados.

## 3. Diccionarios y parámetros de la API

``` python
parametros = {
    "latitude": 40.4168,
    "longitude": -3.7038,
    "daily": "temperature_2m_max",
    "forecast_days": 7,
    "timezone": "Europe/Madrid"
}
```

Un diccionario guarda pares de clave y valor. Por ejemplo,
`"forecast_days"` es una clave y `7` es su valor.

Estos parámetros indican a Open-Meteo qué ubicación consultar, qué
variable meteorológica devolver, cuántos días solicitar y qué zona
horaria utilizar.

## 4. Construir una URL y consultar la API

``` python
url = "https://api.open-meteo.com/v1/forecast?" + urlencode(parametros)

with urlopen(url, timeout=15) as respuesta:
    datos = json.loads(respuesta.read().decode("utf-8"))
```

-   `urlencode(parametros)` transforma el diccionario en parámetros de
    URL.
-   `urlopen(url, timeout=15)` solicita la información a la API y
    establece un tiempo máximo de espera de 15 segundos.
-   `with` gestiona el recurso y lo cierra automáticamente al salir del
    bloque.
-   `respuesta.read()` lee los bytes de la respuesta.
-   `.decode("utf-8")` convierte esos bytes en texto.
-   `json.loads(...)` interpreta el texto JSON y lo convierte en objetos
    de Python.
-   `datos` contiene la respuesta convertida.

La API es el servicio que proporciona los datos; JSON es el formato en
el que llegan. No son lo mismo.

## 5. Acceder a los datos recibidos

``` python
fechas = datos["daily"]["time"]
temperaturas = datos["daily"]["temperature_2m_max"]
```

`datos` es un diccionario. Primero se accede a la clave `"daily"` y
después a la clave que interesa dentro de ella.

-   `fechas` recibe la lista de fechas.
-   `temperaturas` recibe la lista de temperaturas máximas.

Las listas mantienen el orden, por lo que la fecha de una posición
corresponde a la temperatura de esa misma posición.

## 6. Bucles y `zip()`

``` python
for fecha, temperatura in zip(fechas, temperaturas):
    consumo = round(calcular_consumo(temperatura), 2)
```

-   `for` repite un bloque de código por cada elemento del recorrido.
-   `zip(fechas, temperaturas)` empareja los elementos que ocupan la
    misma posición en ambas listas.
-   En cada vuelta, `fecha` contiene una fecha y `temperatura` contiene
    su temperatura máxima.
-   `calcular_consumo(temperatura)` llama a la función creada antes.
-   `round(resultado, 2)` redondea el resultado a dos decimales para
    presentarlo de forma más clara.

Si las listas contienen siete elementos, el bucle se ejecuta siete
veces.

## 7. Crear y escribir el CSV

``` python
with open(
    "prueba4/datos_refrigeracion.csv",
    "w",
    newline="",
    encoding="utf-8"
) as archivo:
    escritor = csv.writer(archivo)

    escritor.writerow([
        "Día",
        "Temperatura máxima (°C)",
        "Consumo de refrigeración (kWh)"
    ])
```

-   `open()` abre un archivo.
-   El modo `"w"` permite escribir: si el archivo no existe, se crea; si
    ya existe, se sobrescribe.
-   `newline=""` evita problemas con saltos de línea al escribir CSV.
-   `encoding="utf-8"` permite guardar correctamente caracteres como las
    tildes y el símbolo de grados.
-   `as archivo` asigna el archivo abierto a la variable `archivo`.
-   `csv.writer(archivo)` crea un escritor CSV.
-   `writerow([...])` escribe una fila. La primera llamada escribe los
    encabezados.

Dentro del bucle se usa:

``` python
escritor.writerow([fecha, temperatura, consumo])
```

Esto escribe una fila con los datos de un día.

El bloque `with` cierra el archivo automáticamente cuando termina,
incluso si se sale del bloque antes de lo previsto.

## 8. Leer el CSV con `DictReader`

En `generar_dashboard.py`:

``` python
with open(ruta_csv, "r", newline="", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        fechas.append(fila["Día"])
        temperaturas.append(float(fila["Temperatura máxima (°C)"]))
        consumos.append(float(fila["Consumo de refrigeración (kWh)"]))
```

-   El modo `"r"` abre el archivo para leerlo.
-   `csv.DictReader` utiliza los encabezados como claves de cada fila.
-   `fila["Día"]` obtiene la fecha.
-   `float(...)` convierte los valores numéricos, que se leen
    inicialmente como texto, a números decimales.
-   `append()` añade cada dato al final de su lista.

Por ejemplo, la fila `"26.9"` se convierte en el número `26.9` mediante
`float()`.

## 9. Rutas de archivos con `pathlib`

``` python
from pathlib import Path

carpeta = Path(__file__).resolve().parent
ruta_csv = carpeta / "datos_refrigeracion.csv"
```

-   `Path` facilita la construcción de rutas de archivos.
-   `__file__` representa la ruta del script que se está ejecutando.
-   `.resolve()` obtiene una ruta absoluta normalizada.
-   `.parent` obtiene la carpeta que contiene el script.
-   El operador `/` une la carpeta y el nombre del archivo para formar
    una ruta.

Esto permite que `generar_dashboard.py` encuentre el CSV y el HTML en la
misma carpeta que el propio script, aunque se ejecute desde otra
ubicación.

## 10. Convertir listas de Python a JavaScript

``` python
datos_html = (
    "const fechas = " + json.dumps(fechas, ensure_ascii=False) + ";\n"
    "        const temperaturas = " + json.dumps(temperaturas) + ";\n"
    "        const consumos = " + json.dumps(consumos) + ";"
)
```

-   `json.dumps(lista)` convierte una lista de Python en texto con
    sintaxis JSON, compatible con los valores de un array de JavaScript.
-   `ensure_ascii=False` permite conservar caracteres Unicode en vez de
    convertirlos en secuencias escapadas.
-   `"\n"` introduce un salto de línea.
-   `+` concatena las cadenas de texto.

El resultado contiene declaraciones como:

``` javascript
const fechas = ["2026-10-11", "2026-10-12"];
const temperaturas = [23.3, 24.4];
const consumos = [0, 0];
```

Los datos del ejemplo son ilustrativos; los valores reales se obtienen
del CSV.

## 11. Plantilla HTML y `replace()`

``` python
with open(ruta_html, "r", encoding="utf-8") as archivo:
    contenido_html = archivo.read()

marcador = "// DATOS_GENERADOS_AQUI"

contenido_html = contenido_html.replace(marcador, datos_html)
```

-   `read()` lee todo el contenido del HTML como texto.
-   `marcador` contiene la cadena exacta que debe buscarse en la
    plantilla.
-   `replace(marcador, datos_html)` sustituye el marcador por las
    declaraciones de JavaScript generadas desde el CSV.

El marcador debe coincidir exactamente, incluidos los espacios. Si el
texto de la plantilla no coincide con el que busca Python, el script
genera un error para avisar de que no puede insertar los datos.

Después se guarda el resultado:

``` python
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    archivo.write(contenido_html)
```

`write()` escribe el HTML completo en el archivo de salida.

La plantilla `dashboard.html` se conserva y el resultado se guarda en
`dashboard_generado.html`.

## 12. HTML, CSS y JavaScript

### HTML

Define la estructura de la página y los contenedores donde aparecerán
los gráficos:

``` html
<div id="graficoTemperaturas" class="grafico"></div>
<div id="graficoConsumo" class="grafico"></div>
```

El atributo `id` permite localizar cada contenedor desde JavaScript.

### CSS

Controla el aspecto visual: fuente, márgenes, fondo, altura de los
gráficos y otros estilos.

### JavaScript y ECharts

``` javascript
const graficoTemperaturas = echarts.init(
    document.getElementById("graficoTemperaturas")
);
```

-   `document.getElementById(...)` busca el contenedor HTML.
-   `echarts.init(...)` inicializa un gráfico dentro de ese contenedor.
-   `setOption({...})` define el título, los ejes y la serie de datos.
-   `type: "line"` crea un gráfico de líneas.
-   `type: "bar"` crea un gráfico de barras.
-   `xAxis` define el eje horizontal, que usa las fechas.
-   `yAxis` define el eje vertical, que representa la temperatura o el
    consumo.
-   `series` contiene el tipo de gráfico y los valores que se dibujan.
-   `tooltip: {}` habilita la información emergente al interactuar con
    los datos.

El evento `resize` redimensiona los gráficos cuando cambia el tamaño de
la ventana.

## 13. Orden correcto de ejecución

Ejecuta estos comandos desde la raíz de `pruebasPracticas`:

``` bash
python3 prueba4/main.py
python3 prueba4/generar_dashboard.py
open prueba4/dashboard_generado.html
```

1.  El primer comando consulta la API y actualiza el CSV.
2.  El segundo lee el CSV y genera el HTML.
3.  El tercero abre el dashboard en el navegador.

Si solo ejecutas el generador, este utilizará el CSV que ya exista; no
consulta la API por su cuenta.

## 14. Conceptos clave para explicar el proyecto

-   **Función:** bloque reutilizable de código que puede recibir
    parámetros y devolver un resultado.
-   **Condicional:** permite ejecutar instrucciones distintas según una
    condición.
-   **Bucle:** repite instrucciones para procesar varios elementos.
-   **Lista:** colección ordenada de elementos.
-   **Diccionario:** colección de pares clave-valor.
-   **API:** interfaz que permite solicitar datos a otro servicio.
-   **JSON:** formato de intercambio de datos.
-   **CSV:** archivo de texto que organiza los datos en filas y
    columnas.
-   **Plantilla:** archivo base que conserva la estructura y recibe
    datos variables.
-   **Automatización:** ejecución de un proceso sin tener que editar
    manualmente los datos en cada actualización.

## 15. Errores que conviene recordar

-   **`No such file or directory`:** comprueba la carpeta actual y la
    ruta del archivo. Si estás dentro de `prueba4`, usa
    `python3 main.py`; si estás en la raíz del repositorio, usa
    `python3 prueba4/main.py`.
-   **No se encuentra el marcador:** comprueba que `dashboard.html`
    contiene exactamente `// DATOS_GENERADOS_AQUI`.
-   **No aparece el CSV:** comprueba que has guardado el código
    actualizado y ejecutado `main.py`.
-   **Los gráficos no se ven:** verifica la conexión a Internet, porque
    ECharts se carga desde una CDN externa.
-   **Los datos del dashboard están desactualizados:** ejecuta primero
    `main.py` y luego `generar_dashboard.py`.
