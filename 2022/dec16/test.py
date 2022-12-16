import unittest
from solution import calculate_part1, calculate_part2;

class TestDec16(unittest.TestCase):

    file = "test.txt"

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file), 1651)

    def test_part2(self):
        self.assertEqual(calculate_part2(self.file), 1707)

if __name__ == '__main__':
    unittest.main()
