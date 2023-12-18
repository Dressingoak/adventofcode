import unittest
from solution import part1, part2


class TestDec17(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("test.txt"), 102)

    def test_part2a(self):
        self.assertEqual(part2("test.txt"), 94)

    def test_part2b(self):
        self.assertEqual(part2("test2.txt"), 71)


if __name__ == "__main__":
    unittest.main()
