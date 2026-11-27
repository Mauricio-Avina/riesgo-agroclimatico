# Calidad observada en el piloto municipal

Se aplicó el modelo de calidad del producto de [ISO/IEC 25010:2023, segunda edición](https://www.iso.org/standard/78176.html). La evaluación corresponde al equipo local y a la etiqueta v1.0-entrega del 27 de noviembre de 2026. Los tiempos HTTP corresponden al ensayo previo identificado en tiempos.json.

| Característica | Prueba o evidencia | Resultado y alcance |
| --- | --- | --- |
| Adecuación funcional | Contratos de las cuatro operaciones de RF-12, equivalencia con oro, extremos de la banda. | Las cuatro respondieron con 200/404/422 según el caso. A sin cambio coincidió con la consulta. |
| Eficiencia de desempeño | 100 predicciones y 10 simulaciones HTTP locales, secuenciales, con una solicitud de calentamiento. | Medias 7.29 y 208.73 ms. Sin carga simultánea ni compromiso de latencia en otro equipo. |
| Compatibilidad | API con JSON/PDF y navegador local en Windows; apertura del boletín y exportación CSV. | Interoperación observada entre la API y Streamlit. Otros navegadores y sistemas quedaron sin evaluar. |
| Capacidad de interacción | Dos modos, texto/símbolo/color, fechas en palabras, cuestionario SUS y tareas sin ayuda. | La tarjeta se verificó técnicamente. El resultado con personas se declara en el Anexo G. |
| Fiabilidad | Radio Wi‑Fi apagada con API activa; ensayo separado con API detenida. | Ficha y PDF recuperados en ambos. La simulación interactiva requiere la API local. |
| Seguridad de la información | Servicio enlazado a loopback, validación de entradas y exportación por lista de campos. | El CSV contiene agregados municipales permitidos. El equipo compartido carece de autenticación individual. |
| Mantenibilidad | Pruebas de módulos, D-001–D-038 y cobertura de sentencias bajo pytest. | 23 pruebas, 35 % de cobertura en la etiqueta (618/1,785). La suite no ejecuta todo el entrenamiento ni la interfaz. |
| Flexibilidad | Traslado a otra carpeta en Windows con Python y entorno virtual nuevos. | La actualización y las pruebas terminaron; la portabilidad a otros sistemas sigue abierta. |
| Protección frente a daños | Restricciones parciales, aviso de extrapolación, banda de fechas y revisión humana prevista. | Se activó el aviso ante un extremo y se documentaron brechas. El efecto en decisiones de campo queda por evaluar. |
