import unittest
from solution import solve


class TestDec11(unittest.TestCase):
    def test_solve_6(self):
        self.assertEqual(solve("test.txt", 6), 22)

    def test_solve_25(self):
        self.assertEqual(solve("test.txt", 25), 55312)


if __name__ == "__main__":
    unittest.main()
