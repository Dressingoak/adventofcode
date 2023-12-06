def part1(file: str):
    prod = 1
    with open(file, "r") as f:
        for line in f.readlines():
            match line.split():
                case ["Time:", *x]:
                    times = [int(_) for _ in x]
                case ["Distance:", *x]:
                    distances = [int(_) for _ in x]
    for time, distance in zip(times, distances):
        ways = 0
        for t in range(1, time):
            rem = time - t
            if rem * t > distance:
                ways += 1
        prod *= ways
    return prod


def part2(file: str):
    prod = 1
    with open(file, "r") as f:
        for line in f.readlines():
            match line.split(":"):
                case ["Time", x]:
                    time = int("".join(x.split()))
                case ["Distance", x]:
                    distance = int("".join(x.split()))
    ways = 0
    for t in range(1, time):
        rem = time - t
        if rem * t > distance:
            ways += 1
    return ways


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
