import unittest
from solution import solve


class TestDec18(unittest.TestCase):

    def test_part1(self):
        self.assertEqual(solve("test.txt", (6, 6), 12), 22)


if __name__ == "__main__":
    unittest.main()
