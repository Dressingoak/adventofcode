def forward(values: list[int]):
    diff = [values[i + 1] - values[i] for i in range(len(values) - 1)]
    if all(x == 0 for x in diff):
        return values[-1]
    else:
        return values[-1] + forward(diff)


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            sum += forward([int(_) for _ in line.split(" ")])
    return sum


def backward(values: list[int]):
    diff = [values[i + 1] - values[i] for i in range(len(values) - 1)]
    if all(x == 0 for x in diff):
        return values[0]
    else:
        return values[0] - backward(diff)


def part2(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            sum += backward([int(_) for _ in line.split(" ")])
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
