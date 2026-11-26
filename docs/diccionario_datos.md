# Diccionario del conjunto maestro

Cada fila identifica un municipio, año agrícola y modalidad. Los indicadores por etapa requieren datos completos de su ventana. Los resultados de cierre y las ventanas futuras se excluyen de los predictores de una alerta emitida antes de que estén disponibles.

| Nombre | Descripción | Unidad | Fuente | Transformación |
| --- | --- | --- | --- | --- |
| `cvegeo` | Clave municipal INEGI | texto, 5 dígitos | SIAP / INEGI | Concatena estado (2) y municipio (3) con ceros iniciales. |
| `anio` | Año agrícola del cierre | año | SIAP | Entero entre 2003 y 2025. |
| `modalidad` | Disponibilidad de agua del cultivo | categoría | SIAP | Selecciona Riego y Temporal, maíz grano PV. |
| `sembrada_ha` | Superficie sembrada | ha | SIAP | Medida del cierre filtrado. Se interpretan separadores numéricos y se conservan los faltantes. |
| `cosechada_ha` | Superficie cosechada | ha | SIAP | Medida del cierre filtrado. Se interpretan separadores numéricos y se conservan los faltantes. |
| `siniestrada_ha` | Superficie con pérdida total | ha | SIAP | Medida del cierre filtrado. Se interpretan separadores numéricos y se conservan los faltantes. |
| `produccion_t` | Volumen cosechado | t | SIAP | Medida del cierre filtrado. Se interpretan separadores numéricos y se conservan los faltantes. |
| `rendimiento_t_ha` | Rendimiento publicado sobre superficie cosechada | t/ha | SIAP | Medida del cierre filtrado. Se interpretan separadores numéricos y se conservan los faltantes. |
| `precio_pesos_t` | Precio medio rural nominal | MXN/t | SIAP | Medida del cierre filtrado. Se interpretan separadores numéricos y se conservan los faltantes. |
| `valor_produccion_pesos` | Valor nominal de la producción | MXN | SIAP | Medida del cierre filtrado. Se interpretan separadores numéricos y se conservan los faltantes. |
| `siniestralidad` | Fracción de la superficie sembrada que se siniestró | proporción 0–1 | SIAP | Divide hectáreas siniestradas entre sembradas. Nulo si el denominador es cero. |
| `fecha_siembra_escenario` | Inicio supuesto del ciclo | fecha | Escenario / INIFAP | 15 de junio del año agrícola para las dos modalidades. |
| `lluvia_siembra_mm` | Precipitación acumulada en establecimiento | mm | NASA POWER | Días 0–6 desde la siembra, inclusivos. Suma de PRECTOTCORR. |
| `racha_seca_siembra_dias` | Mayor racha seca en establecimiento | días | NASA POWER | Días 0–6 desde la siembra, inclusivos. Máximo de días seguidos con menos de 1 mm. |
| `gdd_siembra` | Calor acumulado en establecimiento | °C·día | NASA POWER | Días 0–6 desde la siembra, inclusivos. Suma de (máxima y mínima acotadas a 10–30 °C, promediadas) menos 10 °C diarios. |
| `radiacion_siembra_mj_m2_dia` | Radiación solar media en establecimiento | MJ/m²/día | NASA POWER | Días 0–6 desde la siembra, inclusivos. Media diaria de ALLSKY_SFC_SW_DWN. |
| `lluvia_vegetativo_mm` | Precipitación acumulada en desarrollo vegetativo | mm | NASA POWER | Días 7–59 desde la siembra, inclusivos. Suma de PRECTOTCORR. |
| `racha_seca_vegetativo_dias` | Mayor racha seca en desarrollo vegetativo | días | NASA POWER | Días 7–59 desde la siembra, inclusivos. Máximo de días seguidos con menos de 1 mm. |
| `gdd_vegetativo` | Calor acumulado en desarrollo vegetativo | °C·día | NASA POWER | Días 7–59 desde la siembra, inclusivos. Suma de (máxima y mínima acotadas a 10–30 °C, promediadas) menos 10 °C diarios. |
| `radiacion_vegetativo_mj_m2_dia` | Radiación solar media en desarrollo vegetativo | MJ/m²/día | NASA POWER | Días 7–59 desde la siembra, inclusivos. Media diaria de ALLSKY_SFC_SW_DWN. |
| `lluvia_floracion_mm` | Precipitación acumulada en floración | mm | NASA POWER | Días 60–79 desde la siembra, inclusivos. Suma de PRECTOTCORR. |
| `racha_seca_floracion_dias` | Mayor racha seca en floración | días | NASA POWER | Días 60–79 desde la siembra, inclusivos. Máximo de días seguidos con menos de 1 mm. |
| `gdd_floracion` | Calor acumulado en floración | °C·día | NASA POWER | Días 60–79 desde la siembra, inclusivos. Suma de (máxima y mínima acotadas a 10–30 °C, promediadas) menos 10 °C diarios. |
| `radiacion_floracion_mj_m2_dia` | Radiación solar media en floración | MJ/m²/día | NASA POWER | Días 60–79 desde la siembra, inclusivos. Media diaria de ALLSKY_SFC_SW_DWN. |
| `calor_floracion_dias` | Días calurosos en floración | días | NASA POWER | Cuenta máximas estrictamente superiores a 30 °C en días 60–79. |
| `lluvia_llenado_mm` | Precipitación acumulada en llenado | mm | NASA POWER | Días 80–114 desde la siembra, inclusivos. Suma de PRECTOTCORR. |
| `racha_seca_llenado_dias` | Mayor racha seca en llenado | días | NASA POWER | Días 80–114 desde la siembra, inclusivos. Máximo de días seguidos con menos de 1 mm. |
| `gdd_llenado` | Calor acumulado en llenado | °C·día | NASA POWER | Días 80–114 desde la siembra, inclusivos. Suma de (máxima y mínima acotadas a 10–30 °C, promediadas) menos 10 °C diarios. |
| `radiacion_llenado_mj_m2_dia` | Radiación solar media en llenado | MJ/m²/día | NASA POWER | Días 80–114 desde la siembra, inclusivos. Media diaria de ALLSKY_SFC_SW_DWN. |
| `helada_llenado_dias` | Días con helada en llenado | días | NASA POWER | Cuenta mínimas estrictamente inferiores a 0 °C en días 80–114. |
| `municipio` | Nombre del municipio | texto | INEGI | Nombre de la entidad geográfica municipal. |
| `latitud` | Latitud del punto interior | grados | INEGI | Punto representativo transformado a EPSG:4326. |
| `longitud` | Longitud del punto interior | grados | INEGI | Punto representativo transformado a EPSG:4326. |
| `area_km2` | Superficie del polígono municipal | km² | INEGI | Área en EPSG:6933 dividida entre un millón. |
| `altitud_celda_m` | Elevación de la celda consultada | m | NASA POWER | Tercera coordenada de la respuesta por punto. |
| `marginacion_2020` | Índice de marginación municipal | índice | CONAPO | IM_2020, corte fijo vinculado por clave municipal. |
| `grado_marginacion_2020` | Grado de marginación municipal | categoría | CONAPO | GM_2020, corte fijo vinculado por clave municipal. |
| `inpc` | Índice general nacional medio del año | índice | INEGI | Media de doce índices mensuales, serie 865541. |
| `factor_pesos_constantes` | Factor de actualización monetaria | razón | INEGI | INPC anual de 2025 dividido entre INPC del año agrícola. |
| `precio_pesos_t_de_2025` | Precio medio rural real | MXN de 2025/t | SIAP / INEGI | Precio nominal multiplicado por el factor anual. |
| `valor_produccion_pesos_de_2025` | Valor real de la producción | MXN de 2025 | SIAP / INEGI | Valor nominal multiplicado por el factor anual. |
