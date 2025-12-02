def digit_length(a) -> int:
    if a == 0:
        return 1
    m = 0
    while a // 10**m > 0:
        m += 1
    return m


def is_invalid(a) -> bool:
    if (m := digit_length(a)) % 2 == 1:
        return False
    else:
        n = m // 2
        s = str(a)
        return s[0:n] == s[n:m]


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for r in f.readline().strip().split(","):
            l, h = r.split("-")
            l, h = int(l), int(h)
            for n in range(l, h + 1):
                if is_invalid(n):
                    sum += n
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
