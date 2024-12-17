import unittest
from solution import part1, part2


class TestDec17(unittest.TestCase):

    def test_part1(self):
        self.assertEqual(part1("test.txt"), "4,6,3,5,6,3,5,2,1,0")

    def test_part2(self):
        self.assertEqual(part2("test2.txt"), 117440)


if __name__ == "__main__":
    unittest.main()
