import unittest
from solution import part1, part2


class TestDec8(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt", connections=10), 40)

    def test_part2(self):
        self.assertEqual(part2("test.txt"), 25272)


if __name__ == "__main__":
    unittest.main()
