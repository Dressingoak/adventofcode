def number_len(n: int):
    if (m := n // 10) == 0:
        return 1
    return 1 + number_len(m)


def blink(stone: int):
    if stone == 0:
        yield 1
    elif (l := number_len(stone)) % 2 == 0:
        m = 10 ** (l // 2)
        yield stone // m
        yield stone % m
    else:
        yield stone * 2024


def count_stones(stones: dict[int, int]):
    nxt = {}
    for stone, count in stones.items():
        for nxt_stone in blink(stone):
            if nxt_stone not in nxt:
                nxt[nxt_stone] = count
            else:
                nxt[nxt_stone] += count
    return nxt


def solve(file: str, n: int):
    with open(file, "r") as f:
        stones = {int(_): 1 for _ in f.readline().split(" ")}
    for _ in range(n):
        stones = count_stones(stones)
    return sum(count for count in stones.values())


def part1(file: str):
    return solve(file, 25)


def part2(file: str):
    return solve(file, 75)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
