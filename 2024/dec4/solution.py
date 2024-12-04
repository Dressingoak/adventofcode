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


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
