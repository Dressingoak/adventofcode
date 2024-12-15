import unittest
from solution import part1, part2


class TestDec15(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 10092)

    def test_part1_small(self):
        self.assertEqual(part1("test_small.txt"), 2028)

    def test_part2(self):
        self.assertEqual(part2("test.txt"), 9021)


if __name__ == "__main__":
    unittest.main()
