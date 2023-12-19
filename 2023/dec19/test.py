import unittest
from solution import part1, part2


class TestDec19(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 19114)

    def test_part2(self):
        self.assertEqual(part2("test.txt"), 167409079868000)


if __name__ == "__main__":
    unittest.main()
