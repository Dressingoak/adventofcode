import sys
sys.path.append('../')
import os
import unittest
from dec17.solution import calculate_part1, calculate_part2

class TestDec17(unittest.TestCase):

    file = os.path.join(os.path.dirname(__file__), "test.txt")
    shape_file = os.path.join(os.path.dirname(__file__), "shapes.txt")

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file, self.shape_file), 3068)

    def test_part2(self):
        self.assertEqual(calculate_part2(self.file, self.shape_file), 1_514_285_714_288)

if __name__ == '__main__':
    unittest.main()
