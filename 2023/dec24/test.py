import unittest
from solution import part1, part2, Fraction, solve_linear_system


class TestDec23(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt", least=7, most=27), 2)

    def test_gauss_jordan_matrix_inversion(self):
        matrix = [
            [2, -1, 0],
            [-1, 2, -1],
            [0, -1, 2],
        ]
        identity = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
        res = solve_linear_system(matrix, identity)
        expected = [
            [Fraction(3, 4), Fraction(1, 2), Fraction(1, 4)],
            [Fraction(1, 2), Fraction(1), Fraction(1, 2)],
            [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)],
        ]
        self.assertEqual(res, expected)

    def test_gauss_jordan_linear_system(self):
        A = [
            [2, 1, -1],
            [-3, -1, 2],
            [-2, 1, 2],
        ]
        c = [[8], [-11], [-3]]
        x = solve_linear_system(A, c)
        expected = [
            [Fraction(2)],
            [Fraction(3)],
            [Fraction(-1)],
        ]
        self.assertEqual(x, expected)

    def test_part2(self):
        self.assertEqual(part2("test.txt"), 47)


if __name__ == "__main__":
    unittest.main()
