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


def part1(file: str, steps=64):
    field, start, rows, cols = parse_field(file)

    parity = (sum(start) + steps % 2) % 2

    def gen_available(pos):
        for di, dj in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            i, j = pos
            I, J = i + di, j + dj
            if (
                I >= 0
                and I < rows
                and J >= 0
                and J < cols
                and abs(start[0] - I) + abs(start[1] - J) <= steps
                and field[I][J] != "#"
            ):
                yield (I, J)

    def gen(pos):
        if sum(pos) % 2 == parity:
            targets = set()
            for u in gen_available(pos):
                targets.update(gen_available(u))
            for t in targets:
                yield t, 2
        else:
            for u in gen_available(pos):
                yield u, 1

    return sum(1 for v in dijkstra(gen, start).values() if v <= steps)


def find_cost(field, start, parity, max_dist):
    rows, cols = len(field), len(field[0])

    def gen_available(pos):
        for di, dj in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            i, j = pos
            I, J = i + di, j + dj
            if (
                abs(start[0] - I) + abs(start[1] - J) <= max_dist
                and field[I % rows][J % cols] != "#"
            ):
                yield (I, J)

    def gen(pos):
        if sum(pos) % 2 == parity:
            targets = set()
            for u in gen_available(pos):
                targets.update(gen_available(u))
            for t in targets:
                yield t, 2
        else:
            for u in gen_available(pos):
                yield u, 1

    d = dijkstra(gen, start)
    return d


def part2_naive(file: str, steps=26501365):
    field, start, _, _ = parse_field(file)

    parity = (sum(start) + steps % 2) % 2

    d = {k: v for k, v in find_cost(field, start, parity, steps).items() if v <= steps}
    return len(d)


def part2(file: str):
    steps = 26501365
    # Total steps = 26501365 = 2023 * 100 * 131 + 65
    field, start, size, _ = parse_field(file)  # Assume rows == cols
    mid = size // 2  # Assume S is at (rows // 2, rows // 2)

    parity = (sum(start) + steps % 2) % 2
    y = []
    for s in range(mid, mid + 2 * size + 1, size):  # Steps 65, 65 + 131, 65 + 131 * 2
        print(f"{s}: ", end="")
        y.append(
            count := sum(
                1 for v in find_cost(field, start, parity, s).values() if v <= s
            )
        )
        print(count)
    # y.extend([3742, 33564, 93148])

    # Due to the vertical, horizontal and diagonal free paths, reaching any point on the free path on the diagonal
    # takes <= steps required by going through the fields. Also, the asked number of steps pefectly fit inside free
    # paths. The first observation means that the number of reachable spots grow quadratically. Thus, interpolate a
    # 2nd order polynomial P from (0, y[0]), (1, y[1]) and (2, y[2]) and find P(2023 * 100)
    # P(x) = a * x**2 + b * x + c
    c = y[0]  # From P(0) = c
    a = (c + y[2]) // 2 - y[1]  # From P(1) = a + b + c, P(2) = 4 * a + 2 * b + c
    b = y[1] - a - c
    x = (steps - mid) // size
    return a * x**2 + b * x + c


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
