# Ficha del modelo municipal de pérdida de maíz

**Identificación y responsables.** Piloto retrospectivo de maíz grano, primavera–verano, en Guanajuato y Querétaro. Versión de servicio con diez restricciones de dirección (D-027) y calibración de Platt. El rol técnico interpreta y revisa el aviso; el consejo de la cooperativa decidiría sobre usos y ampliaciones. Estructura adaptada de [Mitchell et al. (2019)](https://doi.org/10.1145/3287560.3287596).

**Uso previsto.** Priorizar municipios y orientar visitas o conversaciones con productores. La unidad es municipio–año–modalidad. El evento se registra cuando la superficie siniestrada supera el 10 % de la sembrada. La probabilidad expresa riesgo de superar ese umbral. El porcentaje de superficie dañada en una parcela requiere observación local.

**Usos no recomendados.** No emplear el resultado para conceder o negar crédito o seguros, imponer sanciones, valorar individualmente a productores ni ordenar riegos de auxilio en temporal. El simulador estima sensibilidad retrospectiva y excluye los costos de cambiar de fecha o modalidad.

**Datos y cortes.** Oro integra SIAP, clima NASA POWER, geografía de INEGI, INPC y marginación CONAPO. De 2,776 registros, 1,809 (454 pérdidas) corresponden a entrenamiento 2003–2017; 362 (49) a validación y calibración 2018–2020; 605 (91) a prueba 2021–2025. Cada año completo permaneció en un único bloque. Se excluyeron del ajuste los resultados agrícolas de cierre que definen la etiqueta.

**Factores y estimación.** La API devuelve climatología municipal suavizada y calibrada en siembra. Desde vegetativo, el boosting usa clima por etapa, modalidad y características municipales. Las etapas aún desconocidas se completan con trayectorias anteriores. Las cuatro lluvias tienen restricción decreciente; las cuatro rachas secas, el calor en floración y la helada en llenado tienen restricción creciente. La helada permaneció constante en el entrenamiento. TreeSHAP explica el puntaje previo a calibración. En la tarjeta se seleccionan tres aportes entre las variables restringidas y la modalidad. En siembra se describe la historia de referencia.

**Métricas de la temporada completa.** En prueba, AP 0.337, ROC-AUC 0.772, Brier 0.1196 y BSS 0.167 frente a la referencia municipal. Antes de calibrar, Brier fue 0.1445. La probabilidad media fue 8.3 % frente a 15.0 % de eventos. Se subestimaron los cinco quintiles. Los umbrales de amarillo y rojo proceden de costos de riego de auxilio de Sinaloa. El rojo tuvo escaso respaldo empírico; se audita la detección desde el amarillo. [Resultados e intervalos por años](../reports/revision_modelos.csv) · [Calibración](../reports/revision_quintiles.csv)

**Evaluación desagregada al amarillo (2021–2025).**

| Grupo | Casos | Pérdidas detectadas / observadas | Sensibilidad | Brier |
| --- | ---: | ---: | ---: | ---: |
| Guanajuato | 435 | 33/38 | 86.8 % | 0.0691 |
| Querétaro | 170 | 31/53 | 58.5 % | 0.2487 |
| Riego | 285 | 2/11 | 18.2 % | 0.0364 |
| Temporal | 320 | 62/80 | 77.5 % | 0.1937 |
| Marginación alta | 35 | 9/12 | 75.0 % | 0.2930 |
| Marginación baja | 215 | 22/28 | 78.6 % | 0.1022 |
| Marginación media | 105 | 16/20 | 80.0 % | 0.1501 |
| Marginación muy baja | 250 | 17/31 | 54.8 % | 0.0974 |

**Consideraciones éticas.** En Querétaro quedaron 22 pérdidas sin aviso y en riego, nueve. Las diferencias de composición y de años de pérdida son hipótesis que requieren revisión local. Los grupos con menos de 20 eventos se interpretan con cautela. Revisar primero las omisiones, documentar los motivos y contrastar otro ciclo antes de extender el uso. [Auditoría por grupo](../reports/revision_equidad.csv)

**Advertencias y mantenimiento.** El clima de una celda de rejilla puede diferir del de una parcela, en especial en relieve complejo. Un año análogo previo a 2018 forma parte del entrenamiento. Consultar la banda de fechas y las alertas P1–P99. Cada actualización requiere revisar cobertura municipal, calibración, diferencias de sensibilidad y cambios respecto al ciclo anterior. Ante daños, pérdida sistemática de avisos o un uso prohibido, remitir la decisión al consejo y suspender la ampliación. [Plan de adopción](adopcion.md) · [Propuesta de acuerdo de datos](acuerdo_datos.md)
