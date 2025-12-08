import unittest
from solution import part1


class TestDec8(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt", connections=10), 40)


if __name__ == "__main__":
    unittest.main()
