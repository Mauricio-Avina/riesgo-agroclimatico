Resumen:
Este proyecto busca generar una plataforma computacional de gestión predictiva de 
riesgos climáticos para agricultura sostenible

Cómo instalarlo:
1. Instala python 3.12
2. Clona el repositorio con git clone. (https://github.com/Mauricio-Avina/riesgo-agroclimatico)
3. Crea y activa el entorno
4. E instala las librerías con pip install -r requierements.txt

Cómo está organizado:
riesgo-agroclimatico/
├── data/  #Aquí estarán los datos
│   ├── bronce/ # Datos raw 
│   ├── plata/  # Datos ETL
│   └── oro/    # Datos listos para el usuario
├── notebooks/  # Libretas de análisis
├── src/        # Fuentes y código
│   ├── etl/    # Código ETL
│   ├── features/ 
│   ├── models/ # Modelos entrenados
│   ├── api/    # Apis de conexión a las fuentes
│   └── app/    # Script de app
├── tests/      # Pruebas
├── reports/figures/ #Reportes y figuras ilustrativas para el reporte
├── docs/       # Documentos
├── requirements.txt # Librerías a instalar
└── README.md   # Acerca del proyecto