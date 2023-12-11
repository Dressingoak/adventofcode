import unittest
from solution import part1, parse_and_expand


class TestDec11(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 374)

    def test_part2_1(self):
        self.assertEqual(parse_and_expand("test.txt", 9), 1030)

    def test_part2_2(self):
        self.assertEqual(parse_and_expand("test.txt", 99), 8410)


if __name__ == "__main__":
    unittest.main()
