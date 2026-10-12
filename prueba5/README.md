# Prueba 5 - Iluminación y dashboard

Proyecto de prácticas de DAM que consulta la previsión meteorológica de Open-Meteo para Madrid, calcula un uso estimado de iluminación según la nubosidad media diaria y muestra los resultados en un dashboard web.

## Objetivo

Obtener la nubosidad media de los próximos siete días, calcular el uso estimado de iluminación y representar ambos datos mediante dos gráficos.

La fórmula aplicada es:

- Si la nubosidad es igual o superior al 50 %: `(nubosidad - 50) * 0.5`.
- Si la nubosidad es inferior al 50 %: `0 kWh`.

## Estructura del proyecto

- `prueba5/probar_api.py`: prueba inicial de la conexión con Open-Meteo. Consulta y muestra las fechas y la nubosidad media.
- `prueba5/main.py`: consulta la API, calcula el uso estimado de iluminación, muestra los resultados y genera el CSV.
- `prueba5/datos_iluminacion.csv`: archivo generado por `main.py`, con las columnas Día, Nubosidad media (%) y Uso estimado de iluminación (kWh).
- `prueba5/dashboard.html`: plantilla HTML con los contenedores de los dos gráficos y un marcador que se sustituye automáticamente.
- `prueba5/generar_dashboard.py`: lee el CSV, prepara los datos para JavaScript, configura los gráficos y genera el HTML final.
- `prueba5/dashboard_generado.html`: dashboard generado automáticamente; no se edita manualmente.

## Tecnologías utilizadas

- Python 3 y su biblioteca estándar: `json`, `csv`, `urllib` y `pathlib`.
- API de previsión meteorológica de Open-Meteo.
- HTML y CSS para la página web.
- JavaScript y Apache ECharts para los gráficos.
- Git y GitHub para el control de versiones.

No es necesario instalar paquetes de Python adicionales. El navegador necesita conexión a Internet para cargar ECharts desde su CDN.

## Cómo ejecutar el proyecto

Ejecuta los comandos desde la carpeta raíz del repositorio `pruebasPracticas`.

1. (Opcional) Probar la consulta a la API:

   ```bash
   python3 prueba5/probar_api.py
   ```

2. Consultar la API y generar el CSV:

   ```bash
   python3 prueba5/main.py
   ```

3. Generar el dashboard a partir del CSV:

   ```bash
   python3 prueba5/generar_dashboard.py
   ```

4. Abrir el dashboard:

   ```bash
   open prueba5/dashboard_generado.html
   ```

## Flujo de datos

1. `main.py` construye la URL de Open-Meteo y solicita la variable diaria `cloud_cover_mean`.
2. La respuesta JSON proporciona las fechas y la nubosidad media.
3. La función `calcular_uso_iluminacion()` aplica la fórmula de la práctica.
4. Los resultados se guardan en `datos_iluminacion.csv`.
5. `generar_dashboard.py` lee el CSV y convierte las listas a JSON para utilizarlas en JavaScript.
6. El script sustituye el marcador `// DATOS_GENERADOS_AQUI` de la plantilla y guarda `dashboard_generado.html`.
7. El navegador muestra un gráfico de líneas de nubosidad y un gráfico de barras de uso estimado de iluminación. Ambos utilizan las mismas fechas en el eje horizontal.

## Actualizar los datos

Para actualizar la previsión, vuelve a ejecutar `main.py` y después `generar_dashboard.py`. El CSV y el dashboard se regeneran con los datos disponibles en ese momento.

No es necesario modificar manualmente `dashboard.html` para actualizar los datos.

## Notas

- Los valores meteorológicos corresponden a la previsión disponible en el momento de la consulta y pueden cambiar.
- `main.py` utiliza una ruta relativa para guardar el CSV; por eso se recomienda ejecutar los comandos desde la raíz del repositorio.
- Si el dashboard no muestra los gráficos, comprueba la conexión a Internet y que `dashboard_generado.html` se haya generado correctamente.
