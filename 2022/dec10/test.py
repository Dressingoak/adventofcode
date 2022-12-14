import unittest
from solution import calculate_part1, calculate_part2;

class TestDec10(unittest.TestCase):

    file = "test.txt"

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file), 13140)

    def test_part2(self):
        self.assertEqual(calculate_part2(self.file), """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....""")

if __name__ == '__main__':
    unittest.main()