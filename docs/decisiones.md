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

## D-005 · 26/11/2026 · Unidad de observación y duplicados del SIAP

- **Contexto.** El cierre agrícola identifica el maíz grano con el código 7490000. En primavera-verano, la unidad de análisis es municipio, año agrícola y modalidad.
- **Alternativas.** Conservar las filas originales, sumar desgloses compatibles o descartar una copia cuando se demuestre que está duplicada.
- **Decisión.** Conservar las 2,776 filas que cumplen la delimitación. La comparación de las tres columnas de la llave en los cierres originales devolvió cero duplicados. Si otra edición introduce una repetición, la integración se detiene para identificar su origen.
- **Razón.** Sumar superficies repetidas podría contarlas dos veces. Descartar una fila sin examinarla podría eliminar producción válida. La clave municipal combina dos dígitos de estado y tres de municipio, de modo que 11 y 1 dan `11001`.
- **Consecuencias.** Las 168 combinaciones sin fila en el cierre quedan ausentes. Una cosecha o una pérdida de cero exige un registro que la respalde. La siniestralidad se calcula como hectáreas siniestradas entre sembradas y queda nula si el denominador es cero. [Cobertura por municipio y modalidad](../reports/integracion_2_2_a_2_5.md)

## D-006 · 26/11/2026 · Punto para pedir el clima

- **Contexto.** NASA POWER requiere una coordenada por consulta y el SIAP identifica municipios mediante una clave.
- **Alternativas.** Usar el centroide del polígono o un punto representativo interior.
- **Decisión.** Usar un punto representativo por municipio. Se calculó el área en la proyección equivalente EPSG:6933 y se convirtieron las coordenadas del punto a EPSG:4326 para la consulta.
- **Razón.** En un municipio de geometría irregular el centroide puede caer fuera del polígono. Se verificó que los 64 puntos elegidos quedaran dentro de sus límites.
- **Consecuencias.** Riego y temporal comparten la exposición meteorológica de la misma celda. Se usa la misma cartografía para todo el periodo. La altitud corresponde a la celda y un solo punto representa de forma limitada los contrastes de relieve de la Sierra Gorda. [Cotejo con estaciones del SMN](../reports/cotejo_lluvia_smn.csv)

## D-007 · 26/11/2026 · Año base del INPC

