def iter(numbers: list[int], concat: bool):
    """Applies operators right-to-left"""
    if len(numbers) == 1:
        yield numbers[0]
    else:
        for res in iter(numbers[1:], concat):
            yield numbers[0] + res
            yield numbers[0] * res
            if concat:
                yield int(str(res) + str(numbers[0]))


def solve(file: str, concat: bool):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            parts = line.split(" ")
            result = int(parts[0][:-1])
            numbers = [int(_) for _ in parts[-1 : -len(parts) : -1]]
            possible = False
            for x in iter(numbers, concat):
                if x == result:
                    possible = True
                    break
            if possible:
                sum += result
    return sum


def part1(file: str):
    return solve(file, False)


def part2(file: str):
    return solve(file, True)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
