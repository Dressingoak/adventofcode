import unittest
from solution import part1


class TestDec19(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(part1("test.txt"), 0)


if __name__ == "__main__":
    unittest.main()
