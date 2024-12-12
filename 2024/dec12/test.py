import unittest
from solution import part1, part2


class TestDec11(unittest.TestCase):
    def test_part1_a(self):
        self.assertEqual(part1("test.txt"), 140)

    def test_part1_b(self):
        self.assertEqual(part1("testXO.txt"), 772)

    def test_part1_c(self):
        self.assertEqual(part1("test2.txt"), 1930)

    def test_part2_a(self):
        self.assertEqual(part2("test.txt"), 80)

    def test_part2_b(self):
        self.assertEqual(part2("testXO.txt"), 436)

    def test_part2_c(self):
        self.assertEqual(part2("test2.txt"), 1206)

    def test_part2_d(self):
        self.assertEqual(part2("testE.txt"), 236)

    def test_part2_e(self):
        self.assertEqual(part2("testAB.txt"), 368)


if __name__ == "__main__":
    unittest.main()
