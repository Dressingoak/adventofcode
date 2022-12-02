import sys

def to_num(v):
    match v:
        case 'A' | 'X': return 0
        case 'B' | 'Y': return 1
        case 'C' | 'Z': return 2

def outcome(v1, v2):
    return (v1 - v2 + 1) % 3 * 3 + v1 + 1

def score(player: str, opponent: str) -> int:
    return outcome(to_num(player), to_num(opponent))

def calculate_part1(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            (opponent, player) = line.strip().split(" ")
            s += score(player, opponent)
    return s

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 2, part 1: {}".format(calculate_part1(file)))
    # print("Dec 2, part 2: {}".format(calculate_part2(file)))
