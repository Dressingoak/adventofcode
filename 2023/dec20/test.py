import unittest
from solution import part1


class TestDec20(unittest.TestCase):
    def test_part1a(self):
        self.assertEqual(part1("test.txt"), 32000000)
    
    def test_part1b(self):
        self.assertEqual(part1("test.txt"), 11687500)


if __name__ == "__main__":
    unittest.main()
