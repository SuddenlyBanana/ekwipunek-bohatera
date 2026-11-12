import unittest

from main import Ekwipunek


class TestEkwipunek(unittest.TestCase):
    def test_kupowanie_odejmuje_zloto_i_dodaje_przedmiot(self):
        ekwipunek = Ekwipunek(zloto=20)

        sukces, _ = ekwipunek.kup("mikstura")

        self.assertTrue(sukces)
        self.assertEqual(ekwipunek.zloto, 10)
        self.assertEqual(ekwipunek.przedmioty["mikstura"], 1)

    def test_nie_mozna_kupic_bez_zlota(self):
        ekwipunek = Ekwipunek(zloto=0)

        sukces, _ = ekwipunek.kup("miecz")

        self.assertFalse(sukces)
        self.assertNotIn("miecz", ekwipunek.przedmioty)

    def test_nie_mozna_przekroczyc_limitu_wagi(self):
        ekwipunek = Ekwipunek(zloto=100, maksymalna_waga=3.0)

        sukces, _ = ekwipunek.kup("miecz")

        self.assertFalse(sukces)
        self.assertEqual(ekwipunek.aktualna_waga(), 0)

    def test_uzycie_usuwa_ostatnia_sztuke(self):
        ekwipunek = Ekwipunek({"mikstura": 1})

        sukces, _ = ekwipunek.uzyj("mikstura")

        self.assertTrue(sukces)
        self.assertNotIn("mikstura", ekwipunek.przedmioty)

    def test_sprzedaz_usuwa_przedmiot_i_dodaje_zloto(self):
        ekwipunek = Ekwipunek({"miecz": 1}, zloto=0)

        sukces, _ = ekwipunek.sprzedaj("miecz")

        self.assertTrue(sukces)
        self.assertEqual(ekwipunek.zloto, 15)
        self.assertNotIn("miecz", ekwipunek.przedmioty)


if __name__ == "__main__":
    unittest.main()
