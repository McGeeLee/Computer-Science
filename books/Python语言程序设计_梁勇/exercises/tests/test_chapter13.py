import tempfile
import unittest
from pathlib import Path

from solutions import chapter13


class Chapter13Tests(unittest.TestCase):
    def test_registry(self): self.assertEqual(list(chapter13.EXERCISES),[f"13.{i}" for i in range(1,18)])
    def test_text_file_exercises(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"test.txt"; path.write_text("good morning\nmorning all\n",encoding="utf-8")
            self.assertEqual(chapter13.ex_13_2(path),(25,4,2)); self.assertEqual(chapter13.ex_13_1(path,"morning"),2); self.assertEqual(path.read_text(),"good \n all\n")
            self.assertEqual(chapter13.ex_13_5(path,"good","hello"),1); self.assertIn("hello",path.read_text())
            generated=Path(directory)/"numbers.txt"; numbers=chapter13.ex_13_4(generated,20,seed=1); self.assertEqual(numbers,sorted(numbers)); self.assertEqual(len(numbers),20)
    def test_encryption_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/"in.bin"; encrypted=Path(directory)/"encrypted.bin"; output=Path(directory)/"out.bin"; source.write_bytes(bytes(range(256)))
            chapter13.ex_13_8(source,encrypted); chapter13.ex_13_9(encrypted,output); self.assertEqual(output.read_bytes(),source.read_bytes())
    def test_custom_exceptions(self):
        self.assertEqual(chapter13.ex_13_10(2,4),chapter13.Rational(1,2))
        with self.assertRaises(RuntimeError): chapter13.ex_13_10(1,0)
        with self.assertRaises(RuntimeError): chapter13.ex_13_11(1,2,9)
        with self.assertRaises(chapter13.TriangleError) as context: chapter13.ex_13_12(1,2,9)
        self.assertEqual(context.exception.getSide3(),9)
    def test_graph_and_salary(self):
        graph=chapter13.parse_graph("3\n0 0 0 1 2\n1 10 0 0\n2 5 10 0\n"); self.assertEqual(graph.edges,{(0,1),(0,2)})
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"Salary.txt"; chapter13.ex_13_16(path,50,seed=2); report=chapter13.ex_13_17(path); self.assertEqual(report["all"][0],50); self.assertEqual(sum(report[rank][0] for rank in ("assistant","associate","full")),50)
    def test_address_store(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"addresses.dat"; store=chapter13.AddressBookStore(path); store.add(chapter13.Address("A","B","C","D","1")); store.update(chapter13.Address("X","B","C","D","1")); self.assertEqual(chapter13.AddressBookStore(path).current().name,"X")


if __name__=="__main__": unittest.main()
