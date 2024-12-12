import unittest
from solution import part1


class TestDec11(unittest.TestCase):
    def test_part1_a(self):
        self.assertEqual(part1("test.txt"), 140)

    def test_part1_b(self):
        self.assertEqual(part1("test2.txt"), 772)

    def test_part1_c(self):
        self.assertEqual(part1("test3.txt"), 1930)


if __name__ == "__main__":
    unittest.main()
