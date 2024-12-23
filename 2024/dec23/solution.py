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
        if c >= 2:
            if any(_.startswith("t") for _ in k):
                sum += 1
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
