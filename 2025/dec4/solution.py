def part1(file: str):
    s = 0
    with open(file, "r") as f:
        rolls = []
        for line in f.readlines():
            rolls.append([int(x == "@") for x in line.strip()])
    n, m = len(rolls), len(rolls[0])
    for i in range(n):
        for j in range(m):
            if not rolls[i][j]:
                continue
            c = 0
            for k in range(-1 if i > 0 else 0, 2 if i < n - 1 else 1):
                for l in range(-1 if j > 0 else 0, 2 if j < m - 1 else 1):
                    if k == 0 and l == 0:
                        continue
                    c += rolls[i + k][j + l]
            if c < 4:
                s += 1
    return s


def remove_rolls(rolls):
    s = 0
    n, m = len(rolls), len(rolls[0])
    after = [[False for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if not rolls[i][j]:
                continue
            c = 0
            for k in range(-1 if i > 0 else 0, 2 if i < n - 1 else 1):
                for l in range(-1 if j > 0 else 0, 2 if j < m - 1 else 1):
                    if k == 0 and l == 0:
                        continue
                    c += rolls[i + k][j + l]
            if c < 4:
                s += 1
            else:
                after[i][j] = True
    return s, after


def part2(file: str):
    ss = 0
    with open(file, "r") as f:
        rolls = []
        for line in f.readlines():
            rolls.append([int(x == "@") for x in line.strip()])
    while True:
        s, rolls = remove_rolls(rolls)
        ss += s
        if s == 0:
            break
    return ss


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
