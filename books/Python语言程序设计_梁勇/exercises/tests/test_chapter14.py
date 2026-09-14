import tempfile
import unittest
from pathlib import Path

from solutions import chapter14


class Chapter14Tests(unittest.TestCase):
    def test_registry(self): self.assertEqual(list(chapter14.EXERCISES),[f"14.{i}" for i in range(1,12)])
    def test_keywords_ignore_comments_and_strings(self):
        source="if True:\n    text = 'for while'  # return\n    for x in []:\n        pass\n"
        self.assertEqual(chapter14.keyword_counts(source),{"True":1,"for":1,"if":1,"in":1,"pass":1})
    def test_modes(self): self.assertEqual(chapter14.ex_14_2([9,3,0,3,9,3,2,4,9]),[3,9])
    def test_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"text.txt"; path.write_text("Banana, apple; APPLE! rhythm",encoding="utf-8")
            self.assertEqual(chapter14.ex_14_8(path),["apple","banana","rhythm"])
            self.assertEqual(chapter14.ex_14_11(path),(7,15))
    def test_capital_quiz(self):
        quiz=chapter14.CapitalQuiz({"A":"One","B":"Two"},seed=1); state=quiz.current; self.assertTrue(quiz.answer(quiz.capitals[state].upper())); self.assertEqual(quiz.correct,1)


if __name__=="__main__": unittest.main()
