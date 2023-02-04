import sys
sys.path.append('../')
from puzzle import Puzzle

def first_n_distinct(chars: str, n: int) -> int:
    for i in range(n, len(chars)):
            if len(set(chars[i-n:i])) == n:
                return i

def calculate_part1(file: str):
    with open(file, "r") as f:
        line = f.readline()
        return first_n_distinct(line, 4)

def calculate_part2(file: str):
    with open(file, "r") as f:
        line = f.readline()
        return first_n_distinct(line, 14)
    
if __name__ == '__main__':

    puzzle = Puzzle(__file__)

    puzzle.add_part(1, calculate_part1)
    puzzle.add_part(2, calculate_part2)

    puzzle.run()
