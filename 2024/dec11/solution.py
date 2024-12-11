def number_len(n):
    if (m := n // 10) == 0:
        return 1
    return 1 + number_len(m)


def count_stones(stone, remaining, known):
    if remaining == 0:
        return 1
    if (stone, remaining) in known:
        return known[(stone, remaining)]
    if stone == 0:
        value = count_stones(1, remaining - 1, known)
    elif (l := number_len(stone)) % 2 == 0:
        m = 10 ** (l // 2)
        a, b = stone // m, stone % m
        value = count_stones(a, remaining - 1, known) + count_stones(
            b, remaining - 1, known
        )
    else:
        value = count_stones(stone * 2024, remaining - 1, known)
    known[(stone, remaining)] = value
    return value


def solve(file: str, n: int):
    count = 0
    with open(file, "r") as f:
        stones = [int(_) for _ in f.readline().split(" ")]
    known = {}
    for stone in stones:
        count += count_stones(stone, n, known)
    return count


def part1(file: str):
    return solve(file, 25)


def part2(file: str):
    return solve(file, 75)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
