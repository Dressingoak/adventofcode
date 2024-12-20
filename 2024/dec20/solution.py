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


def part1(file: str):
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

    steps = {}

    _, best = a_star(
        gen,
        start,
        lambda pos: pos == end,
        lambda pos: abs(pos[0] - end[0]) + abs(pos[1] - end[1]),
    )

    for i in range(rows):
        for j in range(cols):
            if not map[i][j]:
                continue
            for di, dj in [(0, 1), (1, 0)]:
                if (
                    (k := i + 2 * di) >= 0
                    and (l := j + 2 * dj) >= 0
                    and k < rows
                    and l < cols
                    and not map[i + di][j + dj]
                    and map[k][l]
                ):
                    k, l = i + di, j + dj
                    map[k][l] = True
                    _, s = a_star(
                        gen,
                        start,
                        lambda pos: pos == end,
                        lambda pos: abs(pos[0] - end[0]) + abs(pos[1] - end[1]),
                    )
                    if (t := best - s) not in steps:
                        steps[t] = 1
                    else:
                        steps[t] += 1
                    map[k][l] = False
    #         progress = (i * cols + (j + 1)) / (rows * cols) * 100
    #         print(f"{progress:.2f} % ({i=}, {j=})")
    # for a, b in sorted((a, b) for a, b in steps.items()):
    #     print(f"There are {b} cheats that save {a} picoseconds.")

    return sum(b for a, b in steps.items() if a >= 100)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
