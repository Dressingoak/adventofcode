import unittest
from solution import part1, part2


class TestDec1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 161)


class TestDec2(unittest.TestCase):
    def test_part2(self):
        self.assertEqual(part2("test2.txt"), 48)


if __name__ == "__main__":
    unittest.main()
