# Reproducción desde cero del piloto · 27 de noviembre de 2026

Se clonó el repositorio con Git desde la copia local, con transferencia independiente de objetos. Se creó un entorno virtual vacío con Python 3.12.10 en Windows. El código ejecutado corresponde a [d47dc9c](https://github.com/Mauricio-Avina/riesgo-agroclimatico/commit/d47dc9c17dea0107594571c3b63adf13c7092677). La instalación usó pip y su caché de descargas. Ningún paquete se importó del entorno virtual de trabajo. El origen de los insumos fue la copia de bronce: se copiaron los 98 archivos listados y se verificó cada SHA-256 frente a la última entrada de su ruta en el manifiesto del clon.

| Operación | Tiempo observado |
| --- | ---: |
| Clonar y crear el entorno | 1.42 + 3.30 s |
| Instalar dependencias | 60.97 s |
| Copiar y verificar bronce | 0.73 s |
| Ejecutar actualizar.bat | 54.01 s |
| Ejecutar pytest con cobertura (tiempo de pared) | 7.77 s |

Tiempo acumulado de esas operaciones: 128.19 s, excluidos instalación previa de Python, pausas de preparación y medición de la API. Dentro de actualizar.bat se cronometraron el pipeline (11.14 s), python -m src.models (30.75 s) y la generación de fichas y boletines (11.16 s). Las duraciones se midieron con time.perf_counter y dependen del equipo, los hilos y la caché. Los ficheros revision_modelos.csv, revision_equidad.csv, metricas_modelos.csv, revision_quintiles.csv y pronosticos_prueba.csv coincidieron byte por byte con los entregados.

Para repetir, clonar en una carpeta vacía, ejecutar `py -3.12 -m venv .venv`, instalar con `.venv\Scripts\python -m pip install -r requirements.txt`, restaurar y verificar bronce, y ejecutar `actualizar.bat`. Correr `.venv\Scripts\python -m pytest --cov=src --cov-report=term-missing`. Con la API en ejecución, `.venv\Scripts\python -m scripts.medir_servicio` mide una solicitud de calentamiento más 100 predicciones y 10 simulaciones secuenciales de San José de Iturbide. El ensayo fijó OMP_NUM_THREADS y OPENBLAS_NUM_THREADS a 1 para los procesos medidos. Media de predicción: 7.29 ms (6.20–9.87); simulación: 208.73 ms (207.28–210.06).

La ejecución adicional en la carpeta de trabajo, que contenía cambios locales previos en la integración de datos, también pasó las 23 pruebas y obtuvo 34 % (597 de 1,780 sentencias). El Anexo C documenta el denominador de la revisión reproducida: 596 de 1,779.

[Salida de pytest](pruebas.txt) · [Tiempos con precisión completa](tiempos.json) · [Calidad del producto](calidad_producto.md)
