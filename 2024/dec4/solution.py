def check_substring(s):
    return "XMAS" == s or "SAMX" == s


def part1(file: str):
    count = 0
    grid = []
    with open(file, "r") as f:
        for line in f.readlines():
            grid.append(line.strip())
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols - 3):
            s = grid[i][j : j + 4]
            count += int(check_substring(s))
    for i in range(rows - 3):
        for j in range(cols):
            s = "".join(grid[i + k][j] for k in range(4))
            count += int(check_substring(s))
    for i in range(rows - 3):
        for j in range(cols - 3):
            s = "".join(grid[i + k][j + k] for k in range(4))
            count += int(check_substring(s))
    for i in range(rows - 3):
        for j in range(3, cols):
            s = "".join(grid[i + k][j - k] for k in range(4))
            count += int(check_substring(s))
    return count


def part2(file: str):
    count = 0
    grid = []
    with open(file, "r") as f:
        for line in f.readlines():
            grid.append(line.strip())
    rows, cols = len(grid), len(grid[0])
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if grid[i][j] == "A":
                match [grid[i - 1][j - 1], grid[i + 1][j + 1]]:
                    case ["M", "S"] | ["S", "M"]:
                        match [grid[i - 1][j + 1], grid[i + 1][j - 1]]:
                            case ["M", "S"] | ["S", "M"]:
                                count += 1
    return count


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
