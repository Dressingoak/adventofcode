def part1(file: str):
    price = 0
    map = []
    remaining = set()
    with open(file, "r") as f:
        for line in f.readlines():
            map.append([_ for _ in line.strip()])
    rows, cols = len(map), len(map[0])
    remaining = {(i, j) for i in range(rows) for j in range(cols)}
    while len(remaining) > 0:
        i, j = next(iter(remaining))
        stack = [(i, j)]
        seen = set([(i, j)])
        t = map[i][j]
        t_area = 0
        t_perimeter = 0
        while len(stack) > 0:
            i, j = stack.pop()
            remaining.remove((i, j))
            t_area += 1
            for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                k, l = i + di, j + dj
                if (k, l) in seen:
                    continue
                if k >= 0 and k < rows and l >= 0 and l < cols:
                    s = map[k][l]
                    if s == t:
                        stack.append((k, l))
                        seen.add((k, l))
                    else:
                        t_perimeter += 1
                else:
                    t_perimeter += 1
        price += t_area * t_perimeter
    return price


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
