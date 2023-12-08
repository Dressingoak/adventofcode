import unittest
from solution import part1, part2


class TestDec8(unittest.TestCase):
    def test_part1_1(self):
        self.assertEqual(part1("test.txt"), 2)

    def test_part1_2(self):
        self.assertEqual(part1("test2.txt"), 6)

    def test_part2(self):
        self.assertEqual(part2("test3.txt"), 6)


if __name__ == "__main__":
    unittest.main()
