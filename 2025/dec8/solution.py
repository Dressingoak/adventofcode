def part1(file: str, connections: int = 1000):
    junction_boxes: list[tuple[int, int, int]] = []
    junction_box_distances: list[tuple[int, tuple[int, int]]] = []
    circuts: list[int, set[int]] = []
    with open(file, "r") as f:
        for line in f.readlines():
            x, y, z = line.strip().split(",")
            junction_boxes.append((int(x), int(y), int(z)))
    n = len(junction_boxes)

    for i in range(n):
        x1, y1, z1 = junction_boxes[i]
        for j in range(i + 1, n):
            x2, y2, z2 = junction_boxes[j]
            d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            junction_box_distances.append((d2, (i, j)))
    junction_box_distances.sort()

    for d2, (i, j) in junction_box_distances[:connections]:
        connected = False
        for l in range(len(circuts)):
            if i in circuts[l] or j in circuts[l]:
                circuts[l].add(i)
                circuts[l].add(j)
                connected = True
        if not connected:
            circuts.append(set([i, j]))
        for k in range(m := len(circuts)):
            for l in range(k + 1, m):
                if len(circuts[k].intersection(circuts[l])) > 0:
                    circuts[k].update(circuts[l])
                    circuts[l] = set()
    sizes = sorted((len(circut) for circut in circuts if len(circut) > 0), reverse=True)
    m = sum(sizes)
    sizes = sizes + [
        1,
    ] * (n - m)
    return sizes[0] * sizes[1] * sizes[2]


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
