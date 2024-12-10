def part1(file: str):
    map = []
    starts = []
    with open(file, "r") as f:
        for rows, line in enumerate(f.readlines()):
            row = []
            for cols, h in enumerate(line.strip()):
                row.append(int(h))
                if int(h) == 0:
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


def part2(file: str):
    sum_of_ratings = 0
    map = []
    starts = []
    with open(file, "r") as f:
        for rows, line in enumerate(f.readlines()):
            row = []
            for cols, h in enumerate(line.strip()):
                row.append(int(h))
                if int(h) == 0:
                    starts.append((rows, cols))
            map.append(row)
    rows += 1
    cols += 1
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while len(starts) > 0:
        new_starts = []
        for i, j in starts:
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
                        sum_of_ratings += 1
                    else:
                        new_starts.append((k, l))
        starts = new_starts
    return sum_of_ratings


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
