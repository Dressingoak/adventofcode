import unittest
from solution import part1, part2


class TestDec1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 11)


class TestDec2(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part2("test.txt"), 11)


if __name__ == "__main__":
    unittest.main()
