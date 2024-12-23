import unittest
from solution import part1


class TestDec23(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(part1("test.txt"), 7)


if __name__ == "__main__":
    unittest.main()
