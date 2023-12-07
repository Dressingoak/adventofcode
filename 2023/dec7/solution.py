def get_type_from_counts(sorted_counts: list[int]):
    match sorted_counts:
        case [5]:
            return 1  # Five of a kind
        case [1, 4]:
            return 2  # Four of a kind
        case [2, 3]:
            return 3  # Full house
        case [1, 1, 3]:
            return 4  # Three of a kind
        case [1, 2, 2]:
            return 5  # Two pairs
        case [1, 1, 1, 2]:
            return 6  # One pair
        case [1, 1, 1, 1, 1]:
            return 7  # High card
        case _:
            raise


def get_type(hand: str):
    s = {}
    for c in hand:
        if c in s:
            s[c] += 1
        else:
            s[c] = 1
    return get_type_from_counts(sorted(_ for _ in s.values()))


def total_winnings(file: str, values: list[int], type_fun):
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
                            type_fun(hand),
                            *(values.index(c) for c in hand),
                        )
                    )
            max_rank += 1
    hands.sort(key=lambda x: tuple(x[2:]), reverse=True)
    return sum(r * hand[1] for r, hand in zip(range(1, max_rank + 1), hands))


def part1(file: str):
    values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    return total_winnings(file, values, get_type)


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
            return min(types, default=1)
        case _:
            return get_type_from_counts(sorted(_ for _ in s.values()))


def part2(file: str):
    values = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    return total_winnings(file, values, get_type_with_joker)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
