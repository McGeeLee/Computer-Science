import unittest
from fractions import Fraction

from solutions import chapter08


class Chapter08Tests(unittest.TestCase):
    def test_registry_and_strings(self):
        self.assertEqual(list(chapter08.EXERCISES), [f"8.{i}" for i in range(1, 22)])
        self.assertTrue(chapter08.ex_8_1("111-22-3333"))
        self.assertFalse(chapter08.ex_8_1("11-122-3333"))
        self.assertEqual(chapter08.ex_8_2("gram", "programming"), 3)
        self.assertTrue(chapter08.ex_8_3("abc12345"))
        self.assertEqual(chapter08.ex_8_4("welcome", "e"), 2)
        self.assertEqual(chapter08.ex_8_5("system error, syntax error", "error"), 2)
        self.assertEqual(chapter08.ex_8_6("A1 b!"), 2)
        self.assertEqual(chapter08.ex_8_7("1-800-Flowers"), "1-800-3569377")
        self.assertEqual(chapter08.ex_8_8("10001"), 17)
        self.assertEqual(chapter08.ex_8_9("11111111"), "FF")
        self.assertEqual(chapter08.ex_8_10(17), "10001")
        self.assertEqual(chapter08.ex_8_11("abc"), "cba")
        self.assertEqual(chapter08.ex_8_12("TTATGTTTTAAGGATGGGGCGTTAGTT"), ("TTT", "GGGCGT"))
        self.assertEqual(chapter08.ex_8_13("distance", "disinfection"), "dis")

    def test_checksums(self):
        self.assertTrue(chapter08.ex_8_14("4388576018410707"))
        self.assertEqual(chapter08.ex_8_15("013601267"), "0136012671")
        self.assertEqual(chapter08.ex_8_15("013031997"), "013031997X")
        self.assertEqual(chapter08.ex_8_16("978013213080"), "9780132130806")
        self.assertEqual(chapter08.ex_8_16("978013213079"), "9780132130790")

    def test_geometry_and_numbers(self):
        first, second, distance, nearby = chapter08.ex_8_17(2.1, 2.3, 2.3, 4.2)
        self.assertAlmostEqual(distance, 1.91, places=2)
        self.assertTrue(nearby)
        c1, c2 = chapter08.Circle2D(5, 5.5, 10), chapter08.Circle2D(9, 1.3, 10)
        self.assertEqual(chapter08.ex_8_18(c1, c2)[2:], (True, False, True))
        r1, r2 = chapter08.Rectangle2D(9, 1.3, 10, 35.3), chapter08.Rectangle2D(1.3, 4.3, 4, 5.3)
        self.assertEqual(chapter08.ex_8_19(r1, r2)[2:], (False, False, False))
        self.assertEqual(chapter08.ex_8_20(), sum((Fraction(i, i + 1) for i in range(1, 10)), Fraction()))
        a, b = chapter08.Complex(3.5, 6.5), chapter08.Complex(-3.5, 1)
        added, subtracted, multiplied, divided, magnitude = chapter08.ex_8_21(a, b)
        self.assertEqual(added, chapter08.Complex(0, 7.5))
        self.assertEqual(multiplied, chapter08.Complex(-18.75, -19.25))
        self.assertAlmostEqual(divided.real, -0.43396226415)


if __name__ == "__main__":
    unittest.main()
