import sys

def calculate_part1(file: str):
    sides = 0
    adj = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    seen = set()
    with open(file, "r") as f:
        for line in f.readlines():
            match line.strip().split(","):
                case [x, y, z]:
                    x, y, z = int(x), int(y), int(z)
                    sides += 6
                    for (dx, dy, dz) in adj:
                        if (x + dx, y + dy, z + dz) in seen:
                            sides -= 2
                    seen.add((x, y, z))
    return sides

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 18, part 1: {}".format(calculate_part1(file)))
    # print("Dec 18, part 2: {}".format(calculate_part2(file)))
