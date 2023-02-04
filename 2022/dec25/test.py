import sys
sys.path.append('../')
import os
import unittest
from dec25.solution import calculate_part1

class TestDec25(unittest.TestCase):

    file = os.path.join(os.path.dirname(__file__), "test.txt")

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file), "2=-1=0")

if __name__ == '__main__':
    unittest.main()
