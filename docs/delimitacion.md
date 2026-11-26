# Delimitación y comparación de estados

El piloto de la interfaz, el boletín y la adopción se realizará en Querétaro. Para entrenar y evaluar el modelo se propone utilizar Querétaro y Guanajuato, ciclo primavera-verano, maíz grano y modalidades de riego y temporal, durante 2003–2025. Este periodo se escogió por la cobertura municipal publicada por la [DGSIAP](https://nube.agricultura.gob.mx/datosAbiertos/Agricola.php); la disponibilidad efectiva de cada combinación y el número de pérdidas deberán verificarse al integrar los datos.

## Comparación para elegir el piloto

La comparación siguiente se limita a 2023–2025 y no es el periodo de entrenamiento. Son datos de maíz grano, ciclo primavera-verano, riego y temporal. La superficie media es la suma de las hectáreas sembradas de los tres años dividida entre tres. Los porcentajes son cocientes de las sumas de los tres años: superficie de temporal / superficie total sembrada y superficie siniestrada / superficie total sembrada, respectivamente.

| Estado | Superficie sembrada media anual (ha) | Superficie de temporal (%) | Superficie siniestrada (%) |
| --- | ---: | ---: | ---: |
| Guanajuato | 335,236.33 | 57.07 | 6.87 |
| Jalisco | 541,913.08 | 92.65 | 1.67 |
| Michoacán | 465,960.66 | 75.26 | 7.79 |
| Querétaro | 75,383.86 | 70.91 | 13.63 |

En promedio, Querétaro sembró el 22.49 % de la superficie de Guanajuato, el 16.18 % de la de Michoacán y el 13.91 % de la de Jalisco. De los cuatro estados, tuvo la menor superficie sembrada media y la mayor proporción siniestrada durante la comparación. La superficie siniestrada representa pérdida total y puede incluir causas distintas de fenómenos climáticos; no debe interpretarse por sí sola como pérdida exclusivamente climática.

### Datos para reproducir la tabla

| Estado | Año | Sembrada total (ha) | Sembrada temporal (ha) | Siniestrada total (ha) |
| --- | ---: | ---: | ---: | ---: |
| Guanajuato | 2023 | 366,582.00 | 213,587.00 | 65,468.25 |
| Guanajuato | 2024 | 324,824.00 | 188,569.00 | 0.00 |
| Guanajuato | 2025 | 314,303.00 | 171,786.00 | 3,624.50 |
| Jalisco | 2023 | 552,644.36 | 511,589.39 | 26,701.42 |
| Jalisco | 2024 | 530,643.87 | 492,863.06 | 0.00 |
| Jalisco | 2025 | 542,451.00 | 501,747.00 | 375.00 |
| Michoacán | 2023 | 485,314.47 | 364,848.27 | 91,564.55 |
| Michoacán | 2024 | 458,978.00 | 342,401.20 | 12,863.00 |
| Michoacán | 2025 | 453,589.51 | 344,762.00 | 4,479.60 |
| Querétaro | 2023 | 75,941.07 | 54,473.00 | 22,733.00 |
| Querétaro | 2024 | 72,405.07 | 51,075.00 | 3,500.00 |
| Querétaro | 2025 | 77,805.45 | 54,825.00 | 4,601.15 |

Fuente: Servicio de Información Agroalimentaria y Pesquera, estadísticas de producción agrícola. Los valores 2023 y 2024 proceden de las hojas de cierre agrícola de maíz grano conservadas en el archivo de trabajo «Cierre agrícola.xlsx». Los valores 2025 se obtuvieron sumando los registros municipales de maíz grano, primavera-verano, del [cierre municipal oficial de 2025](https://nube.agricultura.gob.mx/index.php?ANIO=2025&view=10AE434F-A2158368-A120BC5A-EDF4AFAA), separando temporal y riego. Consulta: 26 de noviembre de 2026. La hoja «Cierre agrícola 2025» del archivo de trabajo no identifica un cultivo y contiene todos los cultivos, por lo que no se utilizó como total de maíz.
