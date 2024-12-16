import unittest
from solution import part1, part2


class TestDec15(unittest.TestCase):
    def test_part1_a(self):
        self.assertEqual(part1("test.txt"), 7036)

    def test_part1_b(self):
        self.assertEqual(part1("test2.txt"), 11048)

    def test_part2_1(self):
        self.assertEqual(part2("test.txt"), 45)

    def test_part2_b(self):
        self.assertEqual(part2("test2.txt"), 64)


if __name__ == "__main__":
    unittest.main()
