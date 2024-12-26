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


def iter_points(center: tuple[int, int], radius: int):
    i, j = center
    for k in range(-radius, radius + 1):
        width = radius - abs(k)
        for l in range(-width, width + 1):
            yield (i + k, j + l)


def solve(file: str, dist: int, save: int):
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

    end_to_any = dijkstra(gen, end)
    best = end_to_any[start]

    count = 0
    for (i, j), c1 in end_to_any.items():
        for k, l in iter_points((i, j), dist):
            if (c2 := end_to_any.get((k, l))) is not None:
                s = abs(i - k) + abs(j - l)
                t = best - (c2 + s + (best - c1))
                if t >= save:
                    count += 1
    return count


def part1(file: str):
    return solve(file, 2, 100)


def part2(file: str):
    return solve(file, 20, 100)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
