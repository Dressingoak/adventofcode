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
            case [None, x]:
                return
            case [x, y] if y is None or x < y:
                self.swap(i, j)
                self.sift_up(j)

    def sift_down(self, i):
        children = [
            j
            for j in [2 * i + 1, 2 * i + 2]
            if j < len(self.data) and self.data[j][1] is not None
        ]
        if len(children) > 0:
            j = min(children, key=lambda k: self.data[k][1])
            if self.data[i][1] is None or self.data[j][1] < self.data[i][1]:
                self.swap(i, j)
                self.sift_down(j)

    def insert(self, key, value) -> None:
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
            return None


def parse_field(file: str):
    field = []
    with open(file, "r") as f:
        for i, line in enumerate(f):
            row = []
            for j, c in enumerate(line.strip()):
                row.append(c)
                if c == "S":
                    start = (i, j)
            field.append(row)
    return field, start, i + 1, j + 1


def dijkstra(gen, start):
    Q = MinPriorityQueue()
    dist = dict()
    dist[start] = 0
    Q.insert(start, 0)
    while len(Q) > 0:
        u, _ = Q.pop()
        for v, x in gen(u):
            alt = dist[u] + x
            if v not in dist or alt < dist[v]:
                dist[v] = alt
                Q.insert(v, alt)
    return dist


def part1(file: str):
    path = []
    with open(file) as f:
        for line in f:
            path.append([c for c in line.strip()])
    rows = len(path)
    start = (0, path[0].index("."), 3)
    end = (rows - 1, path[rows - 1].index("."), 3)

    deltas = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    # Directed acyclic graph, use Dijstra with negative weights
    def gen(node):
        i, j, direction = node
        for d in range(-1, 2):
            nd = (direction + d) % 4
            di, dj = deltas[nd]
            I, J = i + di, j + dj
            try:
                match path[I][J]:
                    case ".":
                        yield (I, J, nd), -1
                    case "<" if nd != 2:
                        yield (I, J - 1, nd), -2
                    case "^" if nd != 3:
                        yield (I - 1, J, nd), -2
                    case ">" if nd != 0:
                        yield (I, J + 1, nd), -2
                    case "v" if nd != 1:
                        yield (I + 1, J, nd), -2
            except IndexError:
                pass

    graph = dijkstra(gen, start)
    return -graph[end]


def part2(file: str):
    path = []
    with open(file) as f:
        for line in f:
            path.append([c for c in line.strip()])
    rows = len(path)
    start = (0, path[0].index("."))
    end = (rows - 1, path[rows - 1].index("."))

    deltas = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    nodes = [start, end]
    for i, row in enumerate(path):
        for j, c in enumerate(row):
            if c in ["<", "^", ">", "v"]:
                nodes.append((i, j))

    def gen(node):
        match node:
            case (i, j):
                paths = {}
                for d in range(4):
                    for s, c in gen((i, j, d, 0)):
                        if s not in paths or c > paths[s]:
                            paths[s] = c
                for s, c in paths.items():
                    yield s, c
            case (i, j, direction, acc):
                for d in range(-1, 2):
                    nd = (direction + d) % 4
                    di, dj = deltas[nd]
                    I, J = i + di, j + dj
                    try:
                        match path[I][J]:
                            case "#":
                                pass
                            case _ if (I, J) in nodes:
                                yield (I, J, nd), acc + 1
                            case ".":
                                yield from gen((I, J, nd, acc + 1))
                    except IndexError:
                        pass

    distances = {}
    for node in nodes:
        distances[node] = [((i, j), c) for (i, j, _), c in gen(node)]

    def build(s, dist):
        if s not in dist:
            return None
        maximal = None
        for i in range(len(dist[s])):
            t, c = dist[s][i]
            if t == end:
                return c
            exclude = [s, *[k for k, _ in dist[s]]]
            ndist = {
                k: [(tt, cc) for tt, cc in v if tt not in exclude]
                for k, v in dist.items()
            }
            if (rem := build(t, ndist)) is not None:
                if maximal is None:
                    maximal = c + rem
                else:
                    maximal = max(maximal, c + rem)
        return maximal

    return build(start, distances)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")  # part2('input.txt')=6378
