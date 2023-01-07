import unittest
from solution import calculate_part1

class TestDec25(unittest.TestCase):

    file = "test.txt"

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file)[0], "2=-1=0")

if __name__ == '__main__':
    unittest.main()
