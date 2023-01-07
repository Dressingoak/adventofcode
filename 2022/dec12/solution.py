import sys
sys.path.append('../')
from timing import print_timing
from path_finding import dijkstra

def parse(file: str):
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
            if i > 0 and hmap[i-1][j] - cur <= 1:
                adj[(i-1, j)] = 1
            if j > 0 and hmap[i][j-1] - cur <= 1:
                adj[(i, j-1)] = 1
            if i < rows - 1 and hmap[i+1][j] - cur <= 1:
                adj[(i+1, j)] = 1
            if j < cols - 1 and hmap[i][j+1] - cur <= 1:
                adj[(i, j+1)] = 1
            graph[(i, j)] = adj

    return hmap, graph, rows, cols, start, end

@print_timing
def calculate_part1(file: str):
    _, graph, _, _, start, end = parse(file)
    shortest, _ = dijkstra(graph, start, end)
    return shortest

@print_timing
def calculate_part2(file: str):
    hmap, graph, rows, cols, _, end = parse(file)
    starting_points = []
    for i in range(rows):
        for j in range(cols):
            if hmap[i][j] == ord("a"):
                starting_points.append((i,j))        
    return min(d for d, _ in [dijkstra(graph, start, end) for start in starting_points] if d is not None)
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 12, part 1: {} (took {})".format(*calculate_part1(file)))
    print("Dec 12, part 2: {} (took {})".format(*calculate_part2(file)))
