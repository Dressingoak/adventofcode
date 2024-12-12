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


def set_to_grid(points: set):
    arr = []
    i1, i2 = min(i for i, _ in points), max(i for i, _ in points) + 1
    j1, j2 = min(j for _, j in points), max(j for _, j in points) + 1
    for i in range(i1, i2):
        arr.append([(i, j) in points for j in range(j1, j2)])
    n = len(arr)
    m = len(arr[0])
    rows = []
    for i in range(len(arr) + 1):
        row = []
        for j in range(m + 1):
            row.append(
                (
                    arr[i - 1][j - 1] if (i > 0 and j > 0) else False,
                    arr[i - 1][j] if (i > 0 and j < m) else False,
                    arr[i][j - 1] if (i < n and j > 0) else False,
                    arr[i][j] if (i < n and j < m) else False,
                )
            )
        rows.append(row)
    return rows


def count_sides(points):
    sides = 0
    grid = set_to_grid(points)
    visited = set()
    for k in range(len(grid)):
        for l in range(len(grid[k])):
            match grid[k][l]:
                case (False, False, False, False) | (True, True, True, True):
                    continue
                case _ if (k, l) in visited:
                    continue
                case shape:
                    i, j = (k, l)
                    path = []
                    while len(path) == 0 or (i, j) != path[0]:
                        path.append((i, j))
                        changed = True
                        match shape:
                            # Straight
                            case (False, False, True, True):
                                j += 1
                                changed = False
                            case (True, False, True, False):
                                i += 1
                                changed = False
                            case (True, True, False, False):
                                j -= 1
                                changed = False
                            case (False, True, False, True):
                                i -= 1
                                changed = False

                            # Right turn
                            case (False, False, False, True):
                                j += 1
                            case (False, False, True, False):
                                i += 1
                            case (True, False, False, False):
                                j -= 1
                            case (False, True, False, False):
                                i -= 1

                            # Left turn
                            case (False, True, True, True):
                                i -= 1
                            case (True, True, False, True):
                                j -= 1
                            case (True, True, True, False):
                                i += 1
                            case (True, False, True, True):
                                j += 1

                            # Direction depended
                            case (False, True, True, False):
                                i += j - path[-2][1]
                            case (True, False, False, True):
                                j -= i - path[-2][0]
                        shape = grid[i][j]
                        if changed:
                            sides += 1
                    visited.update(path)
    return sides


def part2(file: str):
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
        t_sides = count_sides(seen)
        price += t_area * t_sides
    return price


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
