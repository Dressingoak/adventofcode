def plot(robots, size: tuple[int, int]):
    for i in range(size[1]):
        for j in range(size[0]):
            if (i, j) not in robots:
                print(".", end="")
            else:
                print(robots[(i, j)], end="")
        print("")


def solve(file: str, size: tuple[int, int]):
    rows, cols = size[1], size[0]
    quadrants = {i: 0 for i in range(4)}
    robots = {}
    with open(file, "r") as f:
        for line in f.readlines():
            p, v = line.split(" ")
            p = p.split("=")[1].split(",")
            p = (int(p[1]), int(p[0]))
            v = v.split("=")[1].split(",")
            v = (int(v[1]), int(v[0]))
            for _ in range(100):
                p = ((p[0] + v[0]) % rows, (p[1] + v[1]) % cols)
            if p not in robots:
                robots[p] = 1
            else:
                robots[p] += 1
            match p:
                case _ if p[0] < rows // 2 and p[1] < cols // 2:
                    quadrants[0] += 1
                case _ if p[0] < rows // 2 and p[1] > cols // 2:
                    quadrants[1] += 1
                case _ if p[0] > rows // 2 and p[1] < cols // 2:
                    quadrants[2] += 1
                case _ if p[0] > rows // 2 and p[1] > cols // 2:
                    quadrants[3] += 1
    safety_factor = 1
    # plot(robots, size)
    for c in quadrants.values():
        safety_factor *= c
    return safety_factor


def part1(file: str):
    if file == "input.txt":
        return solve(file, (101, 103))
    else:
        return solve(file, (11, 7))


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
