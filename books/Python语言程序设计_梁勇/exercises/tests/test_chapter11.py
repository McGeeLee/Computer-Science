import unittest

from solutions import chapter11


class Chapter11Tests(unittest.TestCase):
    def test_registry(self):
        self.assertEqual(list(chapter11.EXERCISES), [f"11.{number}" for number in range(1, 53)])

    def test_matrix_arithmetic(self):
        matrix=[[1.5,2,3,4],[5.5,6,7,8],[9.5,1,3,1]]
        self.assertEqual([chapter11.ex_11_1(matrix,c) for c in range(4)],[16.5,9,13,13])
        self.assertEqual(chapter11.ex_11_2([[1,2],[3,4]]),5)
        self.assertEqual(chapter11.ex_11_5([[1,2],[3,4]],[[5,6],[7,8]]),[[6,8],[10,12]])
        self.assertEqual(chapter11.ex_11_6([[1,2,3]],[[1],[2],[3]]),[[14]])
        self.assertEqual(chapter11.ex_11_13([[23.5,35,2,10],[4.5,3,45,3.5],[3.5,44,5.5,12.6]]),[1,2])

    def test_geometry_and_sequences(self):
        pair=chapter11.ex_11_7([[0,0,0],[4,0,0],[1,0,0]])
        self.assertEqual(pair[:2],(0,2)); self.assertAlmostEqual(pair[2],1)
        self.assertTrue(chapter11.ex_11_15([[1,1],[2,2],[3,3],[4,4]]))
        self.assertEqual(chapter11.ex_11_30([[9,4],[3,-5]],[-6,-21]),[-2,3])
        self.assertEqual(chapter11.ex_11_31([[0,0],[2,2],[0,2],[2,0]]),[1,1])
        self.assertEqual(chapter11.ex_11_32([[0,0],[3,0],[0,4]]),6)
        self.assertEqual(chapter11.ex_11_34([[5.6,-7],[6.5,-7],[8,1]]),[6.5,-7])

    def test_games_and_patterns(self):
        game=chapter11.ex_11_9(); game.play(0,0); game.play(1,0); game.play(0,1); game.play(1,1); game.play(0,2); self.assertEqual(game.winner,"X")
        connect=chapter11.ex_11_20()
        for column in (0,0,1,1,2,2,3): connect.drop(column)
        self.assertEqual(connect.winner,"R")
        self.assertTrue(chapter11.ex_11_19([[1,1,1,1],[0,2,3,4]]))
        self.assertEqual(chapter11.ex_11_11(7),[["H","H","H"],["H","H","H"],["T","T","T"]])

    def test_sudoku_and_matrix_properties(self):
        grid=[[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]
        answer=chapter11.sudoku_solutions(grid,1)[0]
        self.assertTrue(chapter11.ex_11_24(answer))
        self.assertTrue(chapter11.ex_11_25([[.15,.875,.375],[.55,.005,.225],[.30,.12,.4]]))
        self.assertTrue(chapter11.ex_11_52([list("ABC"),list("BCA"),list("CAB")]))
        self.assertEqual(chapter11.largest_square_block([[1,1,0],[1,1,0],[0,0,1]]),(0,0,2))

    def test_banks_and_tax(self):
        balances=[25,125,175,75,181]
        loans=[[0,100.5,0,0,320.5],[0,0,40,85,0],[125,0,0,75,0],[125,0,0,0,0],[0,0,125,0,0]]
        self.assertEqual(chapter11.ex_11_17(balances,loans,201),[3,1])
        self.assertAlmostEqual(chapter11.ex_11_12(0,400000),117683.5)


if __name__ == "__main__": unittest.main()
