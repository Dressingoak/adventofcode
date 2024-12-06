def part1(file: str):
    map = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row = []
            for j, e in enumerate(line.strip()):
                if e == "^":
                    row.append(".")
                    pos = (i, j)
                    dir = 1  # up
                else:
                    row.append(e)
            map.append(row)
    i, j = pos
    rows, cols = len(map), len(map[0])
    visited = set()
    active = True
    while active:
        try:
            match dir:
                case 0:  # right
                    for j in range(j, cols):
                        if map[i][j + 1] == "#":
                            dir = 3
                            break
                        visited.add((i, j))
                case 1:  # up
                    for i in range(i, -1, -1):
                        if map[i - 1][j] == "#":
                            dir = 0
                            break
                        visited.add((i, j))
                case 2:  # left
                    for j in range(j, -1, -1):
                        if map[i][j - 1] == "#":
                            dir = 1
                            break
                        visited.add((i, j))
                case 3:  # down
                    for i in range(i, rows):
                        if map[i + 1][j] == "#":
                            dir = 2
                            break
                        visited.add((i, j))
        except IndexError:
            visited.add((i, j))
            active = False
    return len(visited)


def part2(file: str):
    map_orig = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row = []
            for j, e in enumerate(line.strip()):
                if e == "^":
                    row.append(".")
                    pos = (i, j)
                    dir_orig = 1  # up
                else:
                    row.append(e)
            map_orig.append(row)
    i, j = pos
    rows, cols = len(map_orig), len(map_orig[0])
    ways = 0
    for k in range(rows):
        for l in range(cols):
            if (k, l) == pos:
                continue
            i, j = pos
            dir = dir_orig
            map = [[_ for _ in map_orig[r]] for r in range(rows)]
            map[k][l] = "#"
            visited = set()
            loop = False
            active = True
            while active and not loop:
                if i == 6 and j == 3:
                    pass
                try:
                    match dir:
                        case 0:  # right
                            for j in range(j, cols):
                                if map[i][j + 1] == "#":
                                    dir = 3
                                    break
                                if (i, j, dir) not in visited:
                                    visited.add((i, j, dir))
                                else:
                                    loop = True
                                    break
                        case 1:  # up
                            for i in range(i, -1, -1):
                                if i == 0:
                                    raise IndexError
                                if map[i - 1][j] == "#":
                                    dir = 0
                                    break
                                if (i, j, dir) not in visited:
                                    visited.add((i, j, dir))
                                else:
                                    loop = True
                                    break
                        case 2:  # left
                            for j in range(j, -1, -1):
                                if j == 0:
                                    raise IndexError
                                if map[i][j - 1] == "#":
                                    dir = 1
                                    break
                                if (i, j, dir) not in visited:
                                    visited.add((i, j, dir))
                                else:
                                    loop = True
                                    break
                        case 3:  # down
                            for i in range(i, rows):
                                if map[i + 1][j] == "#":
                                    dir = 2
                                    break
                                if (i, j, dir) not in visited:
                                    visited.add((i, j, dir))
                                else:
                                    loop = True
                                    break
                except IndexError:
                    visited.add((i, j, dir))
                    active = False
            if loop:
                ways += 1
    return ways


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
