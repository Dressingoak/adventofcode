import sys
sys.path.append('../')
from puzzle import Puzzle

def to_range(lst: str) -> tuple[int, int]:
    l, r = lst.split("-")
    return (int(l), int(r))

def overlaps_fully(e1, e2, flip=True):
    match (e1, e2, flip):
        case ((l1, l2), (r1, r2), _) if l1 <= r1 and l2 >= r2: return True
        case (l, r, True): return overlaps_fully(r, l, False)
        case _: return False

def overlaps_partially(e1, e2, flip=True):
    match (e1, e2, flip):
        case (l, r, _) if overlaps_fully(l, r, False): return True
        case ((l1, l2), (r1, r2), _) if l1 <= r1 and l2 >= r1 and l2 < r2: return True
        case (l, r, True): return overlaps_partially(r, l, False)
        case _: return False

def calculate_part1(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            e1, e2 = [to_range(_) for _ in line.strip().split(",")]
            s += int(overlaps_fully(e1, e2))
    return s

def calculate_part2(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            e1, e2 = [to_range(_) for _ in line.strip().split(",")]
            s += int(overlaps_partially(e1, e2))
    return s
    
puzzle = Puzzle(__file__)

puzzle.add_part(1, calculate_part1)
puzzle.add_part(2, calculate_part2)

if __name__ == '__main__':
    puzzle.run()
