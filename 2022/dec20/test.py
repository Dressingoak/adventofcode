import unittest
from solution import calculate_part1, calculate_part2;

class TestDec20(unittest.TestCase):

    file = "test.txt"

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file), 3)

    def test_part2(self):
        self.assertEqual(calculate_part2(self.file), 1623178306)

if __name__ == '__main__':
    unittest.main()
