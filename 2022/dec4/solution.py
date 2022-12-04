import sys

def to_range(lst: str) -> tuple[int, int]:
    l, r = lst.split("-")
    return (int(l), int(r))

def overlaps_fully(e1, e2, flip=False):
    if e1[0] <= e2[0] and e1[1] >= e2[1]:
        return 1
    elif flip:
        return overlaps_fully(e2, e1, False)
    else:
        return 0

def overlaps_partially(e1, e2, flip=False):
    if overlaps_fully(e1, e2, False) == 1:
        return 1
    elif e1[0] <= e2[0] and e1[1] >= e2[0] and e1[1] < e2[1]:
        return 1
    elif flip:
        return overlaps_partially(e2, e1, False)
    else:
        return 0

def calculate_part1(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            e1, e2 = [to_range(_) for _ in line.strip().split(",")]
            s += overlaps_fully(e1, e2, True)
    return s

def calculate_part2(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            e1, e2 = [to_range(_) for _ in line.strip().split(",")]
            s += overlaps_partially(e1, e2, True)
    return s
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 4, part 1: {}".format(calculate_part1(file)))
    print("Dec 4, part 2: {}".format(calculate_part2(file)))
