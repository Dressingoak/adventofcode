import unittest
from solution import part1, part2


class TestDec8(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 14)

    def test_part1(self):
        self.assertEqual(part2("test.txt"), 34)


if __name__ == "__main__":
    unittest.main()
