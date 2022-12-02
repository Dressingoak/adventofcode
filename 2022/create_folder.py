import sys
import os

if __name__ == '__main__':
    day = sys.argv[1]

    folder = f"dec{day}"

    os.mkdir(folder)
    
    f = open(f"{folder}/test.txt", "a")
    f.close()

    f = open(f"{folder}/solution.py", "a")
    f.write(f"""import sys

def calculate_part1(file: str):
    with open(file, "r") as f:
        pass
    return 0

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec {day}, part 1: {{}}".format(calculate_part1(file)))
    # print("Dec {day}, part 2: {{}}".format(calculate_part2(file)))
""")
    f.close()

    f = open(f"{folder}/test.py", "a")
    f.write(f"""import unittest
from solution import calculate_part1 #, calculate_part2;

class TestDec{day}(unittest.TestCase):

    file = "test.txt"

    def test_part1(self):
        self.assertEqual(calculate_part1(self.file), 0)

    # def test_part2(self):
    #     self.assertEqual(calculate_part2(self.file), 0)

if __name__ == '__main__':
    unittest.main()
""")
    f.close()
