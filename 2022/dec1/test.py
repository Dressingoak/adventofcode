import unittest
import click
from click.testing import CliRunner
from solution import calculate_part1, calculate_part2;

class TestDec1(unittest.TestCase):

    runner = CliRunner()
    file = "test.txt"

    def test_part1(self):
        self.assertEqual(calculate_part1.callback(self.file), 24000)

    def test_part2(self):
        self.assertEqual(calculate_part2.callback(self.file), 45000)

if __name__ == '__main__':
    unittest.main()
