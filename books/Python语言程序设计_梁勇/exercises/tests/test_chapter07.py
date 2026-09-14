import unittest

from solutions import chapter07


class Chapter07Tests(unittest.TestCase):
    def test_registry_and_geometry_classes(self):
        self.assertEqual(list(chapter07.EXERCISES), [f"7.{i}" for i in range(1, 11)])
        rectangle = chapter07.ex_7_1(4, 40)
        self.assertEqual((rectangle.getArea(), rectangle.getPerimeter()), (160, 88))
        polygons = chapter07.ex_7_5()
        self.assertEqual(polygons[1].getPerimeter(), 24)
        quadratic = chapter07.ex_7_6(1, 3, 1)
        self.assertAlmostEqual(quadratic.getRoot1(), -0.381966, places=5)
        linear = chapter07.ex_7_7(9, 4, 3, -5, -6, -21)
        self.assertEqual((linear.getX(), linear.getY()), (-2, 3))
        self.assertEqual(chapter07.ex_7_9((2, 2, 0, 0, 0, 2, 2, 0)), (1, 1))

    def test_domain_classes(self):
        stock = chapter07.ex_7_2()
        self.assertAlmostEqual(stock.getChangePercent(), -0.7317073171)
        account = chapter07.ex_7_3()
        self.assertEqual(account.getBalance(), 20_500)
        self.assertAlmostEqual(account.getMonthlyInterest(), 76.875)
        fans = chapter07.ex_7_4()
        self.assertTrue(fans[0].isOn())
        self.assertFalse(fans[1].isOn())
        watch = chapter07.StopWatch(); watch.stop()
        self.assertGreaterEqual(watch.getElapsedTime(), 0)
        clock = chapter07.ex_7_10(555_550)
        self.assertEqual((clock.getHour(), clock.getMinute(), clock.getSecond()), (10, 19, 10))


if __name__ == "__main__":
    unittest.main()
