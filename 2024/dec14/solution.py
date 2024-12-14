def plot(robots, size: tuple[int, int]):
    for i in range(size[1]):
        for j in range(size[0]):
            if (i, j) not in robots:
                print(".", end="")
            else:
                print(robots[(i, j)], end="")
        print("")


def solve_part1(file: str, size: tuple[int, int]):
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


def solve_part2(file: str, size: tuple[int, int]):
    rows, cols = size[1], size[0]
    quadrants = {i: 0 for i in range(4)}
    robots = []
    with open(file, "r") as f:
        for line in f.readlines():
            p, v = line.split(" ")
            p = p.split("=")[1].split(",")
            p = (int(p[1]), int(p[0]))
            v = v.split("=")[1].split(",")
            v = (int(v[1]), int(v[0]))
            robots.append((p, v))
    c = 0
    while True:
        c += 1
        robot_count = {}
        for i in range(len(robots)):
            p, v = robots[i]
            p = ((p[0] + v[0]) % rows, (p[1] + v[1]) % cols)
            robots[i] = (p, v)
            if p not in robot_count:
                robot_count[p] = 1
            else:
                robot_count[p] += 1
        line = 10
        for i in range(size[1] - line):
            for j in range(size[0] - line):
                # When a suspiciously long line of robots appear, maybe that is it?
                if all((i, j + k) in robot_count for k in range(line)):
                    plot(robot_count, size)
                    return c


def part1(file: str):
    if file == "input.txt":
        return solve_part1(file, (101, 103))
    else:
        return solve_part1(file, (11, 7))


def part2(file: str):
    if file == "input.txt":
        return solve_part2(file, (101, 103))
    else:
        return 0  # Input needs to support it


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
