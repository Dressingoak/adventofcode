def mix(n, s):
    return n ^ s


def prune(s):
    return s % 16777216


def draw(n):
    yield n
    while True:
        n = prune(mix(n * 64, n))
        n = prune(mix(n // 32, n))
        n = prune(mix(n * 2048, n))
        yield n


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            n = int(line.strip())
            for i, s in enumerate(draw(n)):
                if i == 2000:
                    # print(f"{n}: {s}")
                    sum += s
                    break
    return sum


def price(n):
    prev = None
    for s in draw(n):
        m = s % 10
        yield m, (m - prev if prev is not None else None)
        prev = m


def anticipate(n, seq):
    l4, l3, l2, l1 = None, None, None, None
    for i, (p, d) in enumerate(price(n)):
        if i == 2000:
            return None
        l4, l3, l2, l1 = l3, l2, l1, d
        if (l4, l3, l2, l1) == seq:
            return p


def seqs(base, offset):
    for i in range(base**4):
        l4 = (i // base**3) % base - offset
        l3 = (i // base**2) % base - offset
        l2 = (i // base**1) % base - offset
        l1 = (i // base**0) % base - offset
        yield (l4, l3, l2, l1)


def part2(file: str):
    max = 0
    best = None
    secrets = []
    with open(file, "r") as f:
        for line in f.readlines():
            secrets.append(int(line.strip()))
    for seq in seqs(19, 9):
        sum = 0
        for n in secrets:
            price = anticipate(n, seq)
            if price is not None:
                sum += price
        if sum > max:
            max = sum
            best = seq
            print(seq, sum)
    print(max, best)
    return max


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
