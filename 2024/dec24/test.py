import unittest
from solution import part1


class TestDec24(unittest.TestCase):

    def test_part1_a(self):
        self.assertEqual(part1("test.txt"), 4)

    def test_part1_b(self):
        self.assertEqual(part1("test2.txt"), 2024)


if __name__ == "__main__":
    unittest.main()
