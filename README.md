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
