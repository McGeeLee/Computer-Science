import math
import random
import unittest

from solutions import chapter06


class Chapter06Tests(unittest.TestCase):
    def test_registry_is_complete(self):
        self.assertEqual(list(chapter06.EXERCISES), [f"6.{i}" for i in range(1, 49)])

    def test_basic_functions(self):
        self.assertEqual([chapter06.ex_6_1(i) for i in range(1, 5)], [1, 5, 12, 22])
        self.assertEqual(chapter06.ex_6_2(234), 9)
        self.assertTrue(chapter06.ex_6_3(12321))
        self.assertEqual(chapter06.ex_6_4(3456), 6543)
        self.assertEqual(chapter06.ex_6_5(3, 2.4, 5), (2.4, 3, 5))
        self.assertAlmostEqual(chapter06.ex_6_7(10_000, 0.05 / 12, 5), 12_833.59, places=2)
        self.assertAlmostEqual(chapter06.celsius_to_fahrenheit(40), 104)
        self.assertAlmostEqual(chapter06.meter_to_foot(20), 65.57377, places=5)
        self.assertEqual(chapter06.ex_6_10(), 1229)
        self.assertEqual(chapter06.ex_6_12("1", "Z", 10)[0], "1 2 3 4 5 6 7 8 9 :")
        self.assertAlmostEqual(chapter06.ex_6_14(901), 3.1427, places=4)
        self.assertEqual(chapter06.ex_6_16(2020), 366)
        self.assertAlmostEqual(chapter06.ex_6_17(1, 1, 1), math.sqrt(3) / 4)
        self.assertIsNone(chapter06.ex_6_17(1, 3, 1))

    def test_number_theory(self):
        self.assertAlmostEqual(chapter06.ex_6_21(2), math.sqrt(2), places=4)
        self.assertEqual(chapter06.ex_6_23(555_550_000), "154:19:10")
        palindromic = chapter06.ex_6_24()
        self.assertEqual(len(palindromic), 100)
        self.assertEqual(palindromic[:5], (2, 3, 5, 7, 11))
        emirps = chapter06.ex_6_25()
        self.assertEqual(emirps[:5], (13, 17, 31, 37, 71))
        self.assertIn((31, 2**31 - 1), chapter06.ex_6_26())
        self.assertIn((3, 5), chapter06.ex_6_27())

    def test_games_and_validation(self):
        self.assertTrue(chapter06.ex_6_28([(5, 6)])[0])
        self.assertFalse(chapter06.ex_6_28([(1, 2)])[0])
        self.assertTrue(chapter06.ex_6_28([(4, 4), (6, 2)])[0])
        self.assertFalse(chapter06.ex_6_29("4388576018402626"))
        # PDF 的 OCR 丢失了一位；印刷原文的有效示例是 4388576018410707。
        self.assertTrue(chapter06.ex_6_29("4388576018410707"))
        wins = chapter06.ex_6_30(1000, random.Random(3))
        self.assertTrue(400 < wins < 600)

    def test_later_functions(self):
        self.assertAlmostEqual(chapter06.ex_6_33(5.5), 52.0444413678)
        self.assertAlmostEqual(chapter06.ex_6_34(5, 6.5), 72.6901701749)
        self.assertEqual(len(chapter06.ex_6_36(100, random.Random(1))), 100)
        self.assertEqual(chapter06.ex_6_48(34, 5), "00034")
        self.assertEqual(chapter06.ex_6_48(34, 1), "34")


if __name__ == "__main__":
    unittest.main()
