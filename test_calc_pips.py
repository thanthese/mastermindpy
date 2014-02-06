from unittest import TestCase

import mastermindpy as m


class TestCalc_pips(TestCase):
    def test_calc_pips(self):
        self.assertEqual({"black": 2, "white": 0}, m.calc_pips("bbaa", "bbzz"))
        self.assertEqual({"black": 4, "white": 0}, m.calc_pips("bbaa", "bbaa"))
        self.assertEqual({"black": 0, "white": 4}, m.calc_pips("bbaa", "aabb"))
        self.assertEqual({"black": 0, "white": 0}, m.calc_pips("bbaa", "zzzz"))
        self.assertEqual({"black": 1, "white": 1}, m.calc_pips("bbaa", "bazz"))
