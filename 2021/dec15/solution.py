import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[list[int]]:
    f = open(file, "r")
    return [[int(_) for _ in line.strip()] for line in f.readlines()]

def to_graph(data: list[list[int]]) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    rows = len(data)
    cols = len(data[0])
    g = dict()
    for i in range(rows):
        for j in range(cols):
            v = [(k, j) for k in range(i-1, i+2) if k in range(rows) and k != i]
            h = [(i, l) for l in range(j-1, j+2) if l in range(cols) and l != j]
            g[(i, j)] = {(k, l): data[k][l] for (k, l) in v + h}
    return g

def dijkstra(g: dict[tuple[int, int], dict[tuple[int, int], int]], s: tuple[int, int], t: tuple[int, int]) -> int:
    Q = set()
    dist = dict()
    for v in g.keys():
        Q.add(v)
        dist[v] = None
    dist[s] = 0
    while len(Q) > 0:
        u = min({k: v for (k, v) in dist.items() if v is not None and k in Q}, key = lambda k: dist[k])
        if u == t:
            return dist[u]
        Q.remove(u)
        for v, x in {k: v for (k, v) in g[u].items() if k in Q}.items():
            alt = dist[u] + x
            if dist[v] is None or alt < dist[v]:
                dist[v] = alt

def compute(data: list[list[int]]):
    graph = to_graph(data)
    source = (0, 0)
    target = (len(data) - 1, len(data[len(data) - 1]) - 1)
    return dijkstra(graph, source, target)

data = read(file)

print("Dec 15, part 1: {}".format(compute(data)))
