"""Controles de D-014, D-019 y D-020 sobre los datos publicados."""
import unittest

from src import config
from src.models.objetivo import cargar, grupos, pliegues, predictores


class ParticionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datos = cargar()
        cls.partes = grupos(cls.datos)

    def test_evento_estricto_y_particion(self):
        self.assertEqual(self.datos.perdida.sum(), 594)
        self.assertFalse(self.datos.loc[self.datos.siniestralidad.eq(config.UMBRAL_PERDIDA),
                                       "perdida"].any())
        anteriores = set()
        for parte, control in zip(self.partes.values(), [(1809,454), (362,49), (605,91)], strict=True):
            anios = set(parte.anio)
            self.assertTrue(anteriores.isdisjoint(anios))
            if anteriores:
                self.assertLess(max(anteriores), min(anios))
            anteriores.update(anios)
            self.assertEqual((len(parte), parte.perdida.sum()), control)
        self.assertEqual(anteriores, set(self.datos.anio))

    def test_pliegues(self):
        entrena = self.partes["entrenamiento"]
        for a, b in pliegues(entrena):
            self.assertLess(entrena.iloc[a].anio.max(), entrena.iloc[b].anio.min())
            self.assertEqual(entrena.iloc[b].anio.nunique(), config.ANIOS_POR_PLIEGUE)
            self.assertEqual(entrena.iloc[b].perdida.nunique(), 2)

    def test_predictores(self):
        for horizonte, n in [("completa",26), ("prefloracion",16)]:
            x = predictores(self.datos, horizonte)
            self.assertEqual(len(x.columns), n)
            self.assertTrue(set(config.EXCLUIDAS_MODELO).isdisjoint(x.columns))
            self.assertFalse(x.isna().any().any())
            if horizonte == "prefloracion":
                self.assertFalse(any("floracion" in c or "llenado" in c for c in x))
