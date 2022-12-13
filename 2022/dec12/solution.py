import sys

class MinPriorityQueue:
    def __init__(self) -> None:
        self.keys = dict()
        self.data = []

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

def dijkstra(g: dict[int, dict[int, int]], s: int, t: int) -> int:
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
            try:
                alt = dist[u] + x
            except:
                return None
            if dist[v] is None or alt < dist[v]:
                dist[v] = alt
                Q.insert(v, alt)

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

def calculate_part1(file: str):
    _, graph, _, _, start, end = parse(file)
    return dijkstra(graph, start, end)

def calculate_part2(file: str):
    hmap, graph, rows, cols, _, end = parse(file)
    starting_points = []
    for i in range(rows):
        for j in range(cols):
            if hmap[i][j] == ord("a"):
                starting_points.append((i,j))        
    return min(d for d in [dijkstra(graph, start, end) for start in starting_points] if d is not None)
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 12, part 1: {}".format(calculate_part1(file)))
    print("Dec 12, part 2: {}".format(calculate_part2(file)))
