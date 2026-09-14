import unittest

from solutions import chapter10, chapter12


class Chapter12Tests(unittest.TestCase):
    def test_registry(self): self.assertEqual(list(chapter12.EXERCISES),[f"12.{i}" for i in range(1,23)])
    def test_triangle_and_location(self):
        triangle=chapter12.ex_12_1(3,4,5,"blue",False); self.assertIsInstance(triangle,chapter12.GeometricObject); self.assertEqual(triangle.getArea(),6); self.assertEqual(triangle.getPerimeter(),12); self.assertEqual(triangle.getColor(),"blue"); self.assertFalse(triangle.isFilled())
        self.assertEqual(chapter12.ex_12_2([[1,2],[9,3]]),chapter12.Location(1,0,9))
    def test_atm_and_rectangle(self):
        atm=chapter12.ex_12_3(); self.assertEqual(atm.transact(4,"withdraw",3),97); self.assertEqual(atm.transact(4,"deposit",10),107)
        rectangle=chapter12.ex_12_4([[1,1],[5,7],[-1,3]]); self.assertEqual((rectangle.getX(),rectangle.getY(),rectangle.getWidth(),rectangle.getHeight()),(2,4,6,6))
    def test_stack_and_fractal_math(self):
        stack=chapter12.ex_12_16(["a","b"]); stack.push("c"); self.assertEqual(stack.peek(),"c"); self.assertEqual(stack.pop(),"c"); self.assertEqual(stack.getSize(),2)
        self.assertEqual(chapter12.ex_12_14(0j),chapter12.COUNT_LIMIT); self.assertLess(chapter12.ex_12_14(2+2j),chapter12.COUNT_LIMIT)
    def test_24_solver(self):
        expression=chapter12.solve_24([13,5,10,7]); self.assertIsNotNone(expression); self.assertEqual(chapter10.verify_24_expression([13,5,10,7],expression),(True,"correct"))
        self.assertIsNone(chapter12.solve_24([1,1,1,1]))


if __name__=="__main__": unittest.main()
