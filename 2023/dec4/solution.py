def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            _, numbers = line.split(":")
            winning, actual = numbers.split("|")
            winning = set([int(i) for i in winning.split()])
            n = None
            for x in actual.split():
                if int(x) in winning:
                    if n is None:
                        n = 1
                    else:
                        n *= 2
            if n is not None:
                sum += n
    return sum


def part2(file: str):
    cards = {}
    with open(file, "r") as f:
        for line in f.readlines():
            card, numbers = line.split(":")
            _, num = card.split()
            num = int(num)
            if num not in cards:
                cards[num] = 1
            else:
                cards[num] += 1
            winning, actual = numbers.split("|")
            winning = set([int(i) for i in winning.split()])
            matches = sum(1 for _ in winning.intersection(int(i) for i in actual.split()))
            for i in range(num + 1, num + matches + 1):
                if i not in cards:
                    cards[i] = cards[num]
                else:
                    cards[i] += cards[num]
    return sum(v for v in cards.values())


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
