import unittest
from solution import part1


class TestDec13(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 480)


if __name__ == "__main__":
    unittest.main()
