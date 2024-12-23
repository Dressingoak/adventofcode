def combinations(arr, k):
    n = len(arr)
    for i in range(n):
        for j in range(i + k - 1, n):
            temp = arr[i : i + k - 1]
            temp.append(arr[j])
            yield temp


def part1(file: str):
    sum = 0
    connections = {}
    with open(file, "r") as f:
        for line in f.readlines():
            l, r = line.strip().split("-")
            for x, y in [(l, r), (r, l)]:
                if x not in connections:
                    connections[x] = [y]
                else:
                    connections[x].append(y)

    triplets = {}
    for c, t in connections.items():
        for s in combinations(t, 2):
            k = tuple(sorted([c, *s]))
            if k not in triplets:
                triplets[k] = 1
            else:
                triplets[k] += 1
    for k, c in triplets.items():
        if c == 3:
            if any(_.startswith("t") for _ in k):
                sum += 1
    return sum


def part2(file: str):
    connections = {}
    with open(file, "r") as f:
        for line in f.readlines():
            l, r = line.strip().split("-")
            for x, y in [(l, r), (r, l)]:
                if x not in connections:
                    connections[x] = [y]
                else:
                    connections[x].append(y)

    def connected(c1, c2):
        return c2 in connections[c1]

    smallest = 1
    all_combs = []
    for k, c in connections.items():
        arr = [k, *c]
        combs = []
        for n in range(smallest, len(arr)):
            for comb in combinations(arr, n):
                m = len(comb)
                cc = 0
                for i in range(m):
                    for j in range(i):
                        cc += connected(comb[i], comb[j])
                if cc == (m - 1) * m // 2:
                    combs.append(comb)
        if len(combs) > 0:
            s = max(combs, key=lambda x: len(x))
            smallest = len(s)
            all_combs.append(s)
    largest = max(all_combs, key=lambda x: len(x))
    return ",".join(sorted(largest))


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
