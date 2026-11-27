A-000 · fecha · título de aprendizaje
Contexto: qué hice
Aprendizaje: qué aprendí
Costo: qué me constó

## A-001 · 25/11/2026 · Estructura de un proyecto
- Contexto: Estructuré un proyecto en python desde cero y a la par lo alinee con Zotero y con Github para que este proyecto tenga reproducibilidad.
- Aprendizaje: Aprendí los pasos que un proyecto necesita para que sea considerado que tiene reprodicibilidad y sea confiable para cualquier persona que lo consulte
- Costo: Aprender la estructura básica de un proyecto python para una interfaz que haga ETL y consultas de datos, subir este proyecto a github entendiendo los comandos y actualizaciones que necesita cada que se hace un cambio.

## A-002 · 25/11/2026 · Codificación de requirements.txt
- Contexto: Creé el archivo requirements.txt para documentar e instalar las librerías del proyecto.
- Aprendizaje: Aprendí que en Windows PowerShell la redirección con `>` puede guardar el archivo en UTF-16, lo que provoca que herramientas como pip no lo interpreten correctamente. Para controlar la codificación puedo usar `Out-File -Encoding utf8` y generar el archivo en UTF-8.
- Costo: Identificar que el problema estaba en la codificación y volver a guardar el archivo para que se pudiera leer correctamente.

## A-003 · 27/11/2026 · Clasificación municipal (paso 3.1)

El apartado 2.5 enlaza las cuatro familias de clasificación con la comparación de cinco alternativas, incluida la climatología. Mantener los municipios de cada año en el mismo bloque reproduce el uso previsto del aviso. La precisión promedio permite interpretar el orden de los avisos en relación con la prevalencia del bloque. La ficha de Saito y Rehmsmeier acompaña ahora a las métricas de clasificación.

## A-004 · 27/11/2026 · Calibración y costo del aviso (paso 3.2)

El apartado 2.6 desarrolla el Brier binario, la habilidad respecto de la climatología y el umbral económico C/L. Comparar la calibración requiere conservar ambos pronósticos para las mismas filas. Los costos y rendimientos del escenario de Sinaloa quedan identificados en las fichas de 2.6, junto al antecedente del uso de trayectorias meteorológicas.

## A-005 · 27/11/2026 · Explicación y errores por grupo (paso 3.3)

El apartado 2.7 distingue la escala del árbol explicada por SHAP de la probabilidad calibrada que recibe el productor. Para leer la igualdad de oportunidades se presentan las pérdidas de cada grupo junto con la sensibilidad. Esto permite detectar tanto evidencia escasa como un umbral que deja a todos los grupos sin aciertos.
