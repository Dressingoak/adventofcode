import unittest
from solution import part1, part2


class TestDec9(unittest.TestCase):
    def test_part1_1(self):
        self.assertEqual(part1("test.txt"), 4)

    def test_part1_2(self):
        self.assertEqual(part1("test2.txt"), 8)

    def test_part2_1(self):
        self.assertEqual(part2("test3a.txt"), 4)

    def test_part2_2(self):
        self.assertEqual(part2("test3b.txt"), 4)

    def test_part2_3(self):
        self.assertEqual(part2("test4.txt"), 8)

    def test_part2_3(self):
        self.assertEqual(part2("test5.txt"), 10)


if __name__ == "__main__":
    unittest.main()
