pieces = {
    "|": (1, 3),
    "-": (0, 2),
    "J": (0, 1),
    "L": (1, 2),
    "F": (2, 3),
    "7": (3, 0),
}

directions = {0: (0, -1), 1: (-1, 0), 2: (0, 1), 3: (1, 0)}


def follow_main_loop(file: str):
    grid = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row = []
            for j, c in enumerate(line.strip()):
                row.append(c)
                if c == "S":
                    start = (i, j)
            grid.append(row)
    rows, cols = len(grid), len(grid[0])
    yield rows, cols
    i, j = start
    adjacent = {
        k: v
        for k, v in {
            k: grid[i + di][j + dj]
            for k, (di, dj) in directions.items()
            if i + di >= 0 and i + di < rows and j + dj >= 0 and j + dj < cols
        }.items()
        if v != "." and (k + 2) % 4 in pieces[v]
    }
    sd1, sd2 = tuple(adjacent.keys())
    for piece, (d1, d2) in pieces.items():
        if (sd1 == d1 and sd2 == d2) or (sd1 == d2 and sd2 == d1):
            d = d1
            break
    yield piece, start
    di, dj = directions[d]
    node = (i + di, j + dj)
    prev_dir = (d + 2) % 4
    while node != start:
        k, l = node
        piece = grid[k][l]
        match next(d for d in pieces[piece] if d != prev_dir):
            case d:
                yield piece, node
                (dk, dl) = directions[d]
                node = (k + dk, l + dl)
                prev_dir = (d + 2) % 4


def part1(file: str):
    d = 0
    g = follow_main_loop(file)
    next(g)
    for _ in g:
        d += 1
    return d // 2


def part2(file: str):
    g = follow_main_loop(file)
    rows, cols = next(g)
    grid = {}
    for i in range(rows):
        grid[i] = []
    for piece, (i, j) in g:
        grid[i].append((j, piece))
    count = 0
    for i in range(rows):
        grid[i].sort()
        inside = False
        j_prev = None
        carry = None
        for j, piece in grid[i]:
            if inside and piece != "-" and j_prev is not None and j - j_prev > 0:
                count += j - (j_prev + 1)
            match piece:
                case "F" | "L":
                    carry = piece
                case "|":
                    inside = not inside
                case "J" if carry == "F":
                    inside = not inside
                case "7" if carry == "L":
                    inside = not inside
            j_prev = j
    return count


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
