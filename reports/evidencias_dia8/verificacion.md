# Verificación del simulador y de la consulta sin internet

Ensayo del 27 de noviembre de 2026 en Windows. La demostración corresponde al ciclo agrícola 2025. En llenado, el corte climático del calendario regional de referencia es el 7 de octubre de 2025.

| Comprobación | Resultado observado |
| --- | --- |
| Arranque con `iniciar.bat` | La API respondió en el puerto local 8000 y la interfaz en el 8501. |
| Consulta sin salida externa | Se abrió la ficha de Amealco de Bonfil, Querétaro, en temporal y llenado. Se descargó `boletin-22001-2025.pdf`. El historial técnico y la comparación de nueve escenarios respondieron. |
| Recuperación después de detener la API | Se confirmó la caída del servicio de predicción y se abrió la interfaz en un navegador nuevo. Apareció «Modo sin conexión: datos del 2026-11-27». Se volvió a descargar el PDF de Amealco de Bonfil. |
| Alcance del bloqueo | El navegador permitió únicamente destinos locales para HTTP y WebSocket. En los procesos Python se rechazaron conexiones y resolución de nombres externos. La página solicitó cero recursos externos en ambos ensayos. Se mantuvo la conexión física del equipo, según el alcance acordado. |
| Reconstrucción | En una copia del proyecto con los archivos de bronce ya descargados, `actualizar.bat` terminó correctamente, entrenó los modelos y publicó 484 fichas y 64 boletines. El contenido de las 484 fichas coincidió con el de la distribución local. |
| Contrato y cobertura | Las 21 pruebas automatizadas pasaron. Se consultaron los 64 PDF. Para simulación y boletín se verificaron respuesta válida (200), falta de cobertura (404) y entrada inválida (422). |

## Controles del simulador

Para San José de Iturbide (11032), la opción A usa temporal y 15 de junio. La opción B mantiene temporal y cambia la fecha al 1 de julio. La opción C conserva el 15 de junio y cambia a riego. Las tres alternativas se evaluaron con los mismos años análogos.

| Clima | Año | Probabilidad de A | Pérdida esperada de A (MXN de 2025/ha) |
| --- | ---: | ---: | ---: |
| Seco | 2005 | 0.7072 | 2,570.37 |
| Normal | 2006 | 0.4551 | 1,654.31 |
| Húmedo | 2004 | 0.3284 | 1,193.69 |

La probabilidad y el nivel de A coincidieron en los tres casos con la predicción directa de llenado. Para el año seco, los 18 indicadores recalculados el 15 de junio coincidieron exactamente con oro. El 1 de julio cambió la ventana. Una lluvia extrema activó el aviso P1–P99 y la solicitud de riego en un municipio sin esa modalidad recibió un 404. El tornado muestra diez variaciones de una sola variable en el clima normal de A. [Nueve resultados](simulacion_11032.csv) · [Datos del tornado](tornado_11032.csv)

## Evidencia de pantalla

Las capturas corresponden a Amealco de Bonfil. La comparación en pantalla usa temporal y siembras del 15, 22 y 29 de junio. [Vista del productor](consulta_productor.png) · [Historial técnico](historial_tecnico.png) · [Tabla y comparación](comparacion_escenarios.png) · [Tornado](tornado.png) · [Consulta con la API detenida](consulta_sin_conexion.png)

## Prueba con personas

Las capturas documentan un ensayo técnico. La lectura inicial por una persona ajena al proyecto y las cinco sesiones con consentimiento están pendientes. El registro de P1–P5 conserva vacíos los puntajes, tiempos y resultados. El cálculo SUS se verificó con respuestas de control: las diez neutrales dan 50, el patrón más favorable 100 y el menos favorable 0. [Protocolo](../../docs/usuarios.md) · [Registro del piloto](../sus.csv)
