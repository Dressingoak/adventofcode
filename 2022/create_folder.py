import sys
import os

if __name__ == '__main__':
    day = sys.argv[1]

    folder = f"dec{day}"

    os.mkdir(folder)

    f = open(f"{folder}/__init__.py", "a")
    f.close()
    
    f = open(f"{folder}/test.txt", "a")
    f.close()

    f = open(f"{folder}/solution.py", "a")
    f.write(f"""import sys
sys.path.append('../')
from puzzle import Puzzle

def calculate_part1(file: str):
    with open(file, "r") as f:
        pass
    return 0

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0

puzzle = Puzzle(__file__)

puzzle.add_part(1, calculate_part1)
# puzzle.add_part(2, calculate_part2)

if __name__ == '__main__':
    puzzle.run()
""")
    f.close()

    f = open(f"{folder}/test.py", "a")
    f.write(f"""import sys
sys.path.append('../')
import os
import unittest
from dec{day}.solution import calculate_part1 #, calculate_part2

class TestDec{day}(unittest.TestCase):

    file = os.path.join(os.path.dirname(__file__), "test.txt")

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file), 0)

    # def test_part2(self):
    #     self.assertEqual(calculate_part2(self.file), 0)

if __name__ == '__main__':
    unittest.main()
""")
    f.close()
