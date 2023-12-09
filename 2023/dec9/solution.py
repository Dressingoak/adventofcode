def predict(values: list[int]):
    diff = [values[i + 1] - values[i] for i in range(len(values) - 1)]
    if all(x == 0 for x in diff):
        return values[-1]
    else:
        return values[-1] + predict(diff)


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            sum += predict([int(_) for _ in line.split(" ")])
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
