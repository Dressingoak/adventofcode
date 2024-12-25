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


directional_positions = {
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "^": (0, 1),
    "A": (0, 2),
}
"""Layout:
```
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
```
"""

directional_positions_rev = {v: k for k, v in directional_positions.items()}

numeric_positions = {
    "A": (3, 2),
    "0": (3, 1),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}
"""Layout:
```
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
```
"""

numeric_positions_rev = {v: k for k, v in numeric_positions.items()}


def steps(start: str, end: str, top: bool, level: int, known: dict, known_paths: dict):
    if level == 0:
        return 1
    if (mem := (start, end, level)) in known:
        return known[mem]

    if (mem2 := (level, path_start := (start, "A"))) not in known_paths:
        table = directional_positions if not top else numeric_positions
        table_rev = directional_positions_rev if not top else numeric_positions_rev

        def gen(pos):
            cur, inner = pos
            i, j = table[cur]
            for di, dj, dir in [(0, 1, ">"), (-1, 0, "^"), (0, -1, "<"), (1, 0, "v")]:
                if (k := i + di, l := j + dj) in table_rev:
                    nxt = table_rev[(k, l)]
                    cost = steps(inner, dir, False, level - 1, known, known_paths)
                    yield (nxt, dir), cost

        all_cost = dijkstra(gen, path_start)
        known_paths[mem2] = all_cost
    else:
        all_cost = known_paths[mem2]
    res = min(
        c + steps(k[1], "A", False, level - 1, known, known_paths)
        for k, c in all_cost.items()
        if k[0] == end
    )
    known[mem] = res
    return res


def solve(file: str, robots: int):
    complexity = 0
    known = {}
    known_paths = {}
    with open(file, "r") as f:
        for line in f.readlines():
            code = line.strip()
            number = int(code[:-1])
            length = 0
            for i in range(len(code)):
                length += steps(
                    code[i - 1],
                    code[i],
                    True,
                    robots + 1,
                    known,
                    known_paths,
                )
            # print(f"{line.strip()}: {length}")
            complexity += length * number
    return complexity


def part1(file: str):
    return solve(file, 2)


def part2(file: str):
    return solve(file, 25)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
