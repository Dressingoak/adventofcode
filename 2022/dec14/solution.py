import sys
sys.path.append('../')
from puzzle import Puzzle

def parse_cave(file: str):
    cave = {}
    with open(file, "r") as f:
        for line in f.readlines():
            prev = None
            for coords in line.strip().split(" -> "):
                match coords.split(","):
                    case [x1, y1]:
                        x1, y1 = int(x1), int(y1)
                        match prev:
                            case (x, y0) if x == x1:
                                for y in range(min(y0, y1), max(y0, y1)+1):
                                    if x in cave:
                                        cave[x][y] = "#"
                                    else:
                                        cave[x] = {y: "#"}
                            case (x0, y) if y == y1:
                                for x in range(min(x0, x1), max(x0, x1)+1):
                                    if x in cave:
                                        cave[x][y] = "#"
                                    else:
                                        cave[x] = {y: "#"}
                        prev = (x1, y1)
    return cave

def add_floor(cave: dict[int, dict[int, str]]):
    b = max(y for ys in cave.values() for y in ys.keys()) + 2
    for x in range(500 - b, 500 + b + 1):
        if x in cave:
            cave[x][b] = "#"
        else:
            cave[x] = {b: "#"}

def show_cave(cave: dict[int, dict[int, str]]):
    x0, x1 = min(cave.keys()), max(cave.keys())
    y0 = min(y for ys in cave.values() for y in ys.keys())
    y1 = max(y for ys in cave.values() for y in ys.keys())
    s = ""
    for y in range(y0 - 1, y1 + 2):
        for x in range(x0 - 1, x1 + 2):
            if x in cave and y in cave[x]:
                s += cave[x][y]
            else:
                s += "."
        s += "\n"
    return s.strip()

def simulate(cave: dict[int, dict[int, str]], cur: tuple[int, int] | None = None):
    match cur:
        case None: # Source sand from starting position
            return simulate(cave, (500, 0))
        case (x, y) if x in cave and y in cave[x]: # No space for sand
            return None
        case (x, y): # Position is free, simulate
            if x not in cave: # Stuff is falling to the abyss
                return None
            highest = min(j for j in cave[x].keys() if j > y) # Highest rock/sand below current y-pos
            if highest - y > 1:
                return simulate(cave, (x, highest - 1))
            if highest - y == 1:
                if x - 1 in cave:
                    if not highest in cave[x-1]: # Fall diagonally to the left
                        return simulate(cave, (x-1, highest))
                else: # Stuff is falling to the abyss
                    return None
                if x + 1 in cave:
                    if not highest in cave[x+1]: # Fall diagonally to the right
                        return simulate(cave, (x+1, highest))
                else: # Stuff is falling to the abyss
                    return None
                return (x, highest - 1) # Sand is at rest here

def simulate_many(cave):
    c = 0
    while True:
        match simulate(cave):
            case (x, y):
                c += 1
                cave[x][y] = "o"
            case None: break
    return c

def calculate_part1(file: str, show=False):
    cave = parse_cave(file)
    c = simulate_many(cave)
    if show:
        print(show_cave(cave))
    return c

def calculate_part2(file: str, show=False):
    cave = parse_cave(file)
    add_floor(cave)
    c = simulate_many(cave)
    if show:
        print(show_cave(cave))
    return c
    
if __name__ == '__main__':

    puzzle = Puzzle(__file__)

    puzzle.add_part(1, calculate_part1)
    puzzle.add_part(2, calculate_part2)
    puzzle.set_parameter_type_bool("show")
    puzzle.set_parameter_help("show", "display the sand dunes")

    puzzle.run()
