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
                    sum += s
                    break
    return sum


def part2(file: str):
    all_seqs = {}
    with open(file, "r") as f:
        for line in f.readlines():
            n = int(line.strip())
            prices = []
            for i, s in enumerate(draw(n)):
                if i == 2000:
                    break
                prices.append(s % 10)
            seqs = set()
            for i in range(4, 2000):
                seq = (
                    prices[i - 3] - prices[i - 4],
                    prices[i - 2] - prices[i - 3],
                    prices[i - 1] - prices[i - 2],
                    prices[i] - prices[i - 1],
                )
                if seq not in seqs:
                    seqs.add(seq)
                    if seq not in all_seqs:
                        all_seqs[seq] = prices[i]
                    else:
                        all_seqs[seq] += prices[i]
    best = max(all_seqs, key=all_seqs.get)
    print(f"Best sequence: {best}")
    return all_seqs[best]


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
