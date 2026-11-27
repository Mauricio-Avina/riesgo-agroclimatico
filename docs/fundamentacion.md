# Fundamentación de las decisiones del piloto

El apartado 3.6 vincula catorce decisiones con la alternativa que se consideró, el concepto que sostuvo la elección y una comprobación en el proyecto. La secuencia completa de decisiones se conserva en el [registro del proyecto](decisiones.md).

| Decisión | Alternativa descartada | Fundamento | Evidencia |
| --- | --- | --- | --- |
| Conservar insumos y huella por archivo | Sobrescribir el original | 2.4 · Procedencia y reutilización (Wilkinson et al., 2016) | D-005 y D-015; manifiesto de bronce |
| Una fila por municipio, año y modalidad | Mezclar modalidades y escalas | 2.4 · Unidad de observación (Wickham, 2014) | Tabla 9; validación de la llave |
| Evento con más del 10 % siniestrado | Etiquetar toda pérdida positiva | 2.1 y 2.5 · Pérdida respecto del rendimiento esperado (Lobell et al., 2011). Corte local según D-014. | D-014; objetivo.py |
| Separar por años completos | Sortear registros de todos los años | 2.5 · Dependencia temporal (Roberts et al., 2017) | D-019; Anexo E |
| Seleccionar por AP | Usar solo exactitud global | 2.5 · Precisión y sensibilidad con desbalance (Saito & Rehmsmeier, 2015) | D-022; Tabla 10 |
| Calibrar en años posteriores | Tomar la salida cruda como probabilidad | 2.6 · Ajuste sigmoidal (Platt, 1999) | D-023; Figura 5 |
| Fijar avisos con costo/pérdida | Elegir los cortes en prueba | 2.6 · Valor económico del aviso (Richardson, 2000) | D-024; costos_semaforo.csv |
| Usar años climáticos observados | Combinar etapas independientes | 2.6 · Trayectorias históricas (Day, 1985) | D-026 y D-031; Tabla 14 |
| Imponer direcciones de déficit hídrico | Dejar todos los predictores libres | 2.2 y 2.5 · Respuesta parcial (Scikit-learn developers, s/f) | D-027; revisión RF-07 |
| Explicar tres aportes defendibles | Exponer todo el vector en la tarjeta | 2.7 · Contribución local (Lundberg & Lee, 2017) | D-028; Figura 7 |
| Mostrar frecuencias y corte visible | Porcentaje y color como única señal | 2.8 · Interpretación del riesgo (Gigerenzer & Hoffrage, 1995) | D-029; Anexo F |
| Distribuir copia local y boletín | Exigir conexión externa | 2.3 y 2.8 · Condiciones de acceso (Instituto Nacional de Estadística y Geografía, 2026) | D-030; pruebas de desconexión |
| Observar tareas y medir SUS | Inferir facilidad de una demostración | 2.8 · Usabilidad percibida (Sevilla-Gonzalez et al., 2020) | D-032; Anexo G |
| Adoptar por fases y acordar el uso de datos | Extender sin revisión ni responsables | 2.9 · Ensayo y autoridad sobre los datos (Rogers, 2003) (Carroll et al., 2020) | D-033 y D-034; Anexo D |
