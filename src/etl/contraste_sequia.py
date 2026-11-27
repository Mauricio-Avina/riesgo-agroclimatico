"""Cotejo descriptivo de las pérdidas anuales con cortes municipales del MSM."""
import pandas as pd

from src import config
from src.etl.archivos import descargar
from src.registro import configurar_registro


def main():
    """Cuenta municipios con D1–D4 en algún cierre mensual entre junio y septiembre."""
    url = "https://smn.conagua.gob.mx/tools/RESOURCES/Monitor%20de%20Sequia%20en%20Mexico/MunicipiosSequia.xlsx"
    ruta = descargar(url, config.BRONCE / "smn" / "MunicipiosSequia.xlsx")
    monitor = pd.read_excel(ruta, sheet_name=0, dtype={"CVE_CONCATENADA": str})
    monitor = monitor.set_index(monitor.CVE_CONCATENADA.str.zfill(5))
    oro = pd.read_parquet(config.ORO / "dataset_maestro.parquet")
    totales = oro.groupby("anio")[["sembrada_ha", "siniestrada_ha"]].sum()
    totales["pct_superficie_siniestrada"] = 100 * totales.siniestrada_ha / totales.sembrada_ha
    criterio = "pct_superficie_siniestrada"
    extremos = pd.concat([totales.nlargest(3, criterio).assign(grupo="Mayor pérdida"),
                          totales.nsmallest(3, criterio).assign(grupo="Menor pérdida")])
    claves = set(oro.cvegeo)
    if not claves.issubset(monitor.index) or not monitor.index.is_unique:
        raise ValueError("El catálogo del Monitor no coincide con las claves del piloto")
    filas = []
    for anio, anual in extremos.iterrows():
        fechas = pd.date_range(f"{anio}-06-01", f"{anio}-09-30", freq="ME")
        cortes = monitor.loc[sorted(claves), fechas]
        afectados = cortes.isin(["D1", "D2", "D3", "D4"]).any(axis=1)
        filas.append(dict(anio=anio, grupo=anual.grupo, sembrada_ha=anual.sembrada_ha,
                          siniestrada_ha=anual.siniestrada_ha, pct_superficie_siniestrada=anual[criterio],
                          municipios=len(claves),
                          con_sequia=int(afectados.sum()), guanajuato=int(afectados[afectados.index.str.startswith("11")].sum()),
                          queretaro=int(afectados[afectados.index.str.startswith("22")].sum())))
    pd.DataFrame(filas).to_csv(config.REPORTES / "contraste_sequia_3_3.csv", index=False)


if __name__ == "__main__":
    configurar_registro()
    main()
