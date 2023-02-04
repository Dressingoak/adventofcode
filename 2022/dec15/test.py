import sys
sys.path.append('../')
import os
import unittest
from dec15.solution import calculate_part1, calculate_part2

class TestDec15(unittest.TestCase):

    file = os.path.join(os.path.dirname(__file__), "test.txt")

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file, 10), 26)

    def test_part2(self):
        self.assertEqual(calculate_part2(self.file, 20), 56000011)

if __name__ == '__main__':
    unittest.main()
