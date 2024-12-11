import unittest
from solution import part1


class TestDec11(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 55312)


if __name__ == "__main__":
    unittest.main()
