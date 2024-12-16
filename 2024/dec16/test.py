import unittest
from solution import part1


class TestDec15(unittest.TestCase):
    def test_part1_a(self):
        self.assertEqual(part1("test.txt"), 7036)

    def test_part1_b(self):
        self.assertEqual(part1("test2.txt"), 11048)


if __name__ == "__main__":
    unittest.main()
