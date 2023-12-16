import unittest
from solution import part1


class TestDec16(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 46)


if __name__ == "__main__":
    unittest.main()
