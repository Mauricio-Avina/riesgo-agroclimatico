import unittest

import pandas as pd
from pandera.errors import SchemaError

from src.etl.esquemas import ESQUEMAS


class ValidacionTest(unittest.TestCase):
    def test_clave_corta(self):
        """El índice social nunca acepta una clave municipal truncada."""
        tabla = pd.DataFrame({"cvegeo": ["2201"], "marginacion_2020": [1.0],
                              "grado_marginacion_2020": ["Bajo"]})
        with self.assertRaisesRegex(SchemaError, "cvegeo"):
            ESQUEMAS["marginacion"].validate(tabla)

    def test_lluvia_negativa(self):
        """Un dato imposible falla en su propia columna antes del control de calendario."""
        tabla = pd.DataFrame([dict(cvegeo="22001", fecha=pd.Timestamp("2025-06-01"),
            altitud_celda_m=1800., tmax=25., tmin=10., lluvia=-1., radiacion=20., humedad=50.)])
        with self.assertRaisesRegex(SchemaError, "lluvia"):
            ESQUEMAS["clima_diario"].validate(tabla)
