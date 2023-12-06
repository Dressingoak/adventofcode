def isqrt(v: int):
    """Calculate integer floor(sqrt(v)) by bisection"""
    l, r = 0, v + 1
    while l != r - 1:
        c = (l + r) // 2
        if c**2 <= v:
            l = c
        else:
            r = c
    return l


def ways(time: int, distance: int) -> int:
    """Count ways to reach further than distance by solving
    ```
    t * (time - t) > distance
    ```
    for integer `t` and counting elements of the solution set.
    """
    d = time**2 - 4 * distance  # discriminant of the derived quadratic equation
    d_rt = r if (r := isqrt(d)) ** 2 == d else r + 1
    l_lower, r_upper = (time - d_rt) // 2, ((time + d_rt) - 1) // 2 + 1
    while l_lower * (time - l_lower) <= distance:
        l_lower += 1
    while r_upper * (time - r_upper) <= distance:
        r_upper -= 1
    return r_upper - l_lower + 1


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
        prod *= ways(time, distance)
    return prod


def part2(file: str):
    with open(file, "r") as f:
        for line in f.readlines():
            match line.split(":"):
                case ["Time", x]:
                    time = int("".join(x.split()))
                case ["Distance", x]:
                    distance = int("".join(x.split()))
    return ways(time, distance)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
