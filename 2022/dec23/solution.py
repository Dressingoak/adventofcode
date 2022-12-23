import sys

def calculate_part1(file: str):
    elves: set[tuple[int, int]] = set()
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line):
                if c != "#":
                    continue
                else:
                    elves.add((j, -i))
    dirs = [
        [(-1,  1), ( 0,  1), ( 1,  1)], # N
        [( 1, -1), ( 0, -1), (-1, -1)], # S
        [(-1,  1), (-1,  0), (-1, -1)], # W
        [( 1,  1), ( 1,  0), ( 1, -1)]  # E
    ]
    for round in range(10):
        proposals = {}
        for x, y in elves:
            if len(elves.intersection([(a, b) for a in range(x-1,x+2) for b in range(y-1,y+2)])) == 1:
                proposals[(x, y)] = set([(x, y)])
                continue
            moves = False
            for d in range(round, round+4):
                fov = [(x + a, y + b) for a, b in dirs[d % 4]]
                if len(elves.intersection(fov)) == 0:
                    moves = True
                    if fov[1] not in proposals:
                        proposals[fov[1]] = set()
                    proposals[fov[1]].add((x, y))
                    break
            if moves:
                continue
            proposals[(x, y)] = set([(x, y)])
        next = set()
        for k, v in proposals.items():
            if len(v) == 1:
                next.add(k)
            else:
                next.update(v)
        elves = next
    x, y = elves.pop()
    xmin, xmax, ymin, ymax = x, x, y, y
    for (x, y) in elves:
        xmin, xmax = min(xmin, x), max(xmax, x)
        ymin, ymax = min(ymin, y), max(ymax, y)
    return (xmax - xmin + 1) * (ymax - ymin + 1) - len(elves) - 1

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 23, part 1: {}".format(calculate_part1(file)))
    # print("Dec 23, part 2: {}".format(calculate_part2(file)))
