import sys
sys.path.append('../')
from timing import print_timing

def to_num(v):
    match v:
        case 'A' | 'X': return 0
        case 'B' | 'Y': return 1
        case 'C' | 'Z': return 2

@print_timing
def calculate_part1(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            (opponent, player) = line.strip().split(" ")
            v2, v1 = to_num(opponent), to_num(player)
            s += (v1 - v2 + 1) % 3 * 3 + v1 + 1
    return s

@print_timing
def calculate_part2(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            (opponent, outcome) = line.strip().split(" ")
            v2, o = to_num(opponent), to_num(outcome)
            v1 = (v2 + o - 1) % 3
            s += o * 3 + v1 + 1
    return s
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 2, part 1: {} (took {})".format(*calculate_part1(file)))
    print("Dec 2, part 2: {} (took {})".format(*calculate_part2(file)))
