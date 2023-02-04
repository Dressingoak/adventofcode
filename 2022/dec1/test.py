import sys
sys.path.append('../')
import os
import unittest
from dec1.solution import calculate_part1, calculate_part2

class TestDec1(unittest.TestCase):

    file = os.path.join(os.path.dirname(__file__), "test.txt")

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file), 24000)

    def test_part2(self):
        self.assertEqual(calculate_part2(self.file), 45000)

if __name__ == '__main__':
    unittest.main()
