import unittest
from solution import part1, part2


class TestDec18(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(part1("test.txt", (6, 6), 12), 22)

    def test_part1(self):
        self.assertEqual(part2("test.txt", (6, 6)), "6,1")


if __name__ == "__main__":
    unittest.main()
