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

Después de generar la capa oro y los modelos, ejecuta `uvicorn src.api.main:app` desde la raíz del repositorio. Abre [la documentación interactiva local](http://127.0.0.1:8000/docs) para consultar salud, municipios, predicción y explicación. El ejemplo corresponde a San José de Iturbide, temporal, en 2023. Selecciona `siembra` para ver la dispersión entre años análogos o `llenado` para consultar la temporada observada.

Ejecuta `python -m unittest discover -s tests` para verificar el contrato y la coincidencia con el modelo. El comando `python -m src.api.control_siembra` reproduce el [contraste de los 605 avisos con solo siembra](reports/control_api_siembra.csv) frente a la referencia municipal fijada al inicio de la prueba.
