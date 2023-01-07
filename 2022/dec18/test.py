import unittest
from solution import count_sides;

class TestDec18(unittest.TestCase):

    file = "test.txt"

    def test_part1(self):
        self.assertEqual(count_sides(self.file, True)[0], 64)

    def test_part2(self):
        self.assertEqual(count_sides(self.file, False)[0], 58)

if __name__ == '__main__':
    unittest.main()
