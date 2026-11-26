"""Conteos de la ejecución actual y comparación de faltantes en cada granularidad."""
import pandas as pd

from src import config


class Auditoria:
    """Acumula conteos, sin retener en memoria los archivos nacionales y diarios."""

    def __init__(self):
        """Inicia los contadores para una ejecución independiente."""
        self.filas = {}
        self.nulos = {}

    def entrada(self, fuente, tabla):
        """Cuenta observaciones y faltantes originales antes de seleccionar o agregar."""
        self.filas[fuente] = self.filas.get(fuente, 0) + len(tabla)
        faltantes = tabla.isna().sum()
        if fuente in self.nulos:
            faltantes = self.nulos[fuente].add(faltantes, fill_value=0)
        self.nulos[fuente] = faltantes

    def publicar(self, tablas):
        """Informa denominadores; las variables derivadas carecen de medida cruda."""
        fuentes = [
            ("SIAP", "siap_maiz_pv", "Cierre nacional filtrado por cultivo, ciclo, estados y modalidad"),
            ("Geografía", "municipios", "Polígonos de los dos estados; cálculo de área y punto interior"),
            ("POWER", "clima_diario", "Un día por punto; -999 se reconoce como faltante desde la entrada"),
            ("INPC", "inpc", "Serie mensual completa; selección de 2003–2025 y promedio de doce meses"),
            ("CONAPO", "marginacion", "Selección de los dos estados del fichero municipal nacional"),
            ("Oro", "dataset_maestro", "Filas SIAP enriquecidas; conversión a pesos constantes"),
        ]
        registros = []
        for fuente, nombre, motivo in fuentes:
            tabla = tablas[nombre]
            antes = self.nulos[fuente]
            comun = dict(fuente=fuente, filas_entrada=self.filas[fuente], filas_salida=len(tabla), motivo=motivo)
            registros.append(dict(**comun, tipo="fuente"))
            for variable in tabla:
                registros.append(dict(**comun, tipo="variable", variable=variable,
                    faltantes_antes=antes.get(variable), faltantes_despues=tabla[variable].isna().sum(),
                    pct_antes=100 * antes[variable] / self.filas[fuente] if variable in antes else None,
                    pct_despues=100 * tabla[variable].isna().mean()))
        pd.DataFrame(registros).to_csv(config.REPORTES / "calidad.csv", index=False, float_format="%.6f")
