import sys
sys.path.append('../')
import os
import unittest
from dec6.solution import first_n_distinct, calculate_part1, calculate_part2

class TestDec6(unittest.TestCase):

    file = os.path.join(os.path.dirname(__file__), "test.txt")

    def test_example1_4(self):
        self.assertEqual(first_n_distinct("bvwbjplbgvbhsrlpgdmjqwftvncz", 4), 5)

    def test_example2_4(self):
        self.assertEqual(first_n_distinct("nppdvjthqldpwncqszvftbrmjlhg", 4), 6)

    def test_example3_4(self):
        self.assertEqual(first_n_distinct("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4), 10)

    def test_example4_4(self):
        self.assertEqual(first_n_distinct("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4), 11)

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file), 7)

    def test_example1_14(self):
        self.assertEqual(first_n_distinct("bvwbjplbgvbhsrlpgdmjqwftvncz", 14), 23)

    def test_example2_14(self):
        self.assertEqual(first_n_distinct("nppdvjthqldpwncqszvftbrmjlhg", 14), 23)

    def test_example3_14(self):
        self.assertEqual(first_n_distinct("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14), 29)

    def test_example4_14(self):
        self.assertEqual(first_n_distinct("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14), 26)


    def test_part2(self):
        self.assertEqual(calculate_part2(self.file), 19)

if __name__ == '__main__':
    unittest.main()
