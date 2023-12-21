import unittest
from solution import part1


class TestDec19(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt", steps=6), 16)


if __name__ == "__main__":
    unittest.main()
