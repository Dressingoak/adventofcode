import sys
import os

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> set[tuple[str, int, int]]:
    f = open(file, "r")
    positions = set()
    for i, line in enumerate(f.readlines()):
        for j, char in enumerate(line):
            if char == "A" or char == "B" or char == "C" or char == "D":
                positions.add((char, i, j))
    return positions

def unfold(file: str):
    f = open(file, "r")
    if os.path.exists("input2.txt"):
        os.remove("input2.txt")
    fn = open("input2.txt", "a")
    for i, line in enumerate(f.readlines()):
        fn.write(line)
        if i == 2:
            fn.write("  #D#C#B#A#\n")
            fn.write("  #D#B#A#C#\n")


targets = {"A": 3, "B": 5, "C": 7, "D": 9}
cost = {"A": 1, "B": 10, "C": 100, "D": 1000}
known = {}

solution = {item for sublist in [[(char, i, j) for i in [2, 3]] for char, j in targets.items()] for item in sublist} 

def dist(a: tuple[int, int], b: tuple[int, int]) -> int:
    (a1, a2), (b1, b2) = a, b
    return abs(b1 - a1) + abs(b2 - a2)

def minimize(conf: set[tuple[str, int, int]]):
    conf_key = tuple(sorted(list(conf)))
    if conf_key in known:
        return known[conf_key]
    if conf == solution:
        return 0
    positions = {(i, j): t for t, i, j in conf}
    deepest = max(i for _, i, _ in solution)
    c = []
    for t, i, j in conf:
        moveable = []
        if i > 1 and any((k, j) in positions for k in range(i - 1, 1, -1)):
            continue # immovable
        if i > 1 and targets[t] == j and all((k, j) in positions and positions[(k, j)] == t for k in range(i + 1, deepest + 1)):
            continue # in position
        if i != 1:
            lower = 1
            upper = 11
            for _, l in filter(lambda k: k[0] == 1, positions.keys()):
                if l < j:
                    lower = max(lower, l + 1)
                else:
                    upper = min(upper, l - 1)
            moveable = [(1, l) for l in range(lower, upper + 1) if l not in targets.values()]
        if i == 1:
            dst_x = targets[t]
            in_place = [(k, l) for k, l in positions.keys() if l == dst_x]
            try:
                dst_y = min(k for k, _ in in_place) - 1
            except:
                dst_y = deepest
            if not (dst_y > 1 and all(positions[k] == t for k in in_place)):
                continue
            blocked = False
            for _, l in filter(lambda k: k[0] == 1, positions.keys()):
                if (j < dst_x and l > j and l < dst_x) or (j > dst_x and l < j and l > dst_x):
                    blocked = True
                    break
            if blocked:
                continue
            moveable.append((dst_y, dst_x))
        for pos in moveable:
            new_conf = set(_ for _ in conf if _ != (t, i, j))
            new_conf.add((t, *pos))
            new_cost = minimize(new_conf)
            if new_cost is not None:
                c.append(dist((i, j), pos) * cost[t] + new_cost)
    if len(c) == 0:
        r = None
    else:
        r = min(c)
    known[conf_key] = r
    return r

data = read(file)

print("Dec 23, part 1: {}".format(minimize(data)))

unfold(file)
data = read("input2.txt")
known = dict()
solution = {item for sublist in [[(char, i, j) for i in [2, 3, 4, 5]] for char, j in targets.items()] for item in sublist} 
print("Dec 23, part 2: {}".format(minimize(data)))