- **Contexto.** Los cierres del SIAP expresan el precio medio rural en pesos corrientes por tonelada y el valor de la producción en pesos corrientes.
- **Alternativas.** Mantener únicamente los montos nominales o expresarlos también en pesos del primer o del último año del periodo.
- **Decisión.** Conservar los montos originales y añadir su equivalente en pesos de 2025. Se multiplica cada importe por el INPC medio de 2025 dividido entre el INPC medio del año de origen. Cada promedio usa los doce meses de la serie nacional 865541.
- **Razón.** El último año completo de la delimitación ofrece una referencia reciente para interpretar los importes del piloto. En 2025 el factor es exactamente 1. [Calculadora del INEGI](https://www.inegi.org.mx/app/indicesdeprecios/CalculadoraInflacion.aspx)
- **Consecuencias.** Las comparaciones monetarias comparten poder adquisitivo de referencia. Un precio ausente en el cierre sigue ausente al convertirlo. Para una predicción dentro del ciclo solo son admisibles datos ya disponibles en la fecha de emisión.

## D-008 · 26/11/2026 · Fechas de siembra y ventanas por etapa

- **Contexto.** Las series diarias requieren fechas de inicio y fin para estimar la exposición de cada etapa. El cierre municipal anual no incluye fechas de siembra por parcela.
- **Alternativas.** Usar una referencia común y desplazable, o construir calendarios por zona, variedad y modalidad cuando existan fechas observadas.
- **Decisión.** Adoptar el 15 de junio como día cero para comparar ambos estados y modalidades. Con extremos inclusivos, las ventanas son siembra del 15 al 21 de junio (días 0–6), desarrollo vegetativo del 22 de junio al 13 de agosto (7–59), floración del 14 de agosto al 2 de septiembre (60–79) y llenado del 3 de septiembre al 7 de octubre (80–114).
- **Razón.** La agenda de Querétaro sitúa la siembra de temporal desde el inicio de las lluvias hasta el 10 de julio en el semiárido (p. 18) y del 15 de mayo al 20 de julio en la Sierra (p. 23). La de Guanajuato distingue fechas límite del 20 de junio, 30 de julio y 15 de julio según región y régimen de temporal (p. 178), y hasta el 15 de junio en punta de riego en el norte (p. 184). Estas páginas sustentan la elección de la fecha de siembra. [INIFAP, Querétaro](../data/bronce/inifap/agenda_Qro_2017.pdf) · [INIFAP, Guanajuato](../data/bronce/inifap/agenda_Gto_2017.pdf)
- **Fundamento de la duración.** Los cortes internos son supuestos del escenario. Como referencias regionales, el híbrido P2327W florece a los 68–70 días y cuatro variedades criollas ensayadas en el norte de Guanajuato florecieron a los 69–78 días y maduraron a los 110–115 días. [Ficha del híbrido](https://www.pioneer.com/mx/hibridos/maiz/bajio/p2327w.html) · [Ensayo de variedades de temporal en Guanajuato](https://www.conafor.gob.mx/biblioteca/memoria_RNIAF_2009.pdf)
- **Consecuencias.** El simulador puede desplazar las ventanas completas. La variedad y las lluvias pueden adelantar o retrasar las etapas reales. Una alerta previa al fin de una etapa solo puede emplear información disponible al emitirla. Las anomalías y estandarizaciones del módulo 3 se ajustarán con los años de entrenamiento.

La racha seca cuenta días seguidos con menos de 1 mm y se interrumpe al alcanzar 1 mm. La helada requiere una mínima inferior a 0 °C y el calor en floración, una máxima superior a 30 °C. Los grados día se calculan acotando cada temperatura entre 10 y 30 °C antes de promediar y restar 10. Un día faltante deja nulos los indicadores que requieren esa medición. [Zhang et al. (2011)](https://doi.org/10.1002/wcc.147) · [McMaster y Wilhelm (1997)](https://doi.org/10.1016/S0168-1923(97)00027-0)

## D-009 · 26/11/2026 · Municipios sin coordenadas o sin marginación

- **Contexto.** Una unión interna podría ocultar municipios del SIAP cuya clave no se encuentre en INEGI o CONAPO.
- **Alternativas.** Excluir las claves sin correspondencia, imputar valores o conservarlas durante el cotejo e investigar cada falta.
- **Decisión.** Hacer una unión izquierda desde las claves del SIAP, contar antes y después y comprobar el indicador de unión y los campos requeridos. La ejecución dio 64 coincidencias en cada cruce, cero municipios sin coordenadas y cero sin índice o grado. Se conservaron los 64 municipios.
- **Razón.** La comprobación distingue una clave sin correspondencia de una fila encontrada con campos vacíos. Si aparece una discrepancia en otro corte, se revisará el catálogo y el archivo de origen antes de publicar el maestro. [Puntos de control](../reports/integracion_2_2_a_2_5.md)
- **Consecuencias.** Ningún registro agrícola necesitó exclusión o imputación por estas dos fuentes. El índice y el grado corresponden a 2020 en todos los años. Describen el contexto de ese corte y su uso predictivo retrospectivo debe respetar la fecha de publicación. [Datos de CONAPO](https://indicemx.github.io/IMx2020/reference/index.html)

## D-010 · 26/11/2026 · Menos del 5 % de faltantes por variable (RF-02)

- **Contexto.** Una variable con poca cobertura puede deteriorar el modelo aunque el promedio de faltantes de toda la tabla sea bajo.
- **Alternativas.** Medir el porcentaje global de celdas vacías o medir cada variable candidata por separado.
- **Decisión.** Aplicar el umbral estricto de RF-02 a cada variable del modelo. El porcentaje es 100 × filas con valor faltante en esa columna / filas evaluadas. Un resultado igual a 5 % ya requiere revisión. [Requisitos](requisitos.md)
- **Razón.** Evaluar por columna hace visible una fuente o una medición especialmente incompleta.
- **Consecuencias.** La mayor proporción observada en oro fue 3 de 2,776 (0.1081 %). Si una variable alcanza el límite, se investigará el origen y se documentará su tratamiento antes de usarla. [Calidad por columna](../reports/calidad_oro.csv)

## D-011 · 26/11/2026 · Diferencia de sensibilidad superior a 10 puntos porcentuales (RNF-03)

- **Contexto.** Un buen resultado agregado puede ocultar pérdidas que el modelo detecta con menor frecuencia en un grupo.
- **Alternativas.** Informar solo la sensibilidad conjunta o comparar grupos dentro de cada dimensión de RNF-03.
- **Decisión.** En los años de prueba se informarán sensibilidad y Brier por modalidad, estado y grado de marginación. Se documentarán la causa investigada y una medida para cada diferencia absoluta de sensibilidad superior a 10 puntos porcentuales entre grupos de la misma dimensión. [Requisitos](requisitos.md)
- **Razón.** La diferencia en puntos porcentuales permite interpretar cuántas pérdidas adicionales de cada cien quedarían sin detectar entre dos grupos comparables.
- **Consecuencias.** Se reportará el número de pérdidas observadas por grupo. Sin casos positivos, la sensibilidad queda sin estimar. Si la evidencia resulta insuficiente para atribuir una causa, se consignará esa limitación y la comprobación pendiente. La medición requiere predicciones de prueba.

## D-012 · 26/11/2026 · Cuatro de cinco participantes usan la pantalla sin ayuda (RF-08)

- **Contexto.** La cooperativa necesita saber si un usuario puede interpretar y usar la consulta municipal de forma autónoma.
- **Alternativas.** Recoger solo una opinión sobre la pantalla u observar a cada participante al realizar la misma tarea.
- **Decisión.** En el piloto, pedir a cinco participantes que consulten un municipio e identifiquen el riesgo y la recomendación. Registrar para cada persona si completó la tarea sin ayuda. Se cumple el criterio con al menos cuatro éxitos. [Requisitos](requisitos.md)
- **Razón.** Un conteo por persona permite distinguir completar la consulta de necesitar orientación para terminarla.
- **Consecuencias.** Se informará el conteo sobre cinco y la dificultad observada. El resultado describirá esa prueba del piloto. La sesión con usuarios está pendiente.

## D-013 · 26/11/2026 · SUS promedio de al menos 68 puntos (RNF-01)

- **Contexto.** Además de observar la tarea de RF-08, interesa conocer cómo perciben los participantes la usabilidad.
- **Alternativas.** Recoger comentarios abiertos como única medida o acompañarlos de una puntuación comparable entre sesiones.
- **Decisión.** Aplicar la System Usability Scale (SUS) a los cinco participantes después de la prueba. Calcular el puntaje individual sobre 100 y su media aritmética. Se cumple el umbral fijado en RNF-01 cuando la media es mayor o igual a 68 puntos. [Requisitos](requisitos.md)
- **Razón.** El requisito fija de antemano un criterio de aceptación para la percepción de uso que complementa el conteo de tareas completadas.
- **Consecuencias.** Se conservarán las cinco puntuaciones y se reportará la media. Un buen SUS no sustituye la comprobación de autonomía de RF-08. La medición está pendiente de la sesión con usuarios.
