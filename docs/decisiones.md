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

## D-014 · 26/11/2026 · Evento operativo de pérdida

**Contexto y alternativas.** Se compararon cortes estrictos de 0, 10, 25 y 50 % de superficie siniestrada. **Decisión.** Definir el evento como pérdida total en más de una décima de la superficie sembrada del municipio, año y modalidad. **Razón.** Para priorizar la revisión territorial, esta magnitud distingue una afectación extensa de un siniestro localizado. Con 25 o 50 % se omitirían pérdidas superiores a una décima que ameritan verificación temprana. Es un criterio de diseño que se contrastará con la cooperativa. **Consecuencias.** Hay 594/2,776 eventos (21.40 %), 76/1,306 en riego (5.82 %) y 518/1,470 en temporal (35.24 %). El corte define el daño observado; el umbral de probabilidad para emitir una alerta se estimará después. [Comparación de cortes](../reports/umbrales_3_3.csv)

## D-015 · 26/11/2026 · Validación de las tablas publicadas

**Contexto y alternativas.** Los controles dispersos comprobaban partes de cada transformación. **Decisión.** Declarar en Pandera los contratos de las cinco tablas de plata y de oro: columnas requeridas, claves de cinco dígitos, unicidad, dominios, superficies, relaciones térmicas y calendario diario. **Razón.** Un contrato común permite validar archivos ya publicados y rechazar datos de prueba inválidos. **Consecuencias.** Las pruebas de procedencia, calendario mensual, pertenencia espacial y cardinalidad de cada unión siguen junto a la operación que les da sentido. La ejecución publica el reporte después de validar los seis archivos. [Reporte](../reports/calidad.csv)

## D-016 · 26/11/2026 · Publicación oficial de marginación

**Contexto y alternativas.** La primera integración utilizó la copia del repositorio IndiceMx. **Decisión.** Usar la hoja IMM_2020 del libro distribuido por CONAPO y conservar ambas descargas en bronce. **Razón.** La publicación institucional identifica al productor y la edición. **Consecuencias.** En el cruce por clave coincidieron 64 de 64 índices (diferencia absoluta máxima 0) y los 64 grados. Se conserva la limitación temporal del corte 2020. [Publicación de CONAPO](https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372)

## D-017 · 26/11/2026 · Siembra de referencia para riego

**Contexto y alternativas.** Se consideró una fecha exclusiva para riego frente al escenario común de D-008. **Decisión.** Conservar el 15 de junio en riego para comparar las modalidades bajo la misma exposición. **Razón.** En Guanajuato la agenda contempla esa fecha en punta de riego tanto en el norte (15 de mayo al 15 de junio) como en el centro y sur (1 de mayo al 30 de junio), p. 184. **Consecuencias.** Se interpreta como simulación regional. No acredita la fecha efectiva del riego en cada municipio queretano. Las fechas observadas permitirían evaluar un calendario diferenciado. [Agenda de Guanajuato](../data/bronce/inifap/agenda_Gto_2017.pdf)

## D-018 · 26/11/2026 · Presupuesto de cuartillas del cuerpo

- **Contexto.** Los lineamientos de entrega fijan una extensión máxima de 60 cuartillas (p. 3). El documento maestro tiene 38 páginas en el corte del 26 de noviembre.
- **Alternativas consideradas.** Contar el archivo completo o medir el cuerpo desde la introducción hasta el final de las conclusiones.
- **Decisión.** Aplicar el máximo de 60 cuartillas al cuerpo. Los preliminares, las referencias y los anexos quedan fuera del cómputo.
- **Razón.** El sustentante aclaró el alcance del límite para este trabajo.
- **Consecuencias.** En este corte, 4 páginas corresponden a preliminares, 23 al cuerpo, 8 a referencias y 3 a anexos. El cuerpo dispone de un margen de crecimiento de 37 cuartillas. Las 23 actuales incluyen apartados con texto de plantilla.
- **Corte posterior a los pasos 2.6–2.8.** Word paginó 47 páginas totales. El cuerpo tiene 29 cuartillas, desde la introducción hasta las conclusiones, y dispone de 31 cuartillas adicionales. El análisis exploratorio ocupó dos páginas, la presentación de la propuesta una y la integración de datos tres.

## D-019 · 27/11/2026 · Partición temporal

**Contexto y alternativas.** La opción A reserva 2017–2019 para calibrar, con 36 eventos y uno de riego. **Decisión y razón.** Adoptar B. Entrenamiento 2003–2017, 454/1,809 pérdidas. Validación 2018–2020, 49/362 (tres de riego). Prueba 2021–2025, 91/605. Un año menos de prueba permite calibrar con más eventos. Las filas de un año permanecen juntas. **Consecuencias.** Las pérdidas anuales medias fueron 41.4, 7.7 y 19.1 en 2003–2012, 2013–2018 y 2019–2025. La precipitación media de floración en temporal fue 101.4, 86.6 y 93.8 mm. La caída de eventos desde 2013 coincidió con menor precipitación media. Los promedios no identifican el efecto del clima ni distinguen cambios de registro, seguros o variedades. Se calibra en años recientes y se informa por año, incluido 2023.

