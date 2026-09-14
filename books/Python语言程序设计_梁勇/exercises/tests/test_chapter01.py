import math
import unittest

from solutions import chapter01


class Chapter01Tests(unittest.TestCase):
    def test_exercise_registry_is_complete(self):
        self.assertEqual(
            list(chapter01.EXERCISES),
            [f"1.{number}" for number in range(1, 22)],
        )

    def test_fixed_output_exercises(self):
        self.assertEqual(len(chapter01.ex_1_1()), 3)
        self.assertEqual(chapter01.ex_1_2(), ("Welcome to Python",) * 5)
        self.assertIn("FFFFFFF", chapter01.ex_1_3())
        self.assertEqual(chapter01.ex_1_4()[-1], (4, 16, 64))
        self.assertAlmostEqual(chapter01.ex_1_5(), 35.25 / 42)
        self.assertEqual(chapter01.ex_1_6(), 45)

    def test_numeric_exercises(self):
        pi4, pi8 = chapter01.ex_1_7()
        self.assertAlmostEqual(pi4, 4 * (1 - 1 / 3 + 1 / 5 - 1 / 7))
        self.assertLess(abs(pi8 - math.pi), abs(pi4 - math.pi))
        area, perimeter = chapter01.ex_1_8()
        self.assertAlmostEqual(area, 5.5**2 * math.pi)
        self.assertAlmostEqual(perimeter, 11 * math.pi)
        area, perimeter = chapter01.ex_1_9()
        self.assertAlmostEqual(area, 35.55)
        self.assertAlmostEqual(perimeter, 24.8)
        self.assertAlmostEqual(chapter01.ex_1_10(), 11.538461538461538)

    def test_population_prediction(self):
        populations = chapter01.ex_1_11()
        self.assertEqual(len(populations), 5)
        self.assertTrue(all(a < b for a, b in zip(populations, populations[1:])))
        self.assertEqual(populations[-1], 325_932_966)


if __name__ == "__main__":
    unittest.main()
