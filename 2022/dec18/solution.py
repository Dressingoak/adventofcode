import sys
sys.path.append('../')
from puzzle import Puzzle
from path_finding import dijkstra

Cube = tuple[int, int, int]

adj: list[Cube] = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

def add_sides(cube: Cube, seen: set[Cube]) -> int:
    sides = 0
    match cube:
        case (x, y, z):
            sides += 6
            for (dx, dy, dz) in adj:
                if (x + dx, y + dy, z + dz) in seen:
                    sides -= 2
            seen.add((x, y, z))
            return sides

def count_sides(file: str, with_interior: bool):
    sides = 0
    ds = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    seen = set()
    with open(file, "r") as f:
        for line in f.readlines():
            match line.strip().split(","):
                case [x, y, z]: sides += add_sides((int(x), int(y), int(z)), seen)
    if not with_interior:
        xmin, xmax, ymin, ymax, zmin, zmax = 0, 0, 0, 0, 0, 0
        for cube in seen:
            match cube:
                case (x, y, z):
                    xmin, xmax = min(xmin, x), max(xmax, x)
                    ymin, ymax = min(ymin, y), max(ymax, y)
                    zmin, zmax = min(zmin, z), max(zmax, z)
        graph = {}
        for x in range(xmin - 1, xmax + 2):
            for y in range(ymin -1, ymax + 2):
                for z in range(zmin -1, zmax + 2):
                    if (x, y, z) in seen:
                        continue
                    adj = {}
                    for (dx, dy, dz) in ds:
                        c = (x + dx, y + dy, z + dz)
                        if c not in seen and c[0] >= xmin - 1 and c[0] <= xmax + 1 and c[1] >= ymin - 1 and c[1] <= ymax + 1 and c[2] >= zmin - 1 and c[2] <= zmax + 1:
                            adj[c] = 1
                    graph[(x, y, z)] = adj
        _, dist = dijkstra(graph, (-1, -1, -1), None)
        interiour = {k for k, v in dist.items() if v is None}
        for cube in interiour:
            sides += add_sides(cube, seen)
    return sides

def calculate_part1(file: str):
    return count_sides(file, True)

def calculate_part2(file: str):
    return count_sides(file, False)

puzzle = Puzzle(__file__)

puzzle.add_part(1, calculate_part1)
puzzle.add_part(2, calculate_part2)

if __name__ == '__main__':
    puzzle.run()
