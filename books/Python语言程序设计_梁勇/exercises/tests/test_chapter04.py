import unittest

from solutions import chapter04


class Chapter04Tests(unittest.TestCase):
    def test_registry_matches_printed_questions(self):
        expected = [f"4.{i}" for i in range(1, 37)] + ["4.38", "4.39"]
        self.assertEqual(list(chapter04.EXERCISES), expected)
        self.assertNotIn("4.37", chapter04.EXERCISES)

    def test_algebra_and_dates(self):
        roots = chapter04.ex_4_1(1, 3, 1)
        self.assertAlmostEqual(roots[0], -0.381966, places=5)
        self.assertEqual(chapter04.ex_4_1(1, 2, 1), (-1.0,))
        self.assertEqual(chapter04.ex_4_1(1, 2, 3), ())
        self.assertEqual(chapter04.ex_4_3(9, 4, 3, -5, -6, -21), (-2.0, 3.0))
        self.assertIsNone(chapter04.ex_4_3(1, 2, 2, 4, 4, 5))
        self.assertEqual(chapter04.ex_4_5(1, 3), ("Monday", "Thursday"))
        self.assertEqual(chapter04.ex_4_11(2, 2000), 29)
        self.assertEqual(chapter04.ex_4_21(2013, 1, 25), "Friday")
        self.assertEqual(chapter04.ex_4_21(2012, 5, 12), "Saturday")

    def test_classification_and_games(self):
        bmi, category = chapter04.ex_4_6(140, 5, 10)
        self.assertAlmostEqual(bmi, 20.0877, places=4)
        self.assertEqual(category, "Normal")
        self.assertEqual(chapter04.ex_4_7(116), ("1 dollar", "1 dime", "1 nickel", "1 penny"))
        self.assertEqual(chapter04.ex_4_8(3, 1, 2), (1, 2, 3))
        self.assertEqual(chapter04.ex_4_9(50, 24.59, 25, 11.99), 2)
        self.assertEqual(chapter04.ex_4_12(10), (False, True, True))
        self.assertEqual(chapter04.ex_4_15(123, lottery=123), (123, 10_000))
        self.assertEqual(chapter04.ex_4_15(321, lottery=123), (123, 3_000))
        self.assertEqual(chapter04.ex_4_17(1, computer_choice=0)[-1], "win")
        self.assertAlmostEqual(chapter04.ex_4_18(6.81, 1, 10_000), 1468.43, places=2)

    def test_geometry(self):
        self.assertEqual(chapter04.ex_4_19(1, 1, 1), 3)
        self.assertIsNone(chapter04.ex_4_19(1, 3, 1))
        self.assertTrue(chapter04.ex_4_22(4, 5))
        self.assertFalse(chapter04.ex_4_22(9, 9))
        self.assertTrue(chapter04.ex_4_23(2, 2))
        self.assertFalse(chapter04.ex_4_23(6, 4))
        intersection = chapter04.ex_4_25((2, 2, 5, -1, 4, 2, -1, -2))
        self.assertAlmostEqual(intersection[0], 2.88889, places=4)
        self.assertAlmostEqual(intersection[1], 1.11111, places=4)
        self.assertTrue(chapter04.ex_4_26(121))
        self.assertTrue(chapter04.ex_4_27(100.5, 25.5))
        self.assertFalse(chapter04.ex_4_27(100.5, 50.5))
        self.assertEqual(chapter04.ex_4_28((2.5, 4, 2.5, 43), (1.5, 5, 0.5, 3)), "inside")
        self.assertEqual(chapter04.ex_4_29((0.5, 5.1, 13), (1, 1.7, 4.5)), "inside")
        self.assertEqual(chapter04.ex_4_31((3.4, 2), (6.5, 9.5), (-5, 4)), "left")
        self.assertTrue(chapter04.ex_4_32((1, 1), (2.5, 2.5), (1.5, 1.5)))

    def test_hex_and_time(self):
        self.assertEqual(chapter04.ex_4_30(-5, timestamp=0), (7, 0, 0, "PM"))
        self.assertEqual(chapter04.ex_4_33(11), "B")
        self.assertEqual(chapter04.ex_4_34("a"), 10)


if __name__ == "__main__":
    unittest.main()
