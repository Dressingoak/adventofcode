import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[list[int]]:
    f = open(file, "r")
    return [[int(_) for _ in line.strip()] for line in f.readlines()]

def repeat(data: list[list[int]], n: int) -> list[list[int]]:
    rows = len(data)
    cols = len(data[0])
    new_data = []
    for k in range(n * rows):
        i = k % rows
        ai = k // rows
        row = []
        for l in range(n * cols):
            j = l % cols
            aj = l // cols
            row.append((data[i][j] + ai + aj - 1) % 9 + 1)
        new_data.append(row)
    return new_data

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

class MinPriorityQueue:
    def __init__(self) -> None:
        self.keys = dict()
        self.data = []

    def __repr__(self) -> str:
        return "MinPriorityQueue<{}, {}>".format(self.keys, self.data)

    def __len__(self):
        return len(self.data)

    def swap(self, i, j):
        self.keys[self.data[i][0]], self.keys[self.data[j][0]] = j, i
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def sift_up(self, i):
        if i == 0:
            return
        j = (i - 1) // 2
        match [self.data[i][1], self.data[j][1]]:
            case [None, x]: return
            case [x, y] if y is None or x < y:
                self.swap(i, j)
                self.sift_up(j)

    def sift_down(self, i):
        children = [j for j in [2 * i + 1, 2 * i + 2] if j < len(self.data) and self.data[j][1] is not None]
        if len(children) > 0:
            j = min(children, key = lambda k: self.data[k][1])
            if self.data[i][1] is None or self.data[j][1] < self.data[i][1]:
                self.swap(i, j)
                self.sift_down(j)
    
    def insert(self, key, value):
        if key in self.keys:
            i = self.keys[key]
            self.data[i] = (key, value)
        else:
            i = len(self.data)
            self.data.append((key, value))
            self.keys[key] = i
        self.sift_up(i)

    def pop(self):
        if len(self.data) > 0:
            self.swap(0, len(self.data) - 1)
            key, value = self.data.pop()
            self.sift_down(0)
            del self.keys[key]
            return (key, value)
        else:
            return

def dijkstra(g: dict[tuple[int, int], dict[tuple[int, int], int]], s: tuple[int, int], t: tuple[int, int]) -> int:
    Q = MinPriorityQueue()
    dist = dict()
    for v in g.keys():
        Q.insert(v, None)
        dist[v] = None
    dist[s] = 0
    Q.insert(s, 0)
    while len(Q) > 0:
        u, d = Q.pop()
        if u == t:
            return d
        for v, x in g[u].items():
            alt = dist[u] + x
            if dist[v] is None or alt < dist[v]:
                dist[v] = alt
                Q.insert(v, alt)


def compute(data: list[list[int]]):
    graph = to_graph(data)
    source = (0, 0)
    target = (len(data) - 1, len(data[len(data) - 1]) - 1)
    return dijkstra(graph, source, target)

data = read(file)
tiled_data = repeat(data, 5)

print("Dec 15, part 1: {}".format(compute(data)))
print("Dec 15, part 2: {}".format(compute(tiled_data)))
