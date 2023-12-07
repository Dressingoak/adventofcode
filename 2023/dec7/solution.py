def get_value(hand: str, values: list[int]):
    s = 0
    for c in hand:
        s *= 13
        s += 13 - values.index(c)
    return s


def get_type_from_counts(sorted_counts: list[int]):
    s = {}
    match sorted_counts:
        case [5]:
            return 7  # Five of a kind
        case [1, 4]:
            return 6  # Four of a kind
        case [2, 3]:
            return 5  # Full house
        case [1, 1, 3]:
            return 4  # Three of a kind
        case [1, 2, 2]:
            return 3  # Two pairs
        case [1, 1, 1, 2]:
            return 2  # One pair
        case [1, 1, 1, 1, 1]:
            return 1  # High card


def get_type(hand: str):
    s = {}
    for c in hand:
        if c in s:
            s[c] += 1
        else:
            s[c] = 1
    return get_type_from_counts(sorted(_ for _ in s.values()))


def part1(file: str):
    values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    max_rank = 0
    hands = []
    with open(file, "r") as f:
        for line in f.readlines():
            match line.split():
                case [hand, bid]:
                    hands.append(
                        (hand, int(bid), get_type(hand), get_value(hand, values))
                    )
            max_rank += 1
    hands.sort(key=lambda x: (x[2], x[3]))
    return sum(r * hand[1] for r, hand in zip(range(1, max_rank + 1), hands))


def get_type_with_joker(hand: str):
    s = {}
    for c in hand:
        if c in s:
            s[c] += 1
        else:
            s[c] = 1
    match s:
        case {"J": count, **remaining}:
            types = []
            for k in remaining.keys():
                s_n = sorted(
                    vv if kk != k else vv + count for kk, vv in remaining.items()
                )
                types.append(get_type_from_counts(s_n))
            return max(types, default=7)
        case _:
            return get_type_from_counts(sorted(_ for _ in s.values()))


def part2(file: str):
    values = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    max_rank = 0
    hands = []
    with open(file, "r") as f:
        for line in f.readlines():
            match line.split():
                case [hand, bid]:
                    hands.append(
                        (
                            hand,
                            int(bid),
                            get_type_with_joker(hand),
                            get_value(hand, values),
                        )
                    )
            max_rank += 1
    hands.sort(key=lambda x: (x[2], x[3]))
    return sum(r * hand[1] for r, hand in zip(range(1, max_rank + 1), hands))


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