## D-020 · 27/11/2026 · Predictores y horizonte de decisión

**Contexto y alternativas.** El clima de llenado se completa el 7 de octubre con el escenario de siembra del 15 de junio. **Decisión.** Comparar temporada completa (18 variables climáticas y ocho fijas) y prefloración (ocho climáticas y las mismas fijas) al cierre del 13 de agosto. **Razón.** La segunda versión usa solo las etapas que ya transcurrieron. **Consecuencias.** Para adelantar la primera harían falta escenarios de años análogos, por implementar en el día 7. Se excluyen cosecha, pérdidas, producción, rendimiento, precios y valores corrientes y constantes, identificadores, año, fecha de siembra, INPC, factor y grado de marginación. Estado se deriva de la clave. En operación, superficie y fecha deben corresponder a información conocida al emitir el aviso. La superficie anual del cierre aproxima la sembrada y el índice 2020 se usa retrospectivamente como perfil fijo, con esa limitación temporal.

## D-021 · 27/11/2026 · Desbalance y búsqueda

**Contexto y alternativas.** La exactitud favorece a la clase mayoritaria. **Decisión.** Optimizar precisión promedio (AP, especificación de PR-AUC) con 20 combinaciones por algoritmo, cinco pliegues crecientes y bloques de dos años (2008–09 a 2016–17). El primer ajuste usa 2003–07. Escalado dentro del pliegue para logística y red. Pesos balanceados para logística y boosting, por submuestra para el bosque. La red usa parada temprana interna solo en los años del ajuste y el umbral económico común. **Razón y consecuencias.** Se contrastan los puntajes con la prevalencia de cada bloque. La climatología suma dos pseudoobservaciones con la tasa histórica de la modalidad a cada celda, incluso a las de cero eventos. Una celda nueva recibe la tasa de modalidad y una modalidad desconocida la global.

## D-022 · 27/11/2026 · Selección anterior a la prueba

**Contexto y alternativas.** Se puede privilegiar la media o tolerar una desviación entre modelos de distinta complejidad. **Decisión previa.** Para cada horizonte se elige la mayor AP media en los cinco bloques con igual peso. Ante un empate exacto se prefiere, en orden, climatología, logística, bosque, boosting y red. **Razón.** Los bloques difieren en prevalencia y la desviación entre años no estima una diferencia pareada entre algoritmos. **Consecuencias.** La selección incluye la referencia, se registra antes de ajustar Platt y queda fija frente a los resultados de prueba.

**Resultado de la selección.** Con temporada completa ganó el boosting por histogramas (AP media 0.665876). Al 13 de agosto ganó el bosque (0.615447). La referencia alcanzó 0.597837 en ambos. Todos los modelos superaron la prevalencia de cada uno de los cinco bloques. [Detalle por bloque](../reports/busqueda_modelos.csv)

## D-023 · 27/11/2026 · Calibración temporal

**Contexto y alternativas.** Validación contiene 49 eventos entre 362 filas, tres en riego. **Decisión.** Congelar cada ajuste de entrenamiento y ajustar una sigmoide de Platt común con 2018–2020. **Razón.** La isotónica dispone de más flexibilidad con pocos positivos y una calibración separada para riego dependería de tres eventos. **Consecuencias.** Contrastar la media calibrada con 49/362 en validación y reportar el cambio de Brier solo en la prueba. La climatología calibrada se evalúa como quinto modelo. El denominador de BSS usa la climatología cruda recalculada con 2003–2020. Los límites percentiles del 95 % remuestrean cinco años completos con reemplazo, emparejando pronóstico y referencia. Hay 3,125 remuestras ordenadas. En cada año se presentan estimaciones puntuales; cinco años dan intervalos de escasa resolución.

## D-024 · 27/11/2026 · Acciones, umbrales económicos y equidad

