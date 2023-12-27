import unittest
from solution import part1, parse, minimum_cut


class TestDec23(unittest.TestCase):
    def test_algorithm(self):
        G = {
            1: {2: 2, 5: 3},
            2: {1: 2, 3: 3, 5: 2, 6: 2},
            3: {2: 3, 4: 4, 7: 2},
            4: {3: 4, 7: 2, 8: 2},
            5: {1: 3, 2: 2, 6: 3},
            6: {2: 2, 5: 3, 7: 1},
            7: {3: 2, 4: 2, 6: 1, 8: 3},
            8: {4: 2, 7: 3},
        }
        min_cut, s1, s2 = minimum_cut(G, 2)
        self.assertEqual(min_cut, 4)
        self.assertEqual(s1, {3, 4, 7, 8})
        self.assertEqual(s2, {1, 2, 5, 6})

    def test_part1_groups(self):
        g = parse("test.txt")
        _, s1, s2 = minimum_cut(g)
        so1 = s1 if len(s1) > len(s2) else s2
        so2 = s2 if len(s1) > len(s2) else s1
        self.assertEqual(
            so1, {"cmg", "frs", "lhk", "lsr", "nvd", "pzl", "qnr", "rsh", "rzs"}
        )
        self.assertEqual(so2, {"bvb", "hfx", "jqt", "ntq", "rhn", "xhk"})

    def test_part1(self):
        self.assertEqual(part1("test.txt"), 54)


if __name__ == "__main__":
    unittest.main()
