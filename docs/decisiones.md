D-000 · fecha · título de la decisión
Contexto: qué necesitaba resolver
Alternativas: qué otras opciones consideré
Decisión: qué elegí
Por qué: el criterio, con fuente si la hay
Consecuencias: qué gano y qué limito

## D-001 · 25/11/2026 · Github dos cuentas en el mismo windows
- Contexto: Tenía dos cuentas en la misma computadora y no me dejaba hacer git push de la forma correcta
- Alternativas: Eliminar mi otra cuenta para que la creación fuera completamente limpia
- Decisión: Elegí que las dos cuentas comvivieran al mismo tiempo para que de esta manera pueda seguir trabajando en mis otros proyectos
- Por qué: Me permite seguir trabajando en mis otros proyectos con mi otra cuenta
Consecuencias: Facilidad de trabajo y me limitó especificidad de que cuenta estoy usando

## D-002 · 25/11/2026 · Empezar desde cero un proyecto que ya se había hecho
- Contexto: Anteriormente ya había realizado este proyecto pero no me sentía 100% convencido de el
- Alternativas: Corregir o reutilizar codigo del proyecto anterior
- Decisión: Elegí que realizar el proyecto desde cero
- Por qué: No estaba claro y no era reproducible
Consecuencias: Más tiempo invertido y una tabla de tiempos más estricta

## D-003 · 25/11/2026 · Decisión de estado de interés de prueba piloto
- Contexto: Comparé Guanajuato, Querétaro, Michoacán y Jalisco con datos de maíz grano del ciclo primavera-verano de 2023 a 2025, en riego y temporal. Esta comparación de tres años sirve para elegir el piloto; el periodo propuesto para entrenar y evaluar el modelo es 2003–2025.
- Alternativas: Realizar el piloto en Jalisco, Michoacán o Guanajuato.
- Decisión: Elegí Querétaro para la prueba piloto.
- Por qué: En la comparación, sembró en promedio 75,383.86 ha anuales de maíz; el 70.91 % de su superficie sembrada correspondió a temporal y el 13.63 % presentó pérdida completa, la proporción más alta de los cuatro estados. Hubo siniestros en los tres años y sus 18 municipios hacen viable la operación inicial. Las cifras, sus denominadores y la fuente se detallan en [delimitación](delimitacion.md).
- Consecuencias: El piloto, la interfaz, el boletín y la evaluación de adopción se concentran en Querétaro; sus resultados de uso no se pueden generalizar automáticamente a otros estados. La superficie siniestrada puede incluir causas distintas del clima. El alcance de los datos de entrenamiento se decide por separado en D-004.

## D-004 · 26/11/2026 · Región de datos para el modelo
- Contexto: Tres años de comparación no bastan para entrenar y evaluar un modelo; usar solo los 18 municipios de Querétaro limita el número de observaciones y de pérdidas registradas.
- Alternativas: Entrenar únicamente con Querétaro o incluir también Guanajuato.
- Decisión: Usar datos municipales de Querétaro y Guanajuato para 2003–2025, ciclo primavera-verano y modalidades de riego y temporal. El piloto y la evaluación de adopción permanecen en Querétaro.
- Por qué: Los 64 municipios de ambos estados ofrecen hasta 2,944 combinaciones teóricas de municipio, año y modalidad (64 × 23 × 2), frente a 828 para Querétaro. No son filas garantizadas: su disponibilidad, calidad y número de casos de pérdida deben comprobarse en los datos.
- Consecuencias: Aumentan la cobertura potencial y el trabajo de integración y validación. La evaluación debe separar los años de entrenamiento y prueba, informar el desempeño por estado y modalidad, y declarar las limitaciones por registros faltantes y por el número de pérdidas. Los resultados no se extrapolan sin evaluación a otras regiones.
