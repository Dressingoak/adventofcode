def det(x1, y1, x2, y2):
    return x1 * y2 - x2 * y1


def shoelace_with_picks(gen):
    x0, y0 = 0, 0
    x, y = 0, 0
    b = 0
    signed_double_area = 0
    for nxt, amount in gen():
        b += amount
        match nxt:
            case "U":
                y += amount
            case "L":
                x -= amount
            case "D":
                y -= amount
            case "R":
                x += amount
        signed_double_area += det(x0, y0, x, y)  # The Shoelace formula
        x0, y0 = (x, y)
    A = abs(signed_double_area // 2)
    # Pick's theorem: For a simple polygon, the area is given by
    #   A = i + b / 2 - 1
    # where A is the area, i in the interior integer points and b is the points on the boundary.
    # We calculate A with the Shoelace formula, and we seek i + b = A + b / 2 + 1
    return A + b // 2 + 1


def part1(file: str):
    def gen():
        with open(file, "r") as f:
            for line in f.readlines():
                nxt, amount, _ = line.split(" ", 2)
                yield nxt, int(amount)

    return shoelace_with_picks(gen)


def part2(file: str):
    def gen():
        with open(file, "r") as f:
            for line in f.readlines():
                _, _, data = line.split(" ")
                amount = int(data[2:7], 16)
                match data[7]:
                    case "0":
                        nxt = "R"
                    case "1":
                        nxt = "D"
                    case "2":
                        nxt = "L"
                    case "3":
                        nxt = "U"
                yield nxt, amount

    return shoelace_with_picks(gen)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
