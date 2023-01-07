import unittest
from solution import calculate

class TestDec9(unittest.TestCase):

    file1 = "test.txt"
    file2 = "test2.txt"

    def test_2knots_ex1(self):
        self.assertEqual(calculate(self.file1, 2)[0], 13)

    def test_10knots_ex1(self):
        self.assertEqual(calculate(self.file1, 10)[0], 1)

    def test_10knots_ex2(self):
        self.assertEqual(calculate(self.file2, 10)[0], 36)

if __name__ == '__main__':
    unittest.main()
