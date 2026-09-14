import unittest

from solutions import chapter03


class Chapter03Tests(unittest.TestCase):
    def test_registry_is_complete(self):
        self.assertEqual(list(chapter03.EXERCISES), [f"3.{i}" for i in range(1, 20)])

    def test_geometry(self):
        self.assertAlmostEqual(chapter03.ex_3_1(5.5), 71.92, places=2)
        self.assertAlmostEqual(chapter03.ex_3_2(39.55, -116.25, 41.5, 87.37), 10691.7918, places=3)
        self.assertGreater(chapter03.ex_3_3(), 0)
        self.assertAlmostEqual(chapter03.ex_3_4(5.5), 52.0444413678)
        self.assertAlmostEqual(chapter03.ex_3_5(5, 6.5), 72.6901701749)

    def test_text_and_money(self):
        self.assertEqual(chapter03.ex_3_6(69), "E")
        self.assertEqual(chapter03.ex_3_7(timestamp=0), "A")
        self.assertEqual(
            chapter03.ex_3_8(1156),
            {"dollars": 11, "quarters": 2, "dimes": 0, "nickels": 1, "pennies": 1},
        )
        payroll = chapter03.ex_3_9("Smith", 10, 9.75, 0.20, 0.09)
        self.assertAlmostEqual(payroll["net_pay"], 69.225)
        self.assertEqual(chapter03.ex_3_10(), "αβγδεζηθ")
        self.assertEqual(chapter03.ex_3_11(3125), 5213)

    def test_validation(self):
        with self.assertRaises(ValueError):
            chapter03.ex_3_5(2, 5)
        with self.assertRaises(ValueError):
            chapter03.ex_3_6(128)


if __name__ == "__main__":
    unittest.main()
