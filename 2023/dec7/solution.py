values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


def get_value(hand: str):
    s = 0
    for c in hand:
        s *= 13
        s += 13 - values.index(c)
    return s


def analyze(hand: str):
    s = {}
    for c in hand:
        if c in s:
            s[c] += 1
        else:
            s[c] = 1
    hand_value = get_value(hand)
    match sorted(_ for _ in s.values()):
        case [5]:
            return (7, hand_value)  # Five of a kind
        case [1, 4]:
            return (6, hand_value)  # Four of a kind
        case [2, 3]:
            return (5, hand_value)  # Full house
        case [1, 1, 3]:
            return (4, hand_value)  # Three of a kind
        case [1, 2, 2]:
            return (3, hand_value)  # Two pairs
        case [1, 1, 1, 2]:
            return (2, hand_value)  # One pair
        case [1, 1, 1, 1, 1]:
            return (1, hand_value)  # High card


def part1(file: str):
    max_rank = 0
    hands = []
    with open(file, "r") as f:
        for line in f.readlines():
            match line.split():
                case [hand, bid]:
                    print(hand, get_value(hand))
                    hands.append((hand, int(bid), *analyze(hand)))
            max_rank += 1
    hands.sort(key=lambda x: (x[2], x[3]))
    return sum(r * hand[1] for r, hand in zip(range(1, max_rank + 1), hands))


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
