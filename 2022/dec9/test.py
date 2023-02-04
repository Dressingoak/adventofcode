import sys
sys.path.append('../')
import os
import unittest
from dec9.solution import calculate_part1, calculate_part2

class TestDec9(unittest.TestCase):

    file1 = os.path.join(os.path.dirname(__file__), "test.txt")
    file2 = os.path.join(os.path.dirname(__file__), "test2.txt")

    def test_2knots_ex1(self):
        self.assertEqual(calculate_part1(self.file1), 13)

    def test_10knots_ex1(self):
        self.assertEqual(calculate_part2(self.file1), 1)

    def test_10knots_ex2(self):
        self.assertEqual(calculate_part2(self.file2), 36)

if __name__ == '__main__':
    unittest.main()
