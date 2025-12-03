import unittest
from solution import part1


class TestDec3(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 357)


if __name__ == "__main__":
    unittest.main()
