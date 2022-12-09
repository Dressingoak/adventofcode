import sys

def dist(p1, p2):
    return abs(p2[0] - p1[0]) - abs(p2[1] - p1[1])

def in_range(p1, p2):
    for i in range(p1[0]-1, p1[0]+2):
        for j in range(p1[1]-1, p1[1]+2):
            if (i, j) == p2:
                return True
    return False

def calculate_part1(file: str):
    positions = set()
    h, t = (0, 0), (0, 0)
    positions.add(t)
    with open(file, "r") as f:
        for line in f.readlines():
            (dir, steps) = line.strip().split(" ")
            for _ in range(int(steps)):
                match dir:
                    case "L" | "R":
                        d = 1 if dir == "R" else -1
                        h = (h[0] + d, h[1])
                        if not in_range(h, t):
                            t = (t[0] + d, t[1] + h[1] - t[1])
                    case "U" | "D":
                        d = 1 if dir == "U" else -1
                        h = (h[0], h[1] + d)
                        if not in_range(h, t):
                            t = (t[0] + h[0] - t[0], t[1] + d)
                positions.add(t)
    return len(positions)

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 9, part 1: {}".format(calculate_part1(file)))
    # print("Dec 9, part 2: {}".format(calculate_part2(file)))
