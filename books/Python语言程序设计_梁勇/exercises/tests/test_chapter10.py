import unittest

from solutions import chapter10


class Chapter10Tests(unittest.TestCase):
    def test_registry_is_complete(self):
        self.assertEqual(list(chapter10.EXERCISES), [f"10.{number}" for number in range(1, 42)])

    def test_basic_list_problems(self):
        self.assertEqual(chapter10.ex_10_1([40, 55, 70, 58]), ["C", "B", "A", "B"])
        self.assertEqual(chapter10.ex_10_3([2, 5, 6, 5, 4, 3, 23, 43, 2]), {2: 2, 3: 1, 4: 1, 5: 2, 6: 1, 23: 1, 43: 1})
        self.assertEqual(chapter10.ex_10_5([1, 2, 3, 2, 1, 6, 3, 4, 5, 2]), [1, 2, 3, 6, 4, 5])
        self.assertEqual(chapter10.ex_10_6(10), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
        self.assertEqual(sum(chapter10.ex_10_7(1000, seed=3)), 1000)

    def test_statistics_and_sorting(self):
        average, standard_deviation = chapter10.ex_10_9([1.9, 2.5, 3.7, 2, 1, 6, 3, 4, 5, 2])
        self.assertAlmostEqual(average, 3.11)
        self.assertAlmostEqual(standard_deviation, 1.55738, places=5)
        values = [3, 1, 2]; self.assertIs(chapter10.ex_10_10(values), values); self.assertEqual(values, [2, 1, 3])
        self.assertEqual(chapter10.ex_10_12([12, 18, 30]), 6)
        self.assertEqual(chapter10.ex_10_14([4, 2, 8, 1]), [1, 2, 4, 8])
        self.assertTrue(chapter10.ex_10_15([1, 2, 2, 4]))
        self.assertEqual(chapter10.ex_10_16([4, 3, 2, 1]), [1, 2, 3, 4])

    def test_games_and_number_problems(self):
        self.assertEqual(len(chapter10.ex_10_20()), 92)
        self.assertEqual(chapter10.ex_10_21(), [1, 4, 9, 16, 25, 36, 49, 64, 81, 100])
        paths, slots = chapter10.ex_10_19(20, 8, seed=1); self.assertEqual(len(paths), 20); self.assertEqual(sum(slots), 20)
        self.assertEqual(chapter10.ex_10_23([1, -3, 2]), [1.0, 2.0])
        self.assertEqual(chapter10.ex_10_26([1, 5, 16, 61, 111], [2, 4, 5, 6]), [1, 2, 4, 5, 5, 6, 16, 61, 111])
        self.assertTrue(chapter10.ex_10_27([1, 2, 2, 2, 2, 3]))
        values = [5, 2, 9, 3, 6, 8]; pivot = chapter10.ex_10_28(values); self.assertEqual(values[pivot], 5); self.assertTrue(all(v <= 5 for v in values[:pivot])); self.assertTrue(all(v > 5 for v in values[pivot + 1:]))

    def test_safe_24_point_validator(self):
        self.assertEqual(chapter10.verify_24_expression([13, 5, 10, 7], "(13-5)*(10-7)"), (True, "correct"))
        ok, _ = chapter10.verify_24_expression([13, 5, 10, 7], "__import__('os')")
        self.assertFalse(ok)
        ok, _ = chapter10.verify_24_expression([1, 2, 3, 4], "6*4")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
