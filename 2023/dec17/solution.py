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


def move(m, cur: tuple[int, int, int, int]):
    match cur:
        case (i, j, d, s):
            for x in range(-1, 2):
                nd = (d + x) % 4
                if nd == d and s == 2:
                    continue
                ii = i + (nd - 2 if nd % 2 == 1 else 0)
                jj = j + (nd - 1 if nd % 2 == 0 else 0)
                if ii >= 0 and jj >= 0:
                    try:
                        v = m[ii][jj]
                        yield (ii, jj, nd, s + 1 if nd == d else 0), v
                    except IndexError:
                        pass
        case (i, j):
            for d in range(4):
                for (ii, jj, nd, s), v in move(m, (i, j, d, 0)):
                    if s == 1:
                        yield ((ii, jj, nd, 1), v)


def part1(file: str):
    with open(file, "r") as f:
        m = []
        for line in f.readlines():
            m.append([int(v) for v in line.strip()])
    rows, cols = len(m), len(m[0])

    _, cost = a_star(
        lambda x: move(m, x),
        (0, 0),
        lambda x: x[0] == rows - 1 and x[1] == cols - 1,
        lambda x: (rows - 1 - x[0]) + (cols - 1 - x[1]),
    )
    return cost


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
