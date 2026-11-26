# Integración municipal de maíz grano, 2003–2025

El [maestro de datos](../data/oro/dataset_maestro.parquet) reúne 2,776 observaciones de primavera-verano y 41 columnas. Guanajuato aporta 1,996 registros en 46 municipios y Querétaro, 780 en 18 municipios. De las 2,944 combinaciones posibles faltan 166 de riego y dos de temporal en los cierres del SIAP. El maestro conserva las combinaciones publicadas.

## Puntos de control

| Pieza | Lo que debe salir | Resultado observado | Cómo se comprobó |
| --- | --- | --- | --- |
| SIAP, Querétaro 2025 | 77,805.45 ha sembradas | **77,805.45 ha** | Se sumaron las hectáreas sembradas del estado 22 durante 2025. Riego aportó 22,980.45 ha y temporal 54,825.00 ha. |
| SIAP, Querétaro 2023 | 75,941.07 ha sembradas y 22,733 ha siniestradas | **75,941.07 ha sembradas y 22,733.00 ha siniestradas** | La suma estatal reúne 21,468.07 ha sembradas en riego y 54,473.00 en temporal. Toda la superficie siniestrada corresponde a temporal. |
| Municipios | 64 con coordenadas, 18 de Querétaro y 46 de Guanajuato | **18 + 46 = 64**, todos con latitud y longitud | Se contaron las claves únicas por prefijo de estado y se cruzaron las 64 claves del SIAP con la cartografía. Hubo 64 coincidencias y cero coordenadas faltantes. |
| Clima | 64 archivos y 8,401 días por municipio, para 537,664 filas | **64 JSON, 8,401 días en cada serie y 537,664 filas** | Se cotejaron los nombres de archivo con las claves municipales y las fechas de cada serie con el calendario del 01/01/2003 al 31/12/2025. Incluye seis días 29 de febrero. |
| INPC | 23 valores anuales | **23 valores**, uno por cada año de 2003 a 2025 | Se verificaron el conteo, la unicidad y la secuencia de años. Los 276 índices mensuales producen 23 medias de doce meses. El factor para expresar 2025 en pesos de ese mismo año es 1. |
| Marginación | 64 municipios con índice y grado | **64 con ambos datos**, cero sin correspondencia | Se hizo una unión izquierda de las claves únicas del SIAP con CONAPO 2020. El indicador de unión marcó 64 coincidencias y se comprobó que índice y grado tenían valor. |
| Oro | Hasta 2,944 filas y cero llaves repetidas | **2,776 filas y cero duplicados** | Se contó por municipio, año y modalidad y se compararon las llaves de los 23 CSV originales filtrados con las de plata y oro. Las tres listas coinciden. Cada uno de los cuatro cruces conservó las 2,776 filas. |

Las referencias estatales proceden de la [delimitación](../docs/delimitacion.md). Las 64 claves tienen cinco dígitos, por ejemplo, `11001` para Abasolo. La superficie cosechada nunca supera a la sembrada, la siniestralidad va de 0 a 1 y ningún denominador vale cero. Las cinco variables diarias tienen cobertura completa. También se cotejaron con el manifiesto las huellas SHA-256 de los 96 archivos de origen y coincidieron las 96.

### Las 168 combinaciones ausentes

Al comparar el universo de 64 municipios × 23 años × 2 modalidades con los cierres originales de maíz grano, primavera-verano, se localizaron las siguientes ausencias:

| Modalidad | Municipio y periodo sin fila en el cierre | Combinaciones ausentes |
| --- | --- | ---: |
| Riego | Atarjea, Ocampo, Santa Catarina, Tierra Blanca y Xichú (Guanajuato), Pinal de Amoles y Landa de Matamoros (Querétaro), todos de 2003 a 2025 | 161 |
| Riego | Coroneo en 2009 y Moroleón en 2006 y 2018 (Guanajuato), Arroyo Seco y Jalpan de Serra en 2004 (Querétaro) | 5 |
| Temporal | Tarandacuao (Guanajuato) en 2013 y 2014 | 2 |

El faltante se origina en la cobertura publicada para ese cultivo, ciclo y modalidad. Los cierres por sí solos no permiten distinguir entre falta de siembra y falta de reporte. Se conservaron las **1,306 filas de riego y 1,470 de temporal** que sí tienen observación.

**Datos faltantes.** Hay nueve celdas nulas. En 2025, los cierres de riego de Jalpan de Serra, San Joaquín y Tolimán reportan cero hectáreas cosechadas y cero toneladas. En estos registros el SIAP deja vacíos el rendimiento y el precio, y el precio en pesos de 2025 hereda el faltante. Cada una de esas tres columnas tiene 0.1081 % de nulos. El resto tiene cobertura completa. [Porcentaje por columna](calidad_oro.csv)

**Contraste de precipitación.** La tabla compara el promedio de los totales anuales de la celda asignada al municipio con la normal de una estación situada en él. La diferencia porcentual se calcula respecto de la normal del SMN.

| Municipio y estación | NASA POWER 2003–2025 (mm/año) | SMN 1991–2020 (mm/año) | Diferencia |
| --- | ---: | ---: | ---: |
| Abasolo, Guanajuato · estación 11001 | 709.00 | 673.80 | +5.22 % |
| Corregidora, Querétaro · El Batán, estación 22004 | 668.60 | 677.40 | −1.30 % |

En Abasolo, POWER da un promedio más húmedo que el de la estación. En Corregidora, la diferencia es menor y cambia de signo al recortar POWER a 2003–2020 (+0.08 %). Los periodos y el área que representa cada fuente difieren. Estas dos comparaciones acotan la interpretación local y dejan abierta la precisión de los extremos diarios y de los municipios serranos. [Cotejo con ambos periodos](cotejo_lluvia_smn.csv) · [Normal de Abasolo](../data/bronce/smn/nor9120_11001.txt) · [Normal de El Batán](../data/bronce/smn/nor9120_22004.txt)

**Comprobación de las ventanas.** La prueba usa nueve días con lluvias de 0, 0.4, 0, 1, 0, 0, 0, 0 y 0 mm. El total es 1.4 mm y el día de 1 mm separa rachas de tres y cinco días. Con máximas de 35 °C los primeros ocho días y 30 °C el último, y mínimas entre −2 y 0 °C, el recorte produce (30 + 10)/2 − 10 = 10 grados día diarios, 90 en total y ocho días de calor. También se comprobó que mover la siembra desplaza la ventana y que un día ausente invalida los indicadores que lo necesitan. [Pruebas de las ventanas](../tests/test_ventanas.py)

**Reproducción.** Desde la raíz del proyecto, con su entorno de Python activo, se pueden ejecutar estos módulos en orden. Los archivos ya descargados se reutilizan. El código conserva los nombres originales del SIAP, los indicadores por etapa y los importes nominales y reales. El [manifiesto](../data/bronce/manifiesto.csv) identifica cada archivo fuente con su URL, fecha y huella SHA-256. Las [decisiones D-005 a D-013](../docs/decisiones.md) documentan los supuestos y las páginas consultadas de las agendas del INIFAP.

```text
python -m src.etl.siap
python -m src.etl.municipios
python -m src.etl.clima
python -m src.etl.economia
python -m src.etl.sociedad
python -m src.features.oro
python -m unittest discover -s tests -v
```
