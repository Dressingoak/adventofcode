import unittest
from solution import part1, part2


class TestDec19(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt", steps=6), 16)

    def test_part2a(self):
        self.assertEqual(part2("test.txt", steps=6), 16)

    def test_part2b(self):
        self.assertEqual(part2("test.txt", steps=10), 50)

    def test_part2c(self):
        self.assertEqual(part2("test.txt", steps=50), 1594)

    def test_part2d(self):
        self.assertEqual(part2("test.txt", steps=100), 6536)

    def test_part2e(self):
        self.assertEqual(part2("test.txt", steps=500), 167004)

    def test_part2f(self):
        self.assertEqual(part2("test.txt", steps=1000), 668697)

    def test_part2g(self):
        self.assertEqual(part2("test.txt", steps=5000), 16733044)


if __name__ == "__main__":
    unittest.main()
