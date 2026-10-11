# Prueba 4: Refrigeración y dashboard

## Objetivo

Este proyecto obtiene la previsión de temperaturas máximas para los
próximos siete días en Madrid, calcula una estimación del consumo de
refrigeración y muestra los resultados en un dashboard web con dos
gráficos.

La fórmula solicitada es:

-   Si la temperatura máxima es igual o superior a 25 °C:
    `(temperatura - 25) * 10`.
-   Si la temperatura máxima es inferior a 25 °C: `0 kWh`.

## Estructura del proyecto

Los archivos de esta prueba se encuentran en la carpeta `prueba4/`.

  -----------------------------------------------------------------------
  Archivo                             Función
  ----------------------------------- -----------------------------------
  `main.py`                           Consulta la API meteorológica,
                                      calcula el consumo, muestra los
                                      resultados y genera el CSV.

  `datos_refrigeracion.csv`           Archivo generado por `main.py`.
                                      Guarda una fila por día con la
                                      fecha, la temperatura máxima y el
                                      consumo estimado.

  `dashboard.html`                    Plantilla HTML del dashboard.
                                      Contiene la estructura visual, los
                                      estilos CSS y los dos gráficos de
                                      ECharts. Incluye el marcador
                                      `// DATOS_GENERADOS_AQUI`, donde se
                                      insertan los datos.

  `generar_dashboard.py`              Lee el CSV, prepara las listas de
                                      datos, sustituye el marcador de la
                                      plantilla y guarda el HTML
                                      generado.

  `dashboard_generado.html`           Archivo HTML generado
                                      automáticamente por
                                      `generar_dashboard.py`. Es el que
                                      se abre en el navegador para ver el
                                      dashboard actualizado.
  -----------------------------------------------------------------------

Los archivos `datos_refrigeracion.csv` y `dashboard_generado.html` se
crean al ejecutar los scripts; no es necesario escribirlos manualmente.

## Tecnologías y herramientas utilizadas

-   **Python 3:** lenguaje usado para consultar la API, calcular el
    consumo y generar los archivos.
-   **Open-Meteo API:** proporciona la previsión meteorológica. La
    consulta utiliza las coordenadas de Madrid, la variable
    `temperature_2m_max`, siete días de previsión y la zona horaria
    `Europe/Madrid`.
-   **JSON:** formato en el que la API devuelve los datos.
-   **`urllib`:** módulos estándar de Python utilizados para construir
    la URL y realizar la petición HTTP.
-   **`csv`:** módulo estándar para escribir y leer el archivo CSV.
-   **HTML:** estructura de la página web.
-   **CSS:** estilos y distribución visual del dashboard.
-   **JavaScript:** prepara los datos que usan los gráficos.
-   **Apache ECharts:** biblioteca JavaScript que dibuja el gráfico de
    líneas de temperaturas y el gráfico de barras de consumo.
-   **Git y GitHub:** control de versiones y alojamiento del
    repositorio.

No es necesario instalar paquetes de Python externos para ejecutar los
scripts, porque utilizan módulos incluidos en Python. El navegador
necesita conexión a Internet para cargar ECharts desde su CDN.

## Cómo ejecutar el proyecto

Ejecuta los comandos desde la carpeta raíz del repositorio,
`pruebasPracticas`, no desde dentro de `prueba4`.

### 1. Consultar la API, calcular el consumo y generar el CSV

``` bash
python3 prueba4/main.py
```

El programa muestra los resultados en la terminal y crea o sobrescribe
`prueba4/datos_refrigeracion.csv`.

### 2. Generar el dashboard desde el CSV

``` bash
python3 prueba4/generar_dashboard.py
```

El script lee los datos actuales del CSV y crea o sobrescribe
`prueba4/dashboard_generado.html`.

### 3. Abrir el dashboard

En macOS se puede ejecutar:

``` bash
open prueba4/dashboard_generado.html
```

También se puede abrir `dashboard_generado.html` directamente desde el
explorador de archivos.

## Flujo de datos

1.  `main.py` prepara los parámetros y consulta Open-Meteo.
2.  La respuesta JSON se convierte en datos utilizables por Python.
3.  Se extraen las fechas y temperaturas máximas.
4.  `calcular_consumo()` calcula el consumo de cada día.
5.  `main.py` guarda los datos en `datos_refrigeracion.csv`.
6.  `generar_dashboard.py` lee el CSV y obtiene las tres columnas.
7.  El generador inserta los datos en `dashboard.html` en el lugar del
    marcador.
8.  Se crea `dashboard_generado.html`, que contiene los dos gráficos con
    los datos actuales.

## Actualizar los datos

Para actualizar el dashboard con una nueva consulta meteorológica,
ejecuta primero `main.py` y después `generar_dashboard.py`. El primer
script actualiza el CSV y el segundo genera el HTML a partir de ese CSV.

## Detalles importantes

-   Ejecutar `main.py` desde la raíz del repositorio es importante
    porque la ruta del CSV está definida como
    `prueba4/datos_refrigeracion.csv`.
-   `generar_dashboard.py` usa la ruta de su propio archivo para
    localizar el CSV, la plantilla y el HTML de salida.
-   No se debe borrar ni cambiar el marcador `// DATOS_GENERADOS_AQUI`
    de `dashboard.html`, porque el generador lo necesita para insertar
    las listas de datos.
-   `dashboard.html` es la plantilla y `dashboard_generado.html` es el
    resultado generado. Se mantienen separados para no perder la
    plantilla al actualizar el dashboard.
-   El consumo es una estimación basada en la fórmula del ejercicio; no
    es una medición real de una instalación de refrigeración.
