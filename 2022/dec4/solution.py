import sys
sys.path.append('../')
from timing import print_timing

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

@print_timing
def calculate_part1(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            e1, e2 = [to_range(_) for _ in line.strip().split(",")]
            s += int(overlaps_fully(e1, e2))
    return s

@print_timing
def calculate_part2(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            e1, e2 = [to_range(_) for _ in line.strip().split(",")]
            s += int(overlaps_partially(e1, e2))
    return s
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 4, part 1: {} (took {})".format(*calculate_part1(file)))
    print("Dec 4, part 2: {} (took {})".format(*calculate_part2(file)))
