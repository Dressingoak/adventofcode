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


def solve(file: str, bounds: tuple[int, int], bytes: int):
    imax, jmax = bounds
    blocked = set()
    last_coord = None

    with open(file, "r") as f:
        for idx, line in enumerate(f.readlines()):
            if idx < bytes:
                i, j = line.split(",")
                blocked.add(coord := (int(i), int(j)))
                last_coord = coord
            else:
                break

    def gen(pos):
        i, j = pos
        for di, dj in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            if (
                (k := i + di) >= 0
                and k <= imax
                and (l := j + dj) >= 0
                and l <= jmax
                and (k, l) not in blocked
            ):
                yield ((k, l), 1)

    (end, steps) = a_star(
        gen,
        (0, 0),
        lambda pos: pos[0] == imax and pos[1] == jmax,
        lambda pos: abs(imax - pos[0]) + abs(jmax - pos[1]),
    )
    if end == bounds:
        return steps, last_coord
    else:
        return (None, last_coord)


def part1(file: str, bounds=(70, 70), bytes=1024):
    return solve(file, bounds, bytes)[0]


def part2(file: str, bounds=(70, 70)):
    byte = 0
    while (res := solve(file, bounds, byte))[0] is not None:
        byte += 1
    return ",".join([str(_) for _ in res[1]])


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
