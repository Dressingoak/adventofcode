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


def affected_boxes(map, pos, delta):
    i, j = pos
    di, dj = delta
    k, l = i + di, j + dj
    if di != 0:
        match map[k][l]:
            case "[":
                yield (k, l)
                yield from affected_boxes(map, (k, l), delta)
                yield from affected_boxes(map, (k, l + 1), delta)
            case "]":
                yield (k, l - 1)
                yield from affected_boxes(map, (k, l - 1), delta)
                yield from affected_boxes(map, (k, l), delta)
    else:
        match map[k][l]:
            case "[":
                yield (k, l)
                yield from affected_boxes(map, (k, l + 1), delta)
            case "]":
                yield (k, l - 1)
                yield from affected_boxes(map, (k, l - 1), delta)


def get_affected_boxes(map, pos, delta):
    unique_boxes = set(affected_boxes(map, pos, delta))
    match delta:
        case (-1, 0) | (0, -1):
            return sorted(unique_boxes)
        case (1, 0):
            return sorted(unique_boxes, key=lambda b: (-b[0], b[1]))
        case (0, 1):
            return sorted(unique_boxes, key=lambda b: (b[0], -b[1]))


def part2(file: str):
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
                        case "#" | ".":
                            row += [v, v]
                        case "O":
                            row += ["[", "]"]
                        case "@":
                            pos = (i, j * 2)
                            row += [".", "."]
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
        if map[i + di][j + dj] != "#":
            moveable = True
            boxes = get_affected_boxes(map, (i, j), (di, dj))
            for k, l in boxes:
                if map[k + di][l + dj] == "#" or map[k + di][l + dj + 1] == "#":
                    moveable = False
                    break
            if moveable:
                for k, l in boxes:
                    for n in range(1, -1, -1) if dj > 0 else range(2):
                        map[k][l + n], map[k + di][l + dj + n] = (
                            map[k + di][l + dj + n],
                            map[k][l + n],
                        )
                i += di
                j += dj
        # plot(map, (i, j))
        # print()
    gps = 0
    for i, row in enumerate(map):
        for j, v in enumerate(row):
            if v == "[":
                gps += 100 * i + j
    return gps


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
