def part1(file: str):
    tokens = 0
    c = 0
    with open(file, "r") as f:
        for line in f.readlines():
            match c:
                case 0 | 1:
                    if c == 0:
                        arr = []
                    line = line.split(" ")
                    x, y = int(line[2][2:-1]), int(line[3][2:])
                    arr.append((x, y))
                    c += 1
                case 2:
                    line = line.split(" ")
                    x, y = int(line[1][2:-1]), int(line[2][2:])
                    arr.append((x, y))
                    c += 1
                case 3:
                    tokens += minimize_tokens(arr[0], arr[1], arr[2])
                    c = 0
    return tokens


def minimize_tokens(a, b, p):
    """
    Solve
    ```
    A_x * n + B_x * m = P_x
    A_y * n + B_y * m = P_y
    ```
    for integer `n`, `m`. Returns `3 * n + m` if solvable, else 0.
    """
    c0 = p[1] * b[0] - b[1] * p[0]
    c1 = a[1] * b[0] - b[1] * a[0]
    if c0 % c1 == 0:
        n = c0 // c1
        if (p[0] - a[0] * n) % b[0] == 0:
            m = (p[0] - a[0] * n) // b[0]
            return 3 * n + m
    return 0


def part2(file: str):
    tokens = 0
    c = 0
    with open(file, "r") as f:
        for line in f.readlines():
            match c:
                case 0 | 1:
                    if c == 0:
                        arr = []
                    line = line.split(" ")
                    x, y = int(line[2][2:-1]), int(line[3][2:])
                    arr.append((x, y))
                    c += 1
                case 2:
                    line = line.split(" ")
                    x, y = int(line[1][2:-1]), int(line[2][2:])
                    arr.append((x + 10000000000000, y + 10000000000000))
                    tokens += (t := minimize_tokens(arr[0], arr[1], arr[2]))
                    print(f"{t=}")
                    c += 1
                case 3:
                    c = 0
    return tokens


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
