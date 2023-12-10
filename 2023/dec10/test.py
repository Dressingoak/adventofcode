import unittest
from solution import part1


class TestDec9(unittest.TestCase):
    def test_part1_1(self):
        self.assertEqual(part1("test.txt"), 4)

    def test_part1_2(self):
        self.assertEqual(part1("test2.txt"), 8)


if __name__ == "__main__":
    unittest.main()
