import unittest

from solutions import chapter02


class Chapter02Tests(unittest.TestCase):
    def test_registry_is_complete(self):
        self.assertEqual(list(chapter02.EXERCISES), [f"2.{i}" for i in range(1, 27)])

    def test_conversions_and_finance(self):
        self.assertAlmostEqual(chapter02.ex_2_1(43), 109.4)
        area, volume = chapter02.ex_2_2(5.5, 12)
        self.assertAlmostEqual(area, 95.03317777109125)
        self.assertAlmostEqual(volume, 1140.398133253095)
        self.assertAlmostEqual(chapter02.ex_2_3(16.5), 5.0325)
        self.assertAlmostEqual(chapter02.ex_2_4(55.5), 25.197)
        self.assertEqual(tuple(round(v, 2) for v in chapter02.ex_2_5(15.69, 15)), (2.35, 18.04))
        self.assertAlmostEqual(chapter02.ex_2_11(1000, 4.25, 5), 808.8639197424636)
        self.assertEqual(int(chapter02.ex_2_19(1000, 4.25, 1) * 100) / 100, 1043.33)
        self.assertAlmostEqual(chapter02.ex_2_20(1000, 3.5), 2.9166666667)
        self.assertAlmostEqual(chapter02.ex_2_21(100), 608.81, places=2)

    def test_numeric_problems(self):
        self.assertEqual(chapter02.ex_2_6(999), 27)
        self.assertEqual(chapter02.ex_2_7(1_000_000_000), (1902, 214))
        self.assertEqual(chapter02.ex_2_8(55.5, 3.5, 10.5), 1_625_484)
        self.assertAlmostEqual(chapter02.ex_2_9(5.3, 6), -5.56707, places=5)
        self.assertAlmostEqual(chapter02.ex_2_10(60, 3.5), 514.2857142857)
        self.assertEqual(chapter02.ex_2_12()[-1], (5, 6, 15625))
        self.assertEqual(chapter02.ex_2_13(5213), (3, 1, 2, 5))
        self.assertAlmostEqual(chapter02.ex_2_14((1.5, -3.4, 4.6, 5, 9.5, -3.4)), 33.6, places=1)
        # 正确公式得 78.5918；书中示例 78.5895 是已知的舍入/排印偏差。
        self.assertAlmostEqual(chapter02.ex_2_15(5.5), 78.59, places=2)
        self.assertAlmostEqual(chapter02.ex_2_16(5.5, 50.9, 4.5), 10.0889, places=4)
        self.assertAlmostEqual(chapter02.ex_2_17(95.5, 50), 26.8573, places=4)
        self.assertEqual(chapter02.ex_2_18(-5, timestamp=0), (19, 0, 0))
        self.assertEqual(chapter02.ex_2_22(5), 325_932_970)

    def test_validation(self):
        with self.assertRaises(ValueError):
            chapter02.ex_2_6(-1)
        with self.assertRaises(ValueError):
            chapter02.ex_2_9(50, 10)
        with self.assertRaises(ValueError):
            chapter02.ex_2_10(60, 0)


if __name__ == "__main__":
    unittest.main()
