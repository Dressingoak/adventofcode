import unittest
from solution import part1, part2


class TestDec23(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 94)

    def test_part2(self):
        self.assertEqual(part2("test.txt"), 154)


if __name__ == "__main__":
    unittest.main()
