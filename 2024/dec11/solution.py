def number_len(n):
    if (m := n // 10) == 0:
        return 1
    return 1 + number_len(m)


def count_stones(stone, remaining):
    if remaining == 0:
        return 1
    if stone == 0:
        return count_stones(1, remaining - 1)
    elif (l := number_len(stone)) % 2 == 0:
        m = 10 ** (l // 2)
        a, b = stone // m, stone % m
        return count_stones(a, remaining - 1) + count_stones(b, remaining - 1)
    else:
        return count_stones(stone * 2024, remaining - 1)


def part1(file: str):
    count = 0
    with open(file, "r") as f:
        stones = [int(_) for _ in f.readline().split(" ")]
    seen = {}

    for stone in stones:
        count += count_stones(stone, 25)

    return count


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
