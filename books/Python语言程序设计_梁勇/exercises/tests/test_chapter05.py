import math
import random
import unittest

from solutions import chapter05


class Chapter05Tests(unittest.TestCase):
    def test_registry_is_complete(self):
        self.assertEqual(list(chapter05.EXERCISES), [f"5.{i}" for i in range(1, 56)])

    def test_basic_loops(self):
        self.assertEqual(chapter05.ex_5_1([1, 2, -1, 3, 0]), (3, 1, 5, 1.25))
        self.assertEqual(chapter05.ex_5_2([3, 7], [(1, 2), (3, 5)]), 1)
        self.assertEqual(chapter05.ex_5_3()[0], (1, 2.2))
        self.assertAlmostEqual(chapter05.ex_5_4()[-1][1], 16.09)
        self.assertEqual(chapter05.ex_5_8()[-1][0], 20)
        year_ten, total = chapter05.ex_5_9()
        self.assertAlmostEqual(year_ten, 10_000 * 1.05**10)
        self.assertGreater(total, year_ten * 4)
        self.assertEqual(chapter05.ex_5_11([80, 92, 75, 92, 89]), (92, 89))
        self.assertTrue(all(number % 30 == 0 for number in chapter05.ex_5_12()))
        self.assertTrue(all((n % 5 == 0) != (n % 6 == 0) for n in chapter05.ex_5_13()))
        self.assertEqual(chapter05.ex_5_14(), 110)
        self.assertEqual(chapter05.ex_5_15(), 22)
        self.assertEqual(chapter05.ex_5_16(125, 2525), 25)
        self.assertEqual(chapter05.ex_5_18(120), (2, 2, 2, 3, 5))

    def test_numeric_series(self):
        primes = chapter05.ex_5_22()
        self.assertEqual(primes[:5], (2, 3, 5, 7, 11))
        self.assertEqual(primes[-1], 997)
        rates = chapter05.ex_5_23(10_000, 5)
        self.assertEqual((rates[0][0], rates[-1][0]), (5.0, 8.0))
        payment, schedule = chapter05.ex_5_24(10_000, 1, 7)
        self.assertEqual(int(payment * 100) / 100, 865.26)
        self.assertAlmostEqual(schedule[-1][-1], 0.0)
        forward, backward = chapter05.ex_5_25()
        self.assertGreaterEqual(backward, forward)
        self.assertAlmostEqual(chapter05.ex_5_27([100_000])[-1][1], math.pi, places=4)
        self.assertAlmostEqual(chapter05.ex_5_28([100])[-1][1], math.e)
        self.assertTrue(all(year % 4 == 0 for year in chapter05.ex_5_29()))
        self.assertEqual(chapter05.ex_5_30(2013, 2)[-1], ("December", "Sunday"))
        self.assertAlmostEqual(chapter05.ex_5_32(100, 5, 6), 608.81, places=2)
        self.assertAlmostEqual(chapter05.ex_5_33(10_000, 5.75, 18)[-1], 10898.54, places=2)
        self.assertEqual(chapter05.ex_5_35(), (6, 28, 496, 8128))
        self.assertAlmostEqual(chapter05.ex_5_37(), math.sqrt(625) - 1)

    def test_simulations_and_statistics(self):
        sales = chapter05.ex_5_39()
        self.assertAlmostEqual(chapter05._commission(sales) + 5_000, 30_000)
        heads, tails = chapter05.ex_5_40(1000, random.Random(1))
        self.assertEqual(heads + tails, 1000)
        self.assertEqual(chapter05.ex_5_41([3, 5, 2, 5, 5, 5, 0]), (5, 4))
        self.assertAlmostEqual(chapter05.ex_5_42(100_000, random.Random(2)), 0.625, delta=0.01)
        self.assertEqual(len(chapter05.ex_5_43()), 21)
        self.assertEqual(chapter05.ex_5_44(10), "1010")
        self.assertEqual(chapter05.ex_5_45(255), "FF")
        mean, deviation = chapter05.ex_5_46([1, 2, 3, 4, 5.5, 5.6, 6, 7, 8, 9, 10])
        self.assertAlmostEqual(mean, 5.55454545)
        self.assertGreater(deviation, 0)


if __name__ == "__main__":
    unittest.main()
