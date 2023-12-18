def det(x1, y1, x2, y2):
    return x1 * y2 - x2 * y1


def nodes(x, y, prv, nxt):
    match prv, nxt:
        case "U", "L":
            return (x, y), (x + 1, y + 1)
        case "U", "R":
            return (x, y + 1), (x + 1, y)
        case None, "U":
            return (x, y + 1), (x + 1, y + 1)

        case "L", "U":
            return (x, y), (x + 1, y + 1)
        case "L", "D":
            return (x + 1, y), (x, y + 1)
        case None, "L":
            return (x, y), (x, y + 1)

        case "D", "L":
            return (x + 1, y), (x, y + 1)
        case "D", "R":
            return (x + 1, y + 1), (x, y)
        case None, "D":
            return (x + 1, y), (x, y)

        case "R", "U":
            return (x, y + 1), (x + 1, y)
        case "R", "D":
            return (x + 1, y + 1), (x, y)
        case None, "R":
            return (x + 1, y + 1), (x + 1, y)


def shoelace(gen):
    points = []
    prv = None
    x, y = 0, 0

    for nxt, amount in gen():
        if prv is None:
            first = nxt
            prv = nxt
            continue
        match prv:
            case None:
                pass
            case _:
                points.append(nodes(x, y, prv, nxt))
        match nxt:
            case "U":
                y += amount
            case "L":
                x -= amount
            case "D":
                y -= amount
            case "R":
                x += amount
        prv = nxt
    points.append(nodes(x, y, prv, first))

    dets = [0, 0]
    for i in range(-1, len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        for n in range(2):
            dets[n] += det(p1[n][0], p1[n][1], p2[n][0], p2[n][1])
    areas = [abs(_) // 2 for _ in dets]
    return max(areas)


def part1(file: str):
    def gen():
        with open(file, "r") as f:
            for line in f.readlines():
                nxt, amount, _ = line.split(" ", 2)
                yield nxt, int(amount)

    return shoelace(gen)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
