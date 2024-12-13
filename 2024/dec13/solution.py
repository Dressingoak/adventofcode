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


def minimize_tokens(a, b, dst):
    dx, dy = dst
    for pa in range(100):
        x0, y0 = pa * a[0], pa * a[1]
        for pb in range(100):
            x = x0 + pb * b[0]
            y = y0 + pb * b[1]
            if dx < x or dy < y:
                break
            elif dx == x and dy == y:
                return pa * 3 + pb
    return 0


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
