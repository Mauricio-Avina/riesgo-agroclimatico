# Usuarios y tareas del piloto de maíz

El productor decide qué parcela revisar y cuándo avisar a la cooperativa. Consulta por municipio y modalidad antes de salir a campo o al regresar. Puede usar la computadora de la cooperativa y llevar el boletín impreso a la parcela. Con señal intermitente, necesita reconocer la fecha y la etapa de la estimación.

El técnico o agrónomo contrasta el aviso con los cierres municipales, compara fechas de siembra e identifica cuándo conviene visitar las parcelas. Trabaja en la computadora de la cooperativa. Puede ejecutar simulaciones sin salida a internet mientras funcione el servicio local. Los perfiles orientan el diseño y se contrastarán en el piloto.

## Sesión individual de 30 minutos

Reservar cinco minutos para consentimiento, quince para las tres tareas y diez para el SUS y comentarios. Convocar a cinco personas con experiencia técnica o agronómica y, de ser posible, en producción. Registrar solo P1–P5 y el perfil declarado. Antes del piloto, una persona ajena al proyecto leerá la tarjeta y explicará qué entendió. Registrar textualmente cualquier duda sin identificarla.

**Consentimiento.** «Estamos probando una herramienta de la cooperativa. Puedes detener la sesión en cualquier momento. Registraremos tu perfil, tiempos, errores y respuestas bajo un código. ¿Aceptas participar?» Si se retira, dejar las observaciones y respuestas en blanco.

| Tarea que se lee literalmente | Criterio observable de éxito |
| --- | --- |
| 1. Consulta el riesgo de San José de Iturbide, Guanajuato, en temporal y llenado. Cuéntame qué significa lo que ves. | Encuentra la ficha correcta. Expresa con sus palabras el nivel y la posibilidad de una pérdida municipal superior a la décima parte de la superficie sembrada. |
| 2. Compara dos fechas de siembra en temporal para ese municipio. En un año seco, ¿cuál elegirías si buscas la menor pérdida esperada por hectárea? | Identifica dos filas del mismo clima, lee los importes y fundamenta su elección en el menor valor o reconoce un empate. |
| 3. Guarda el boletín para llevarlo al campo y ábrelo. | Descarga y abre el PDF del municipio correcto e identifica el ciclo y la etapa impresa. |

Iniciar el cronómetro al terminar de leer cada consigna. Anotar segundos, número de errores y la acción observada. Si pasan más de 120 segundos sin avance, terminar la tarea como incompleta. Una tarea completada con ayuda queda fuera de los éxitos. Evitar explicar las pantallas o indicar dónde hacer clic. En la hoja de tareas escribir `si` o `no` sin acento. No registrar nombres, contactos, audio ni imágenes de las personas.

**Cuestionario y cálculo.** Administrar los diez enunciados del Anexo G, en su orden, después de la tercera tarea. Registrar enteros de 1 a 5 en `sus_respuestas.csv` y las tres observaciones por persona en `sus_tareas.csv`. Ejecutar `python -m src.app.sus`. El resultado individual y la media se expresan en puntos SUS de 0 a 100. Cada tarea muestra éxitos sobre tareas observadas. Un campo en blanco indica que falta la observación. RF-08 requiere cuatro de cinco consultas sin ayuda; RNF-01 requiere una media de al menos 68 en el piloto de cinco. [Instrumento validado, apéndice 2](https://humanfactors.jmir.org/2020/4/e21161/)

Al concluir, ordenar los problemas observados por impacto en la decisión, bloqueo de la tarea y recurrencia. Asociar cada corrección con tarea, códigos anónimos, captura previa, cambio y captura posterior. Informar el perfil representado y el tamaño del piloto junto con los resultados.

## Lecturas para el apartado 2.8

- ISO 9241-210 (2019). Alcance y principios del diseño centrado en las personas. Distinguir la decisión del productor en campo de la revisión del técnico en la cooperativa. Observar las tareas antes de revisar la interfaz. [Ficha en Zotero](zotero://select/library/items/T8F73GDQ)
- Nielsen (1994). Capítulo 2, pp. 25–62. Mostrar el corte del dato y el uso de la copia local; usar nombres de etapas y acciones familiares. Verificar después con usuarios. [Ficha en Zotero](zotero://select/library/items/JTDYRAL3)
- W3C (2018). Criterios de conformidad 1.4.1 y 1.4.3. Agregar palabra y símbolo al nivel de riesgo y revisar la ficha impresa en escala de grises. [Ficha en Zotero](zotero://select/library/items/LDE34SBD)
- Gigerenzer y Hoffrage (1995). Resumen y planteamiento, pp. 684–686. Traducir la estimación a temporadas de cada diez o cien. Comprobar la interpretación municipal mediante la tarea 1. [Ficha en Zotero](zotero://select/library/items/KLPGQRL6)
- Spiegelhalter et al. (2011). Revisión ilustrada, pp. 1393–1400. Indicar qué superficie define una pérdida y diferenciar una frecuencia estimada de la observada. [Ficha en Zotero](zotero://select/library/items/CCSVMW52)
- Nielsen y Landauer (1993). Modelo de detección, pp. 206–213. Usar cinco sesiones para encontrar obstáculos del piloto. Informar perfiles y evitar extrapolar tasas al conjunto de productores. [Ficha en Zotero](zotero://select/library/items/JX5QPW67)
- Brooke (1996). Cuestionario y sección de puntuación. Calcular un valor por persona tras las tres tareas. Diez respuestas neutrales dan 50 puntos. [Ficha en Zotero](zotero://select/library/items/QVG34892)
- Bangor et al. (2009). Resultados sobre escalas adjetivales, pp. 114–123. Reportar el promedio como puntos sobre 100 y la tasa de éxito por separado. El objetivo de 68 se fija en RNF-01. [Ficha en Zotero](zotero://select/library/items/JQ6AWZ33)
- Sevilla-Gonzalez et al. (2020). Resultados y apéndice multimedia 2. Aplicar los diez enunciados del apéndice 2 con sus anclajes de 1 a 5 después de las tareas. [Ficha en Zotero](zotero://select/library/items/HA434A5M)
- INEGI (2026). ENDUTIH 2025, resultados por ámbito rural y urbano. Prever conexión intermitente, copia municipal fechada y un boletín para llevar al campo. [Ficha en Zotero](zotero://select/library/items/YLG9NMVS)
