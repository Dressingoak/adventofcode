import unittest
from solution import solve


class TestDec20(unittest.TestCase):

    def test_part1(self):
        self.assertEqual(solve("test.txt", 2, 1), 44)

    def test_part2(self):
        self.assertEqual(solve("test.txt", 20, 50), 285)


if __name__ == "__main__":
    unittest.main()
