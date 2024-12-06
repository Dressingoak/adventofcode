def part1(file: str):
    sum = 0
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
                case 0:  # left
                    for j in range(j, cols):
                        visited.add((i, j))
                        if map[i][j + 1] == "#":
                            dir = 3
                            break
                case 1:  # up
                    for i in range(i, -1, -1):
                        visited.add((i, j))
                        if map[i - 1][j] == "#":
                            dir = 0
                            break
                case 2:  # right
                    for j in range(j, -1, -1):
                        visited.add((i, j))
                        if map[i][j - 1] == "#":
                            dir = 1
                            break
                case 3:  # down
                    for i in range(i, rows):
                        visited.add((i, j))
                        if map[i + 1][j] == "#":
                            dir = 2
                            break
        except IndexError:
            active = False
    return len(visited)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
