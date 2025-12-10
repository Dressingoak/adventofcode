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


def part1(file: str):
    total = 0
    light_goals = []
    button_rules = []
    with open(file, "r") as f:
        for line in f.readlines():
            light, *rest = line.strip().split(" ")
            light_goals.append(light[1:-1])
            button_rules.append(
                [[int(_) for _ in b[1:-1].split(",")] for b in rest[:-1]]
            )
    for light, buttons in zip(light_goals, button_rules):

        def gen(l):
            for b in buttons:
                yield "".join(
                    x if i not in b else ("." if x == "#" else "#")
                    for i, x in enumerate(l)
                ), 1

        total += dijkstra(gen, "." * len(light))[light]
    return total


def part2(file: str):
    import numpy as np
    from scipy import optimize
    
    total = 0
    button_rules = []
    joltage_requirements = []
    with open(file, "r") as f:
        for line in f.readlines():
            _, *rest = line.strip().split(" ")
            button_rules.append(
                [[int(_) for _ in b[1:-1].split(",")] for b in rest[:-1]]
            )
            joltage_requirements.append(
                tuple(int(_) for _ in rest[-1][1:-1].split(","))
            )
    for buttons, joltages in zip(button_rules, joltage_requirements):
        A = [[0 for _ in range(len(buttons))] for _ in range(len(joltages))]
        for j, b in enumerate(buttons):
            for i in range(len(joltages)):
                if i in b:
                    A[i][j] = 1
        A = np.array(A, dtype=np.int32)
        c = np.ones(len(buttons), dtype=np.int32)
        b = np.array(joltages, dtype=np.int32)
    
        total += int(optimize.linprog(c=c, A_eq=A, b_eq=b, integrality=1).x.sum().astype(np.int32))

    return total


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
