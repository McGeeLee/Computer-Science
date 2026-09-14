import math
import tempfile
import unittest
from pathlib import Path

from solutions import chapter15


class Chapter15Tests(unittest.TestCase):
    def test_registry(self): self.assertEqual(list(chapter15.EXERCISES),[f"15.{i}" for i in range(1,37)])
    def test_recursive_numbers(self):
        self.assertEqual(chapter15.ex_15_1(234),9); self.assertEqual(chapter15.ex_15_2(10),55); self.assertEqual(chapter15.ex_15_3(24,18),6)
        self.assertAlmostEqual(chapter15.ex_15_4(3),1+1/2+1/3); self.assertAlmostEqual(chapter15.ex_15_5(3),1/3+2/5+3/7); self.assertAlmostEqual(chapter15.ex_15_6(3),1/2+2/3+3/4)
        self.assertEqual(chapter15.ex_15_7(5),(5,15)); self.assertEqual(chapter15.ex_15_18(5),31)
    def test_recursive_strings_and_lists(self):
        self.assertEqual(chapter15.ex_15_8(12345),"54321"); self.assertEqual(chapter15.ex_15_9("abcd"),"dcba"); self.assertEqual(chapter15.ex_15_10("Welcome","e"),2); self.assertEqual(chapter15.ex_15_12([1,9,3]),9); self.assertEqual(chapter15.ex_15_13("Good MorninG"),3); self.assertEqual(chapter15.ex_15_15(list("aBCdE")),3)
    def test_recursive_conversions_and_permutations(self):
        self.assertEqual(chapter15.ex_15_19(123),"1111011"); self.assertEqual(chapter15.ex_15_20(123),"7B"); self.assertEqual(chapter15.ex_15_21("1111011"),123); self.assertEqual(chapter15.ex_15_22("7B"),123); self.assertEqual(set(chapter15.ex_15_23("abc")),{"abc","acb","bac","bca","cab","cba"})
    def test_recursive_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/"one.txt").write_text("cat cat"); (root/"sub").mkdir(); (root/"sub"/"two.txt").write_text("a cat")
            self.assertEqual(chapter15.ex_15_24(root),2); self.assertEqual(chapter15.ex_15_28(root,"cat"),3)
    def test_fractal_generators(self):
        self.assertEqual(len(chapter15.sierpinski_triangles(3,((0,0),(1,0),(0,1)))),27); self.assertEqual(len(chapter15.koch_points(2,0+0j,1+0j)),17); self.assertEqual(len(chapter15.h_tree_lines(2,0,0,10)),63); self.assertEqual(len(chapter15.recursive_tree_lines(3,0,0,10)),15); self.assertEqual(len(chapter15.hilbert_points(3)),64); self.assertEqual(len(chapter15.ex_15_27()),92)


if __name__=="__main__": unittest.main()
