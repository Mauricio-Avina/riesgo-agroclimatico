Resumen:
Este proyecto busca generar una plataforma computacional de gestión predictiva de 
riesgos climáticos para agricultura sostenible

Cómo instalarlo:
1. Instala python 3.12
2. Clona el repositorio y entra en su carpeta:
   ```powershell
   git clone https://github.com/Mauricio-Avina/riesgo-agroclimatico.git
   cd riesgo-agroclimatico
   ```
3. Crea y activa el entorno en PowerShell:
   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Instala las librerías con `pip install -r requirements.txt`.

## Cómo correrlo

`python -m src.pipeline`

Cómo está organizado:
riesgo-agroclimatico/
├── data/  #Aquí estarán los datos
│   ├── bronce/ # Datos raw 
│   ├── plata/  # Datos ETL
│   └── oro/    # Datos unidos y listos para entrenar el modelo
├── notebooks/  # Libretas de análisis
├── src/        # Fuentes y código
│   ├── etl/    # Extracción de las fuentes, transformación y carga de datos
│   ├── features/ # Cálculo de variables, como lluvia por etapa y grados día
│   ├── models/ # Código para entrenar y evaluar modelos; los modelos entrenados son archivos aparte
│   ├── api/    # Servicio que entrega las predicciones a la interfaz
│   └── app/    # Script de app
├── tests/      # Pruebas
├── reports/figures/ #Reportes y figuras ilustrativas para el reporte
├── docs/       # Documentos
├── requirements.txt # Librerías a instalar
└── README.md   # Acerca del proyecto

## Modelos de pérdida municipal

Con el entorno del proyecto activo y las capas de datos publicadas, ejecutar `python -m src.models`. El módulo entrena y calibra cinco alternativas en dos horizontes, guarda los ajustes en `artefactos/` y publica las métricas y figuras en `reports/`. Para comprobar la partición, ejecutar `python -m unittest discover -s tests -p test_particion.py`. Los archivos de búsqueda identifican al ganador de cada horizonte. La AP es la precisión promedio. En los reportes de evaluación, los intervalos por año individual quedan vacíos porque solo se remuestrean años completos.

[Decisiones de modelado](docs/decisiones.md#d-019--27112026--partición-temporal) · [Fichas en Zotero](docs/fichas_modelos.md) · [Pronósticos de prueba](reports/pronosticos_prueba.csv)

## Servicio de consulta municipal

Después de generar la capa oro y los modelos, ejecuta `uvicorn src.api.main:app` desde la raíz del repositorio. Abre [la documentación interactiva local](http://127.0.0.1:8000/docs) para consultar salud, municipios, predicción y explicación. El ejemplo corresponde a San José de Iturbide, temporal, en 2023. En `siembra` se devuelve la climatología municipal calibrada con Platt (base 2003–2017 y calibración 2018–2020 para la prueba). Desde `vegetativo` se usa el boosting restringido. El rango P10–P90 solo existe al consultar el modelo meteorológico. Con `llenado` la temporada queda observada. Las probabilidades se devuelven a cuatro decimales y el nivel se calcula antes de redondear.

Ejecuta `python -m unittest discover -s tests` para verificar el contrato y la coincidencia con el modelo. El comando `python -m src.api.control_siembra` reproduce las [métricas de las cuatro etapas](reports/metricas_por_etapa.csv) sobre los mismos 605 casos para el modelo original, el restringido, la climatología y la política de la API. La columna `api` conserva precisión completa y `api_publicada` reproduce las probabilidades transmitidas con cuatro decimales. El control publica también el [conteo de avisos y cambios de rojo a amarillo](reports/alertas_siembra.csv). El entrenamiento completo incluye la [revisión RF-07](reports/revision_direcciones.csv) y la [auditoría al amarillo](reports/revision_equidad.csv).

## Aplicación de la cooperativa

En Windows, abre `iniciar.bat` en la raíz del proyecto para consultar la aplicación en el navegador local. El modo Productor permite buscar el municipio y descargar el boletín de llenado. En Técnico puedes revisar el historial, ver la explicación completa y comparar fechas y modalidades en tres climas históricos. La demostración reconstruye el ciclo 2025.

Con las dependencias de `requirements.txt` en el entorno `.venv`, `actualizar.bat` ejecuta la integración de datos, entrena los modelos y regenera las fichas y los boletines. Cierra y vuelve a abrir la aplicación para cargar los modelos nuevos. Con los datos y los modelos ya instalados, `python -m src.app.precalcular` regenera solo la distribución local.

[Usuarios y protocolo de prueba](docs/usuarios.md) · [Evidencia de operación local](reports/evidencias_dia8/verificacion.md) · [Boletín de ejemplo](reports/boletin_ejemplo.pdf)