**Contexto y alternativas.** El sustentante eligió usar el escenario publicado por INIFAP. No se dispone de una cotización de la cooperativa. Se compararon cortes de probabilidad fijos y costos incrementales. **Decisión.** Aplicar el marco de costo–pérdida de Richardson a dos ampliaciones de un calendario de riegos de auxilio. El INIFAP informa 600 MXN/ha por auxilio en Sinaloa en 2024. Su ensayo de maíz reporta 6.79, 9.73 y 10.62 t/ha con dos, tres y cinco auxilios, respectivamente (cuadro 5, p. 15). Amarillo evalúa pasar de dos a tres; rojo, de tres a cinco. El costo marginal se expresa en pesos de 2025 con el factor del INPC de 2024. Para estimar el valor bruto por ha se divide el valor de producción real agregado entre la superficie sembrada agregada de 2003–2020. Como escenario, cada incremento experimental de rendimiento se expresa respecto a las 6.79 t/ha del calendario de partida y se aplica al valor histórico por ha. C/L es el precio marginal dividido entre el valor recuperable de ese escalón. [Costo del INIFAP](https://www.gob.mx/inifap/articulos/recomendaciones-para-el-manejo-del-riego-normal-y-deficitario-de-maiz) · [Ensayo de INIFAP e IMTA](https://www.fps.org.mx/portal/index.php/component/phocadownload/category/30-granos-y-flores?download=66:tecnologias-de-riego-bajo-condiciones-de-escasez-de-agua-en-maiz)

**Razón y consecuencias.** Los umbrales permiten un ensayo retrospectivo en pesos constantes. El ensayo corresponde a riego en Sinaloa, otoño–invierno, en suelo arcilloso. Se supone que el valor adicional se recupera solo si hay un evento. El evento municipal incluye daños por otras causas y el ensayo no estima esa respuesta para Guanajuato o Querétaro. El color en temporal sirve para comparar avisos bajo el mismo corte; recomendar riego exige acceso a agua y validación local. Un aviso con clima observado al 7 de octubre llega después de algunas decisiones de riego. Para anticiparlas se requiere el modelo del 13 de agosto o escenarios. El costo publicado en 2024 también limita la interpretación retrospectiva para años anteriores.

**Auditoría preespecificada.** Usar el mismo umbral rojo por modalidad, estado y grado de marginación. Se requieren al menos 20 pérdidas por grupo para interpretar sensibilidad de manera descriptiva (una pérdida equivale como máximo a cinco puntos). Con menos eventos se etiqueta «no concluyente». La diferencia de 10 puntos de RNF-03 activa revisión de cobertura, exposición y registro. Registrar los contrastes y recabar más ciclos antes de cambiar umbrales por grupo con la misma prueba.

**Resultado del escenario y decisión operativa.** El valor histórico de producción es 17,159.56 MXN de 2025 por hectárea sembrada. Para amarillo, C = 622.86 y L = 7,429.91 MXN/ha, con umbral de 8.38 %. Para rojo, C = 1,245.71 y L = 2,249.19 MXN/ha, con umbral de 55.39 %. En temporada completa el umbral amarillo anticipó 62 de 91 eventos con 136 falsas alarmas. El rojo emitió dos avisos, ambos falsas alarmas. En prefloración los respectivos conteos fueron 74 aciertos y 195 falsas alarmas, y cero aciertos en ocho rojos. La igualdad de sensibilidad roja (cero en todos los grupos) refleja una falla compartida. Riego (11 pérdidas) y marginación alta (12) quedan como no concluyentes. Se preserva esta prueba para reporte. Antes de utilizar el rojo para asignar recursos se requiere contrastar costos, eficacia y disponibilidad de agua con la cooperativa y validar un nuevo corte en ciclos independientes. [Costos y pérdidas evitables](../reports/costos_semaforo.csv) · [Equidad histórica al rojo](../reports/equidad_rojo.csv) · [Alertas por año](../reports/semaforo.csv)

**Comparación de horizontes y explicación.** Adelantar el aviso del 7 de octubre al 13 de agosto reduce la AP en 0.0874 (0.3150 frente a 0.2276) y el BSS en 0.0367 (0.1456 frente a 0.1089). En ambos casos el intervalo de BSS al 95 % incluye cero. La logística obtuvo mejor Brier en la prueba que los dos ganadores de validación cruzada; D-022 mantiene la selección previa a la prueba. En 2023 se concentraron 48 de los 91 eventos. Para el boosting, su AP anual fue 0.760, pero su BSS fue −0.376. Una buena ordenación ese año coexistió con probabilidades menos precisas que la referencia.

En el boosting, las cinco primeras columnas por media de |SHAP| fueron el indicador de riego, la lluvia en siembra, la radiación y la racha seca en crecimiento vegetativo, y la lluvia en llenado. Concuerdan con diferencias de abastecimiento de agua y exposición por etapa. La lluvia de floración ocupó el sexto lugar. Su asociación bivariada con la siniestralidad y su importancia una vez incluidas otras variables miden cosas distintas. Las atribuciones del bosque suman a su probabilidad cruda y las del boosting al logaritmo de momios. Platt conserva el orden en ambos ganadores; las atribuciones numéricas pertenecen a la escala cruda. En los casos locales se suman las columnas de una misma variable categórica para dar una sola explicación de la modalidad o del estado. [Importancia](../reports/importancia_shap.csv) · [Casos en palabras del técnico](../reports/caso_shap.csv) · [Métricas por año y modalidad](../reports/metricas_modelos.csv)

## D-025 · 27/11/2026 · Contrato del servicio municipal

**Contexto y alternativas.** La interfaz y los productos posteriores necesitan interpretar del mismo modo una predicción. Se consideró duplicar el cálculo en cada ruta o compartir una capa de servicio con un contrato versionado.

**Decisión.** Usar el prefijo `/v1`. `GET /salud` informa el estado y el modelo cargado. `GET /municipios` entrega claves, nombres y modalidades disponibles, con consulta opcional por clave. `POST /prediccion` recibe clave INEGI de cinco dígitos, modalidad, año y última etapa observada. Devuelve la probabilidad media, el nivel de aviso, P10, P90, el número de escenarios y los años análogos. `POST /explicacion` recibe la misma solicitud y añade la escala de SHAP, la base, la salida media, tres factores con dirección y un mensaje en español. Una solicitud válida responde 200, una combinación o historial ausente responde 404 y una entrada inválida responde 422. Los dos errores tienen detalle en español.

**Razón.** El servicio concentra la carga de artefactos al inicio y comparte la construcción de escenarios entre predicción y explicación. El contrato de entrada permite validar la clave, modalidad, año y etapa antes del cálculo.

**Consecuencias.** El catálogo cubre 64 municipios con 121 de las 128 combinaciones municipio–modalidad. El Anexo B documenta las cuatro rutas en funcionamiento. RF-12 queda cubierto en predicción y explicación. La simulación y el boletín corresponden al día 8. [Contrato y ejemplos](../src/api/main.py) · [Pruebas del servicio](../tests/test_api.py)

## D-026 · 27/11/2026 · Pronóstico dentro del ciclo con años análogos

**Contexto y alternativas.** La lluvia de floración y llenado todavía se desconoce cuando se decide el aviso temprano. Se compararon usar todos los años distintos del consultado, usar solo los anteriores y sustituir cada variable por su media histórica.

**Decisión.** Mantener los predictores fijos y el clima observado de la fila. Cada año anterior del mismo municipio y modalidad aporta todas las etapas pendientes en conjunto. Cada trayectoria recibe el mismo peso. El aviso se pinta aplicando los umbrales estrictos de D-024 a la media de las probabilidades calibradas. Se devuelven los percentiles 10 y 90 entre años, su lista y el número de escenarios. Con llenado observado se calcula una sola probabilidad y los dos percentiles coinciden con ella. Sin observación o sin historia previa para completar lo pendiente se devuelve 404.

**Razón.** La secuencia de un mismo año conserva la asociación histórica entre etapas y evita usar clima posterior al año consultado como análogo. Day (1985, p. 157) aporta el antecedente de pronosticar a partir de condiciones conocidas y trayectorias meteorológicas históricas. [Artículo](https://doi.org/10.1061/%28ASCE%290733-9496%281985%29111%3A2%28157%29)

**Consecuencias.** Los percentiles describen la dispersión meteorológica entre escenarios. Con solo siembra, en 605 observaciones de prueba, la diferencia absoluta mediana frente a la climatología preprueba fue de 10.9 puntos porcentuales y alcanzó 64.7 puntos. El muestreo histórico por sí solo no garantiza proximidad en cada municipio. El servicio opera sobre los años con datos del piloto y el modelo calibrado hasta 2020. Las consultas de años anteriores a 2021 son reconstrucciones con ese modelo fijo. Una emisión en tiempo real requiere datos observables al corte, incluida la superficie sembrada. [Control por municipio, año y modalidad](../reports/control_api_siembra.csv)

### Extensión de D-026 · Calibración del aviso de siembra (RF-06)

**Decisión.** En siembra se publica la climatología municipal por modalidad calibrada con Platt. Se consideró conservar la frecuencia cruda y suprimir el rojo en esa etapa. Se eligió calibrar porque RF-06 exige una probabilidad interpretable además del color. Los dos cortes de D-024 se aplican a la probabilidad calibrada antes de redondear. El campo `fuente` conserva el valor `climatologia`; el contrato y la explicación identifican el método. Los percentiles quedan nulos porque en siembra no se mezclan trayectorias meteorológicas.

**Datos disponibles al emitir.** Para los años de prueba se reutiliza `completa_climatologia_platt.joblib`: frecuencias suavizadas ajustadas con 2003–2017 y sigmoide calibrada con 2018–2020. La referencia cruda 2003–2020 sigue siendo el denominador histórico del BSS. Por eso el cambio de orden entre ambas climatologías puede reflejar las ventanas de ajuste. En reconstrucciones anteriores a 2021 se separan bloques previos al año solicitado: se reserva para Platt hasta un máximo de los tres últimos años y se ajustan las tasas en los restantes. Si faltan bloques disjuntos con ambos desenlaces o historia previa de la celda, se informa falta de cobertura (404). En este piloto los años 2003 y 2004 no permiten calibrar en un bloque anterior independiente. Desde vegetativo se usa el boosting de la extensión de D-027.

**Contraste en 605 observaciones, 2021–2025.** Se observaron 91 pérdidas (15.0 %). La probabilidad media de siembra pasó de 23.1 % a 13.5 %, el Brier de 0.1436 a 0.1329 y la AP de 0.252 a 0.241. Para el mismo estimador base de 2003–2017, el Brier sin Platt fue 0.1522 y con Platt 0.1329. Los avisos desde amarillo bajaron de 410 a 310 y los eventos detectados de 84 a 77. Los rojos bajaron de 40 (8 aciertos) a 35 (7 aciertos). Su precisión siguió en 20 %. En la entrega anterior hubo 33 transiciones de rojo en siembra a amarillo en llenado. Al mantener fijo el nuevo modelo de llenado, la siembra cruda habría dado 37 transiciones y la calibrada dio 32. Los dos contrastes distinguen el cambio de modelo del efecto de calibrar la siembra. [Conteos de alertas y transiciones](../reports/alertas_siembra.csv) · [Métricas por etapa](../reports/metricas_por_etapa.csv) · [Predicciones de la versión anterior](https://github.com/Mauricio-Avina/riesgo-agroclimatico/blob/313761e7093f8a2741af915386227fead9f6d03e/reports/prediccion_por_etapa.csv)

## D-027 · 27/11/2026 · Coherencia agronómica del aviso de déficit hídrico (RF-07)

**Contexto.** La revisión identificó inversiones en los aportes de lluvia y días secos. Una explicación compatible con D-019 es la asociación de los periodos con la precipitación y la frecuencia de siniestro. Los cierres municipales registran daños de distintos orígenes y esa hipótesis no identifica una causa.

**Alternativas.** Un indicador de periodo asumiría que los regímenes históricos persisten. Entrenar desde 2013 descartaría la mayoría de los eventos del ajuste. Restringir el boosting permite conservar años, hiperparámetros, particiones y calibración del experimento original.

**Decisión previa a ejecutar la corrección.** Por RF-07 se restringe a no creciente la respuesta a lluvia de siembra y floración, y a no decreciente la respuesta a la racha seca de floración, manteniendo las demás entradas constantes. Se conservan las demás variables libres. Estas direcciones representan el régimen de déficit hídrico del piloto y pueden ocultar daño por exceso de agua. Se preserva el modelo original y se ajusta la variante con 2003–2017 y Platt con 2018–2020. Se verifica la dirección con perturbaciones controladas y se contrasta con las atribuciones SHAP. El cambio responde a RF-07. La prueba 2021–2025 ya fue examinada y la comparación es retrospectiva. Una evaluación independiente requiere otros ciclos.

**Uso en el corte inicial de tres restricciones (sustituido por las extensiones de D-026 y D-027).** En siembra se comunicaba la frecuencia municipal suavizada de su modalidad. Para la prueba se congela la historia al cierre de 2020 y para consultas más antiguas se excluye el año consultado y los posteriores. Desde vegetativo se usa el modelo restringido con las etapas pendientes cubiertas por años anteriores. Se auditan ambas versiones al amarillo, el primer aviso, conservando los conteos del rojo. Se informan AP y BSS por etapa sin elegir umbrales por grupo en los años de prueba.

### Corte anterior con tres restricciones

**Resultado sobre las mismas 605 observaciones.** En llenado, el boosting original y el restringido dieron AP de 0.315 y 0.342, BSS de 0.146 y 0.189, y Brier calibrado de 0.1227 y 0.1164. Las correlaciones de Spearman entre valor y SHAP cambiaron de +0.714 a −0.839 en lluvia de floración y de −0.691 a +0.482 en racha seca de floración. En el caso 11032 de temporal en 2023, 0 mm en siembra pasó de aportar −1.721 a +0.217 logaritmos de momios. En 15,125 contrastes de la salida calibrada, variando un predictor a la vez por cuantiles y manteniendo el resto fijo, se contaron 3,776 inversiones originales y cero con restricciones. Una correlación entre filas, una contribución respecto a la base y una variación parcial responden a preguntas distintas. Las direcciones de las variables libres aún requieren revisión agronómica. [Direcciones y conteos](https://github.com/Mauricio-Avina/riesgo-agroclimatico/blob/313761e7093f8a2741af915386227fead9f6d03e/reports/revision_direcciones.csv) · [Comparación pareada sobre los mismos casos](https://github.com/Mauricio-Avina/riesgo-agroclimatico/blob/313761e7093f8a2741af915386227fead9f6d03e/reports/revision_modelos.csv)

**Revisión de D-026.** Para las cuatro etapas en orden fenológico, la AP del esquema original fue 0.172, 0.223, 0.230 y 0.315. La de la climatología de 2003–2020 fue 0.252. En siembra, el ROC-AUC de temporal fue 0.303 en el original y 0.350 tras restringirlo. En esa etapa la API devuelve la tasa histórica suavizada, indica su fuente y explica conteos y suavizado. Los dos percentiles son nulos y la lista de años análogos está vacía. Desde vegetativo devuelve la media y percentiles del modelo restringido. El color se decide a precisión completa y la respuesta numérica se redondea a cuatro decimales. [Métricas por etapa y modalidad](https://github.com/Mauricio-Avina/riesgo-agroclimatico/blob/313761e7093f8a2741af915386227fead9f6d03e/reports/metricas_por_etapa.csv)

**Revisión de D-024 y RNF-03.** El denominador de sensibilidad son las pérdidas de cada grupo. A continuación se documentan todos los contrastes de más de 10 puntos al amarillo. Las explicaciones son hipótesis de composición, cobertura y calibración. Los cierres municipales no demuestran causalidad individual. Los grupos con menos de 20 eventos se mantienen como no concluyentes.

| Dimensión y pares con brecha (puntos porcentuales) | Evidencia y posible explicación | Medida verificable antes del uso operativo |
| --- | --- | --- |
| Guanajuato frente a Querétaro, 32.1 en el original y 26.5 en el restringido | Querétaro tuvo 10 de sus 53 pérdidas en riego y Guanajuato 1 de 38. En el año de mayor detección (2023) se concentraron 34/38 pérdidas de Guanajuato y 14/53 de Querétaro. En el modelo restringido quedaron sin aviso 21 en Querétaro y 5 en Guanajuato. | Revisar primero los 21 casos omitidos del piloto con el técnico. Contrastar la sensibilidad por año y modalidad y volver a medir la brecha estatal en ciclos independientes. |
| Temporal frente a riego, 67.2 en el original y 70.9 en el restringido | Solo hubo 11 eventos de riego, 10 omitidos en ambas versiones. En la restringida la mediana del riesgo de los casos con pérdida fue 1.5 % en riego y 25.7 % en temporal. | Contrastar los 10 cierres omitidos con disponibilidad de agua y origen del daño. Reunir al menos 20 pérdidas de riego antes de interpretar el contraste. |
| Marginación media, baja y alta frente a muy baja, respectivamente 25.2, 20.2 y 11.8 en el original y 21.9, 20.5 y 16.9 con restricciones | En muy baja se omitieron 14/31 eventos originalmente y 13/31 en la revisión. Diez de esas 13 omisiones ocurrieron en 2021–2022. La concentración por año puede afectar los contrastes. El grupo alto solo reúne 12 eventos. | Revisar las 10 omisiones tempranas de muy baja, cruzar grado con año y modalidad y repetir los tres contrastes en otros ciclos. Ampliar la evidencia de alta hasta 20 pérdidas. |
| Marginación media frente a alta, 13.3 en el original y 5.0 en el restringido | En el original media detectó 16/20 y alta 8/12. Una detección más en alta elevó su tasa a 9/12. | Verificar el cierre del caso cuyo aviso cambió y acumular más pérdidas de alta antes de cambiar el umbral. |

**Alcance del semáforo y calibración.** De las 91 pérdidas, 80 fueron de temporal. El costo del riego de auxilio de Sinaloa no sustenta prescribirlo en temporal. En la práctica hubo dos niveles útiles para seguimiento, verde y aviso desde amarillo. El rojo dio dos avisos falsos en el original y siete en el restringido, sin aciertos. Los dos modelos subestimaron los cinco quintiles. En promedio pronosticaron 8.3 % y 10.1 % frente al 15.0 % observado; la logística original pronosticó 14.6 %. Los umbrales y la calibración requieren evaluación prospectiva antes de derivar acciones locales. [Grupos y denominadores](https://github.com/Mauricio-Avina/riesgo-agroclimatico/blob/313761e7093f8a2741af915386227fead9f6d03e/reports/revision_equidad.csv) · [Quintiles](https://github.com/Mauricio-Avina/riesgo-agroclimatico/blob/313761e7093f8a2741af915386227fead9f6d03e/reports/revision_quintiles.csv) · [Alertas](https://github.com/Mauricio-Avina/riesgo-agroclimatico/blob/313761e7093f8a2741af915386227fead9f6d03e/reports/revision_alertas.csv)

### Extensión de D-027 · Regla completa de déficit hídrico (RF-07)

**Contexto y decisión.** La versión con tres restricciones dejaba libre la racha seca de siembra. En prueba, su correlación valor–SHAP fue −0.395 y su importancia media absoluta 0.275. En San José de Iturbide (11032), temporal, 2023, siete días secos en los siete días de siembra aportaron −1.116 logaritmos de momios. Se extendió la misma hipótesis agronómica a diez predictores: riesgo no creciente con la lluvia y no decreciente con las rachas secas en las cuatro etapas, y no decreciente con los días de calor en floración y de helada en llenado. Se mantienen los años, hiperparámetros y calibración de las versiones previas. La motivación es RF-07. Se conserva el carácter retrospectivo de la comparación.

**Verificación.** Las correlaciones valor–SHAP para racha seca de siembra, lluvia vegetativa y racha seca de llenado pasaron de −0.395, +0.052 y −0.526 a +0.509, −0.894 y +0.764. En el caso de los siete días secos el aporte pasó a +0.012. Al variar un predictor por cuantiles y fijar los demás hubo cero inversiones en 40,535 contrastes con nueve predictores que variaron en prueba. La décima restricción, helada, está instalada: todas las filas de entrenamiento y las 605 de prueba registraron cero días, por lo que no se estimó una dirección empírica. Un aporte local compara ese valor con la base del árbol. La restricción gobierna el cambio al aumentar el predictor y mantener los demás constantes. [Diagnóstico de direcciones y caso local](../reports/revision_direcciones.csv)

**Consecuencias.** En temporada completa, AP/BSS fueron 0.315/0.146 sin restricciones, 0.342/0.189 con tres y 0.337/0.167 con diez. La versión en servicio obtuvo Brier 0.1445 antes de Platt y 0.1196 después, con media de riesgo de 8.3 % frente a 15.0 % observado. Los cinco quintiles subestimaron las pérdidas. En la Figura 5 se emplea la curva de este último modelo. El beneficio de imponer direcciones agronómicas se evalúa por coherencia y sigue pendiente contrastarlo en ciclos independientes. [Métricas vigentes](../reports/revision_modelos.csv) · [Versión con tres restricciones](https://github.com/Mauricio-Avina/riesgo-agroclimatico/blob/313761e7093f8a2741af915386227fead9f6d03e/reports/revision_modelos.csv) · [Quintiles](../reports/revision_quintiles.csv)

**Seguimiento de RNF-03.** Al amarillo, Guanajuato detectó 33/38 pérdidas y Querétaro 31/53 (brecha de 28.4 puntos). Se priorizan las 22 omisiones de Querétaro y la comparación por año y modalidad. Riego detectó 2/11 y temporal 62/80 (59.3 puntos); se revisarán los nueve daños omitidos en riego y se ampliará su muestra. Frente a marginación muy baja (17/31), las brechas de media (16/20), baja (22/28) y alta (9/12) fueron 25.2, 23.7 y 20.2 puntos. Diez de las 14 omisiones en muy baja ocurrieron en 2021–2022. Se revisarán esos cierres y se reunirán más pérdidas de marginación alta. Estos contrastes describen composición y cobertura dentro del piloto. [Resultados por grupo](../reports/revision_equidad.csv)

## D-028 · 27/11/2026 · Factores de la tarjeta del productor

**Contexto y alternativas.** El mayor aporte local puede corresponder a radiación, ubicación u otra variable sin una dirección agronómica impuesta. Se consideró mostrar las tres mayores contribuciones de todo el árbol o limitar la tarjeta a las variables defendibles para RF-07.

**Decisión y razón.** Desde vegetativo se eligen por valor absoluto tres aportes TreeSHAP entre las cuatro lluvias, las cuatro rachas secas, el calor en floración, la helada en llenado y la modalidad agrupada. Cada frase expresa la contribución respecto a la base del modelo. Las restricciones describen el cambio parcial al variar una sola variable. En siembra se explican el conteo municipal, el suavizado por modalidad y los años de calibración de Platt.

**Consecuencias.** La vista técnica conserva los aportes de todas las variables del árbol y su escala. Cuando quedan etapas por observar, se promedian las contribuciones sobre los mismos años análogos que la predicción. Las tres frases de la tarjeta forman una selección y su suma puede diferir del puntaje completo.

## D-029 · 27/11/2026 · Vistas del productor y del técnico

**Contexto y alternativas.** La cooperativa usa una computadora compartida. Se compararon una sola vista con indicadores técnicos, dos vistas con PIN y dos vistas accesibles con exportación limitada por el servicio.

**Decisión y razón.** La vista del productor reúne nivel, símbolo, frecuencia natural, tres factores y una recomendación. Las frecuencias conservan un denominador de cien cuando la pérdida sería invisible por redondeo a decenas. La orientación de campo se adapta a la modalidad, con la Agenda técnica agrícola de Querétaro (2017) y las recomendaciones de riego de INIFAP (2024) como referencias. La vista técnica concentra historia, explicación completa, simulación y descarga.

**Consecuencias.** RF-15 y el Anexo I definen un modo técnico separado. Cualquier persona con acceso al equipo puede abrirlo. El servicio exporta exclusivamente variables municipales públicas con unidad, fecha y fuente. El tratamiento de datos individuales exigiría revisar el alcance y el control de acceso.

## D-030 · 27/11/2026 · Consulta local y ciclo de demostración

**Contexto y alternativas.** Se valoraron la consulta exclusivamente en línea, una copia de la última consulta y el precálculo de todo el padrón de demostración. La conectividad puede interrumpirse durante el trabajo de campo.

**Decisión y razón.** El ciclo 2025 se identifica como reconstrucción retrospectiva. La API y la interfaz se sirven en el equipo. Al ejecutar la actualización se regeneran las 484 combinaciones de predicción y explicación (121 municipios-modalidades por cuatro etapas) y los 64 boletines municipales, uno por clave con la información de llenado de sus modalidades. Actualizar al incorporar un cierre o cambiar el modelo y antes de distribuir una nueva copia.

**Consecuencias.** El aviso de copia muestra la fecha de generación y la ficha conserva la del último día observado de su etapa. En ausencia de la API siguen disponibles la búsqueda, las fichas y el PDF. La simulación interactiva requiere la API local. El ensayo bloqueó los destinos externos y luego detuvo la API. La red física del equipo siguió disponible para otros programas.

## D-031 · 27/11/2026 · Escenarios y pérdida esperada por hectárea

**Contexto y alternativas.** Un año promedio sintético puede mezclar etapas que nunca ocurrieron juntas. Se consideraron temporadas históricas representativas y diferentes fórmulas monetarias para comparar fecha y modalidad.

**Decisión y razón.** Para la modalidad actual y el municipio, se suma la lluvia de las cuatro ventanas de referencia de cada año hasta 2020. Se selecciona el año más cercano a cada percentil 20, 50 y 80; en empate se toma el año más temprano. A, B y C comparten los tres años. Cada alternativa ocupa la fila municipal de su modalidad en ese mismo año y recalcula las 18 variables del clima diario para una siembra del 1 de junio al 15 de julio. La referencia de oro corresponde al 15 de junio.

**Escala económica.** Para cada modalidad, L es el valor total de producción en pesos de 2025 dividido entre las hectáreas sembradas en 2003–2020, multiplicado por la siniestralidad media de los registros que superan el 10 % siniestrado. Se obtienen 10,656.87 MXN/ha en riego y 3,634.78 en temporal. La pérdida esperada es la probabilidad calibrada, antes de redondear, multiplicada por L. Constituye una aproximación regional al valor expuesto por hectárea. No incorpora los costos de cambiar la fecha o la modalidad.

**Consecuencias.** El tornado parte de A en clima normal y altera una de las diez variables restringidas de P10 a P90 por vez. Los límites y el aviso P1–P99 para los predictores numéricos se calculan solo con 2003–2017. Los escenarios sin fila municipal-modalidad-año se indican como carentes de cobertura. Las comparaciones son retrospectivas y describen sensibilidad del modelo. En San José de Iturbide (11032), temporal, los años seleccionados fueron 2005, 2006 y 2004.

## D-032 · 27/11/2026 · Prueba piloto de usabilidad

**Contexto y alternativas.** Una demostración guiada evalúa el funcionamiento del sistema, pero oculta dificultades de uso. Se compararon la demostración y tres tareas observadas sin asistencia con un cuestionario posterior.

**Decisión y razón.** Se prevén cinco sesiones de treinta minutos con perfiles técnicos, agronómicos o de producción. Después del consentimiento se emplean códigos P1–P5. Se registran logro, duración, errores y bloqueos por tarea. Tras dos minutos sin avance se termina esa tarea. El SUS usa los diez ítems españoles de Sevilla-Gonzalez et al. (2020), apéndice 2, y la puntuación de Brooke (1996).

**Consecuencias.** RF-08 exige cuatro de cinco consultas interpretadas sin ayuda y RNF-01 exige un SUS medio de al menos 68 puntos. Se informan denominadores por tarea, perfiles y media de cuestionarios completos. Los problemas y las correcciones se documentarán con observaciones reales y capturas antes y después. Las pruebas automáticas aportan evidencia técnica independiente.

## D-033 · 27/11/2026 · Adopción por fases

**Contexto y alternativas.** El piloto carece de experiencia de operación cooperativa sostenida. Frente a un despliegue inmediato se eligieron un ciclo técnico, un ciclo de ampliación a productores y una operación con revisión anual.

**Decisión y razón.** El plan define por rol actividades, indicadores y reglas de avance, ajuste o detención antes de recoger evidencia. La compatibilidad con tareas existentes, la facilidad de ensayo y los apoyos locales permiten evaluar adopción y utilidad (Rogers, Davis y Venkatesh et al.). **Consecuencias.** RF-13 evalúa el plan entregado. Las aprobaciones, minutas e indicadores de cada fase se obtendrían en campo. [Plan](adopcion.md)

## D-034 · 27/11/2026 · Datos públicos y aportaciones futuras

**Contexto y alternativas.** El equipo compartido ofrece acceso local a agregados públicos. Admitir aportaciones identificables en el mismo entorno expondría a titulares y comunidades.

**Decisión y razón.** Se documentó un acuerdo de activación previa para información de personas o parcelas identificables, con finalidad, responsable, acceso limitado, plazo, derechos, correcciones y retiro. Se consideraron la LFPDPPP y CARE cuando la información sea colectiva. **Consecuencias.** RF-14 verifica la entrega del acuerdo propuesto. Hasta que las partes acuerden condiciones y existan controles apropiados, el piloto opera con agregados públicos. [Acuerdo propuesto](acuerdo_datos.md)

## D-035 · 27/11/2026 · Evidencia de pruebas y calidad

**Contexto y alternativas.** Una demostración con archivos ya generados oculta problemas de instalación. Un mínimo arbitrario de cobertura incentivaría pruebas sin comprobaciones. **Decisión y razón.** Medir cobertura real de sentencias con pytest-cov, añadir un control manual de diez días, verificar un clon con entorno nuevo y comparar cinco reportes completos. Las nueve características de ISO/IEC 25010:2023 ordenan las evidencias y limitaciones. **Consecuencias.** Se conserva la salida íntegra, tiempos con perf_counter y revisión reproducida. No se confunden pruebas unitarias, ensayos de sistema y validación con personas. La prueba posterior a D-030 apagó la radio Wi-Fi y verificó la consulta y el boletín. En el simulador de D-031, la diferencia máxima entre siembras consecutivas fue de 36.03 puntos en el municipio 11032. Por ello se presenta también el intervalo del día anterior al siguiente. [Reproducción](../reports/reproduccion.md)

## D-036 · 27/11/2026 · Selección de decisiones para la fundamentación

**Contexto y alternativas.** Enumerar todas las decisiones del diario consumiría el espacio de 3.6 sin aclarar qué alternativa se descartó. **Decisión y razón.** Elegir catorce decisiones que cambian la unidad de análisis, la validez temporal, la interpretación del riesgo, el acceso al aviso o la gobernanza; contrastar cada una con una alternativa, una fuente y evidencia local. **Consecuencias.** La tabla mantiene la trazabilidad de las decisiones centrales. Las reglas operativas y su historial permanecen en este diario, referenciado en el Anexo H. [Fundamentación de las 14 decisiones](fundamentacion.md)
