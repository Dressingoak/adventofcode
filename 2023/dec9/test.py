import unittest
from solution import part1, part2


class TestDec9(unittest.TestCase):
    def test_part1_1(self):
        self.assertEqual(part1("test.txt"), 114)

    def test_part1_1(self):
        self.assertEqual(part2("test.txt"), 114)


if __name__ == "__main__":
    unittest.main()
