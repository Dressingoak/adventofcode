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


def dijkstra(keys, gen, start, end):
    Q = MinPriorityQueue()
    dist = dict()
    for v in keys():
        Q.insert(v, None)
        dist[v] = None
    dist[start] = 0
    Q.insert(start, 0)
    while len(Q) > 0:
        u, d = Q.pop()
        if u == end:
            return (d, dist)
        for v, x in gen(u):
            try:
                alt = dist[u] + x
            except:
                return (None, dist)
            if dist[v] is None or alt < dist[v]:
                dist[v] = alt
                Q.insert(v, alt)
    return (None, dist)


def part1(file: str, steps=64):
    field = []
    with open(file, "r") as f:
        for i, line in enumerate(f):
            row = []
            for j, c in enumerate(line.strip()):
                row.append(c)
                if c == "S":
                    start = (i, j)
            field.append(row)
    rows, cols = i + 1, j + 1

    def keys():
        i0, j0 = start
        for i, row in enumerate(field):
            for j, c in enumerate(row):
                if c != "#" and abs(i0 - i) + abs(j0 - j) <= steps:
                    yield (i, j)

    def gen(pos):
        for di, dj in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            i, j = pos
            i0, j0 = start
            I, J = i + di, j + dj
            if (
                I >= 0
                and I < rows
                and J >= 0
                and J < cols
                and abs(i0 - I) + abs(j0 - J) <= steps
                and field[I][J] != "#"
            ):
                yield (I, J), 1

    _, d = dijkstra(keys, gen, start, (-1, -1))
    return sum(
        1 for v in d.values() if v is not None and v <= steps and v % 2 == steps % 2
    )


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
