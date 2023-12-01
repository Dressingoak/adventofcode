import unittest
from solution import calculate_part1

class TestDec1(unittest.TestCase):

    def test_part1(self):
        self.assertEqual(calculate_part1("test.txt"), 142)

if __name__ == '__main__':
    unittest.main()
