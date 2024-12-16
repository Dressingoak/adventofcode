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


def a_star(gen, start, end_eval, heuristic):
    open_set = MinPriorityQueue()
    open_set.insert(start, 0)
    cost_until = {start: 0}
    while len(open_set) > 0:
        current, _ = open_set.pop()
        if end_eval(current):
            break
        for neighbor, cost in gen(current):
            neighbor_cost = cost_until[current] + cost
            if neighbor not in cost_until or neighbor_cost < cost_until[neighbor]:
                cost_until[neighbor] = neighbor_cost
                open_set.insert(neighbor, neighbor_cost + heuristic(neighbor))
    return current, cost_until[current]


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
    map = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row = []
            for j, v in enumerate(line.strip()):
                if v == "#":
                    row.append(False)
                else:
                    row.append(True)
                if v == "S":
                    start = (i, j, 0)
                if v == "E":
                    end = (i, j)
            map.append(row)

    def gen(pos):
        i, j, d = pos
        match d:
            case 0:
                di, dj = 0, 1
            case 1:
                di, dj = -1, 0
            case 2:
                di, dj = 0, -1
            case 3:
                di, dj = 1, 0
        if map[(k := i + di)][(l := j + dj)]:
            yield (k, l, d), 1
        yield (i, j, (d - 1) % 4), 1000
        yield (i, j, (d + 1) % 4), 1000

    _, cost = a_star(
        gen,
        start,
        lambda pos: (pos[0], pos[1]) == end,
        lambda pos: abs(end[0] - pos[0]) + abs(end[1] - pos[1]),
    )

    return cost


def part2(file: str):
    map = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row = []
            for j, v in enumerate(line.strip()):
                if v == "#":
                    row.append(False)
                else:
                    row.append(True)
                if v == "S":
                    start = (i, j, 0)
                if v == "E":
                    end = (i, j)
            map.append(row)

    def gen(pos):
        i, j, d = pos
        match d:
            case 0:
                di, dj = 0, 1
            case 1:
                di, dj = -1, 0
            case 2:
                di, dj = 0, -1
            case 3:
                di, dj = 1, 0
        if map[(k := i + di)][(l := j + dj)]:
            yield (k, l, d), 1
        yield (i, j, (d - 1) % 4), 1000
        yield (i, j, (d + 1) % 4), 1000

    costs = dijkstra(gen, start)
    min_cost = min(costs[(*end, d)] for d in range(4))
    ends = [(*end, (d + 2) % 4) for d in range(4) if costs[(*end, d)] == min_cost]
    for e in ends:
        ret_costs = dijkstra(gen, e)
        summed = {
            pos: cost + ret_costs[(pos[0], pos[1], (pos[2] + 2) % 4)]
            for pos, cost in costs.items()
        }
        stack = [start]
        seen = set()
        while len(stack) > 0:
            pos = stack.pop()
            seen.add(pos)
            adjs = {}
            for adj, _ in gen(pos):
                if (c := summed[adj]) not in adjs:
                    adjs[c] = [adj]
                else:
                    adjs[c].append(adj)
            least = min(_ for _ in adjs.keys())
            stack.extend(k for k in adjs[least] if k not in seen)

    return len(set((i, j) for (i, j, _) in seen))


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
