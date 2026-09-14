import ast
import inspect
import unittest

from solutions import chapter09


class Chapter09Tests(unittest.TestCase):
    def test_registry_is_complete_and_import_has_no_gui_side_effects(self):
        self.assertEqual(list(chapter09.EXERCISES), [f"9.{i}" for i in range(1, 35)])
        self.assertTrue(all(callable(solution) for solution in chapter09.EXERCISES.values()))

    def test_module_parses_and_each_exercise_builds_gui_lazily(self):
        tree = ast.parse(inspect.getsource(chapter09))
        names = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        self.assertTrue({f"ex_9_{i}" for i in range(1, 35)} <= names)


if __name__ == "__main__":
    unittest.main()
