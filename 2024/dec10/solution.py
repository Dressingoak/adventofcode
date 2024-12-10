def part1(file: str):
    map = []
    starts = []
    with open(file, "r") as f:
        for rows, line in enumerate(f.readlines()):
            row = []
            for cols, h in enumerate(line.strip()):
                row.append(int(h) if h != "." else -1)
                if h != "." and int(h) == 0:
                    starts.append(((rows, cols), (rows, cols)))
            map.append(row)
    rows += 1
    cols += 1
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    nines = set()
    while len(starts) > 0:
        new_starts = []
        for s, (i, j) in starts:
            for di, dj in dirs:
                k, l = i + di, j + dj
                if (
                    k >= 0
                    and k < rows
                    and l >= 0
                    and l < cols
                    and map[k][l] == map[i][j] + 1
                ):
                    if map[k][l] == 9:
                        nines.add((s, (k, l)))
                    else:
                        new_starts.append((s, (k, l)))
        starts = new_starts
    return len(nines)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
