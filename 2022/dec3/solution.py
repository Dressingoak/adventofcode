import sys
sys.path.append('../')
from puzzle import Puzzle

def priority(char: str) -> int:
    ascii = ord(char)
    if ascii >= 97 and ascii <= 122:
        return ascii - 96 # a..z => 1..27
    elif ascii >= 65 and ascii <= 90:
        return ascii - 38 # A..Z => 27..52

def calculate_part1(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            arrangement = line.strip()
            if arrangement == "":
                continue
            n = len(arrangement)
            m = n // 2
            match [_ for _ in  set(arrangement[0:m]).intersection(set(arrangement[m:n]))]:
                case [x]: s += priority(x)
                case _: raise Exception("Not exactly one common item!")
    return s

def calculate_part2(file: str):
    s = 0
    with open(file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != ""]
        for i in range(0, len(lines), 3):
            common = set(lines[i])
            [common.intersection_update(set(lines[j])) for j in range(i+1,i+3)]
            match [_ for _ in common]:
                case [x]: s += priority(x)
                case _: raise Exception("Not exactly one common item!")
    return s
    
if __name__ == '__main__':

    puzzle = Puzzle(__file__)

    puzzle.add_part(1, calculate_part1)
    puzzle.add_part(2, calculate_part2)

    puzzle.run()
