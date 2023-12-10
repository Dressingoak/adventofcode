pieces = {
    "|": (1, 3),
    "-": (0, 2),
    "J": (0, 1),
    "L": (1, 2),
    "F": (2, 3),
    "7": (3, 0),
}

directions = {0: (0, -1), 1: (-1, 0), 2: (0, 1), 3: (1, 0)}


def part1(file: str):
    grid = []
    dist = 0
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row = []
            for j, c in enumerate(line.strip()):
                row.append(c)
                if c == "S":
                    start = (i, j)
            grid.append(row)
    rows, cols = len(grid), len(grid[0])
    (i, j) = start
    adjacent = {
        k: v
        for k, v in {
            k: grid[i + di][j + dj]
            for k, (di, dj) in directions.items()
            if i + di >= 0 and i + di < rows and j + dj >= 0 and j + dj < cols
        }.items()
        if v != "." and (k + 2) % 4 in pieces[v]
    }
    if len(adjacent) == 2:
        match next(_ for _ in adjacent.keys()):
            case d:
                (di, dj) = directions[d]
                node = (i + di, j + dj)
                prev_dir = (d + 2) % 4
                dist += 1
        while node != start:
            k, l = node
            piece = grid[k][l]
            match next(d for d in pieces[piece] if d != prev_dir):
                case d:
                    (dk, dl) = directions[d]
                    node = (k + dk, l + dl)
                    prev_dir = (d + 2) % 4
                    dist += 1
    else:
        raise Exception("More pieces connect to S")
    return dist // 2


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
