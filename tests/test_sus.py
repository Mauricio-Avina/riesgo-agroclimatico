import unittest

from src.app.sus import exito, puntuar


class PruebaSUS(unittest.TestCase):
    def test_anclas(self):
        self.assertEqual(puntuar([3]*10), 50)
        self.assertEqual(puntuar([5,1]*5), 100)
        self.assertEqual(puntuar([1,5]*5), 0)
        with self.assertRaises(ValueError):
            puntuar([3]*9)

    def test_tarea_sin_observar_y_con_ayuda(self):
        t = dict(completada="si", segundos="160", errores="0", ayuda="no", bloqueo_mas_120s="no")
        self.assertEqual(exito(t), 1)
        self.assertEqual(exito(t | {"ayuda":"si"}), 0)
        self.assertEqual(exito(t | {"bloqueo_mas_120s":"si"}), 0)
        self.assertEqual(exito(t | {"segundos":""}), "")
