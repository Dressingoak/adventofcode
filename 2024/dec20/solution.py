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


def solve(file: str, dist: int):
    map = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row = []
            for j, v in enumerate(line.strip()):
                match v:
                    case ".":
                        row.append(True)
                    case "#":
                        row.append(False)
                    case "S":
                        start = (i, j)
                        row.append(True)
                    case "E":
                        end = (i, j)
                        row.append(True)
            map.append(row)
    rows, cols = i + 1, j + 1

    def gen(pos):
        i, j = pos
        for di, dj in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            if (
                (k := i + di) >= 0
                and (l := j + dj) >= 0
                and k < rows
                and l < cols
                and map[k][l]
            ):
                yield ((k, l), 1)

    start_to_any = dijkstra(gen, start)
    end_to_any = dijkstra(gen, end)
    best = start_to_any[end]

    steps = {}

    for (i, j), c1 in start_to_any.items():
        for (k, l), c2 in end_to_any.items():
            if (s := abs(i - k) + abs(j - l)) <= dist:
                if (t := best - (c1 + s + c2)) not in steps:
                    steps[t] = 1
                else:
                    steps[t] += 1
    for a, b in sorted((a, b) for a, b in steps.items()):
        print(f"There are {b} cheats that save {a} picoseconds.")
    return steps


def part1(file: str):
    steps = solve(file, 2)
    return sum(b for a, b in steps.items() if a >= 100)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
