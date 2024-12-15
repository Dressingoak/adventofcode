def plot(map, pos):
    for i, row in enumerate(map):
        for j, v in enumerate(row):
            if (i, j) == pos:
                print("@", end="")
            else:
                print(v, end="")
        print("")


def part1(file: str):
    map = []
    movements = []
    parse_map = True
    i = 0
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                parse_map = False
                continue
            if parse_map:
                row = []
                for j, v in enumerate(line):
                    match v:
                        case "#" | "O" | ".":
                            row.append(v)
                        case "@":
                            pos = (i, j)
                            row.append(".")
                map.append(row)
                i += 1
            else:
                movements += [_ for _ in line]
    i, j = pos

    # print("Initial state:")
    # plot(map, (i, j))
    # print()

    for movement in movements:
        # print(f"Move {movement}:")
        match movement:
            case "^":
                di, dj = -1, 0
            case "v":
                di, dj = 1, 0
            case ">":
                di, dj = 0, 1
            case "<":
                di, dj = 0, -1
        match map[i + di][j + dj]:
            case ".":
                i += di
                j += dj
            case "#":
                pass
            case "O":
                k = i + di
                l = j + dj
                while True:
                    match map[k][l]:
                        case ".":
                            map[k][l], map[i + di][j + dj] = (
                                map[i + di][j + dj],
                                map[k][l],
                            )
                            i += di
                            j += dj
                            break
                        case "#":
                            break
                        case "O":
                            k += di
                            l += dj
        # plot(map, (i, j))
        # print()
    gps = 0
    for i, row in enumerate(map):
        for j, v in enumerate(row):
            if v == "O":
                gps += 100 * i + j
    return gps


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
