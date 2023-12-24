import unittest
from solution import part1, part2


class TestDec23(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt", least=7, most=27), 2)

    def test_part2(self):
        self.assertEqual(part2("test.txt"), 47)


if __name__ == "__main__":
    unittest.main()
