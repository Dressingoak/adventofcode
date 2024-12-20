import unittest
from solution import solve


class TestDec20(unittest.TestCase):

    def test_solve(self):
        saves = sorted((a, b) for a, b in solve("test.txt", 2).items() if a > 0)
        self.assertEqual(
            saves,
            [
                (2, 14),
                (4, 14),
                (6, 2),
                (8, 4),
                (10, 2),
                (12, 3),
                (20, 1),
                (36, 1),
                (38, 1),
                (40, 1),
                (64, 1),
            ],
        )


if __name__ == "__main__":
    unittest.main()
