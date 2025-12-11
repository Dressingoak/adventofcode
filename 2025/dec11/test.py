import unittest
from solution import part1, part2


class TestDec11(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 5)

    def test_part2(self):
        self.assertEqual(part2("test2.txt"), 2)


if __name__ == "__main__":
    unittest.main()
