import sys
sys.path.append('../')
from puzzle import Puzzle
from path_finding import dijkstra

def evaluate(current: int, adjecent: int, reversed: bool):
    if not reversed:
        return adjecent - current <= 1
    else:
        return adjecent - current >= -1

def parse(file: str, is_reversed: bool = False):
    with open(file, "r") as f:
        hmap = []
        for i, line in enumerate(f.readlines()):
            row = []
            for j, c in enumerate(line.strip()):
                if c == "S":
                    row.append(ord("a"))
                    start = (i, j)
                elif c == "E":
                    row.append(ord("z"))
                    end = (i, j)
                else:
                    row.append(ord(c))
            hmap.append(row)
    rows = len(hmap)
    cols = len(hmap[0])

    graph = dict()
    for i in range(rows):
        for j in range(cols):
            adj = {}
            cur = hmap[i][j]
            if i > 0 and evaluate(cur, hmap[i-1][j], is_reversed):
                adj[(i-1, j)] = 1
            if j > 0 and evaluate(cur, hmap[i][j-1], is_reversed):
                adj[(i, j-1)] = 1
            if i < rows - 1 and evaluate(cur, hmap[i+1][j], is_reversed):
                adj[(i+1, j)] = 1
            if j < cols - 1 and evaluate(cur, hmap[i][j+1], is_reversed):
                adj[(i, j+1)] = 1
            graph[(i, j)] = adj

    return hmap, graph, start, end

def calculate_part1(file: str):
    _, graph, start, end = parse(file)
    shortest, _ = dijkstra(graph, start, end)
    return shortest

def calculate_part2(file: str):
    hmap, graph, _, end = parse(file, is_reversed=True)
    _, dists = dijkstra(graph, end, None)
    return min(steps for (i, j), steps in dists.items() if hmap[i][j] == ord("a") and steps is not None)
    
puzzle = Puzzle(__file__)

puzzle.add_part(1, calculate_part1)
puzzle.add_part(2, calculate_part2)

if __name__ == '__main__':
    puzzle.run()
