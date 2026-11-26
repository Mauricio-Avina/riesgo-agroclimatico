import unittest

import pandas as pd

from src.features.ventanas import calcular_ventanas, fechas_por_etapa


class VentanasTest(unittest.TestCase):
    def setUp(self):
        fechas = pd.date_range("2023-06-01", periods=9)
        self.serie = pd.DataFrame({"lluvia": [0, 0.4, 0, 1, 0, 0, 0, 0, 0],
                                   "tmax": [35] * 8 + [30], "tmin": [-2] * 8 + [0],
                                   "radiacion": [20] * 9}, index=fechas)

    def test_conteo_manual_y_umbrales_estrictos(self):
        fechas = fechas_por_etapa("2023-06-01", {"floracion": (0, 8)})
        res = calcular_ventanas(self.serie, 2023, fechas)
        self.assertEqual(res["racha_seca_floracion_dias"], 5)
        self.assertEqual(res["lluvia_floracion_mm"], 1.4)
        self.assertEqual(res["gdd_floracion"], 90)
        self.assertEqual(res["calor_floracion_dias"], 8)
        self.assertEqual(res["radiacion_floracion_mj_m2_dia"], 20)
        fechas = fechas_por_etapa("2023-06-02", {"llenado": (0, 7)})
        self.assertEqual(calcular_ventanas(self.serie, 2023, fechas)["helada_llenado_dias"], 7)

    def test_dia_ausente_no_cuenta_como_seco(self):
        fechas = fechas_por_etapa("2023-06-01", {"floracion": (0, 8)})
        incompleta = self.serie.drop(index=self.serie.index[3])
        res = calcular_ventanas(incompleta, 2023, fechas)
        self.assertTrue(all(pd.isna(x) for x in res.values()))
        self.serie.loc[self.serie.index[3], "lluvia"] = float("nan")
        res = calcular_ventanas(self.serie, 2023, fechas)
        self.assertTrue(pd.isna(res["racha_seca_floracion_dias"]))
        self.assertEqual(res["gdd_floracion"], 90)
