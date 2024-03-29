def parse(file: str):
    mirrors = {}
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.strip()):
                if c == ".":
                    continue
                if i not in mirrors:
                    mirrors[i] = {j: c}
                else:
                    mirrors[i][j] = c
    return mirrors, i + 1, j + 1


def count_energized(start, mirrors, rows, cols):
    visited = set()
    beams = [start]
    while len(beams) > 0:
        match beams[-1]:
            case (i, j, 0) if j > 0:
                nxt = (i, j - 1, 0)
            case (i, j, 1) if i > 0:
                nxt = (i - 1, j, 1)
            case (i, j, 2) if j < cols - 1:
                nxt = (i, j + 1, 2)
            case (i, j, 3) if i < rows - 1:
                nxt = (i + 1, j, 3)
            case _:
                beams.pop()
                continue

        mirror = (
            mirrors[nxt[0]][nxt[1]]
            if nxt[0] in mirrors and nxt[1] in mirrors[nxt[0]]
            else None
        )
        beams.pop()
        match nxt, mirror:
            case (i, j, d), "/":
                if (b := (i, j, 3 - d)) not in visited:
                    visited.add(b)
                    beams.append(b)

            case (i, j, d), "\\":
                if (b := (i, j, d + 1 if d % 2 == 0 else d - 1)) not in visited:
                    visited.add(b)
                    beams.append(b)

            case (i, j, 0 | 2), "|":
                if (b := (i, j, 1)) not in visited:
                    visited.add(b)
                    beams.append(b)
                if (b := (i, j, 3)) not in visited:
                    visited.add(b)
                    beams.append(b)

            case (i, j, 1 | 3), "-":
                if (b := (i, j, 0)) not in visited:
                    visited.add(b)
                    beams.append(b)
                if (b := (i, j, 2)) not in visited:
                    visited.add(b)
                    beams.append(b)

            case _:
                if nxt not in visited:
                    visited.add(nxt)
                    beams.append(nxt)

    return len(set((i, j) for i, j, _ in visited))


def part1(file: str):
    mirrors, rows, cols = parse(file)
    return count_energized((0, -1, 2), mirrors, rows, cols)


def part2(file: str):
    mirrors, rows, cols = parse(file)
    edge = []
    for i in range(rows):
        edge.extend([(i, -1, 2), (i, cols, 0)])
    for j in range(cols):
        edge.extend([(-1, j, 3), (rows, j, 1)])
    return max(count_energized(e, mirrors, rows, cols) for e in edge)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
