import unittest
from solution import part1


class TestDec18(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 62)


if __name__ == "__main__":
    unittest.main()