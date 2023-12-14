def part1(file: str):
    rounded = {}
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if i == 0:
                top = [0] * len(line)
            for j, pos in enumerate(line):
                match pos:
                    case "O":
                        ii = top[j]
                        top[j] += 1
                        if ii not in rounded:
                            rounded[ii] = 1
                        else:
                            rounded[ii] += 1
                    case "#":
                        top[j] = i + 1
    return sum((i + 1 - ii) * c for ii, c in rounded.items())


def part2(file: str):
    positions = {}
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            for j, pos in enumerate(line):
                match pos:
                    case "O" | "#":
                        positions[(i, j)] = pos
    rows, cols = i + 1, j

    seen = [sorted([k for k, v in positions.items() if v == "O"])]
    start = None

    N = 1_000_000_000

    for _ in range(N):
        # North
        for j in range(cols):
            top = -1
            for i in range(rows):
                match positions.get((i, j)):
                    case "O" if i != top:
                        del positions[(i, j)]
                        top += 1
                        positions[(top, j)] = "O"
                    case "#":
                        top = i

        # West
        for i in range(rows):
            left = -1
            for j in range(cols):
                match positions.get((i, j)):
                    case "O" if j != left:
                        del positions[(i, j)]
                        left += 1
                        positions[(i, left)] = "O"
                    case "#":
                        left = j

        # South
        for j in range(cols):
            bottom = rows
            for i in range(rows - 1, -1, -1):
                match positions.get((i, j)):
                    case "O" if i != bottom:
                        del positions[(i, j)]
                        bottom -= 1
                        positions[(bottom, j)] = "O"
                    case "#":
                        bottom = i

        # East
        for i in range(rows):
            right = cols
            for j in range(cols - 1, -1, -1):
                match positions.get((i, j)):
                    case "O" if j != right:
                        del positions[(i, j)]
                        right -= 1
                        positions[(i, right)] = "O"
                    case "#":
                        right = j

        ordered = sorted([k for k, v in positions.items() if v == "O"])
        try:
            start = seen.index(ordered)
        except ValueError:
            seen.append(ordered)
        if start is not None:
            break

    period = len(seen[start:])
    index = (N - start) % period + start
    return sum(rows - i for i, j in seen[index])


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
