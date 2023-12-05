def part1(file: str, log: bool = False):
    with open(file, "r") as f:
        for line in f.readlines():
            match line.strip().split():
                case ["seeds:", *xs]:
                    xs = [(int(_), False) for _ in xs]
                    if log:
                        print(f"{'seeds' : <25}", end="")
                case [name, "map:"] if log:
                    print(f"{name : <25}", end="")
                case []:
                    xs = [(x, False) for x, _ in xs]
                    if log:
                        print([x for x, _ in xs])
                case [d, s, r]:
                    d, s, r = int(d), int(s), int(r)
                    xs = [
                        (x + (d - s), True)
                        if x in range(s, s + r) and not mapped
                        else (x, mapped)
                        for x, mapped in xs
                    ]
    if log:
        print([x for x, _ in xs])
    return min([x for x, _ in xs])


def split_range(interval: tuple[int, int], s: int, r: int):
    match interval:
        case (o, l):
            if s in range(o, o + l) and s + r in range(o, o + l):
                yield ((o, s - o), False)
                yield ((s, r), True)
                yield ((s + r, o + l - (s + r)), False)
            elif s in range(o, o + l):
                yield ((o, s - o), False)
                yield ((s, o + l - s), True)
            elif s + r in range(o, o + l):
                yield ((o, s + r - o), True)
                yield ((s + r, o + l - (s + r)), False)
            elif s < o and o + l <= s + r:
                yield ((o, l), True)
            else:
                yield ((o, l), False)


def remap(interval: tuple[int, int], mapping: tuple[int, int, int]):
    match (interval, mapping):
        case ((o, l), (d, s, r)):
            for (oo, ll), shift in split_range((o, l), s, r):
                if ll > 0:
                    if shift:
                        yield ((oo + (d - s), ll), True)
                    else:
                        yield ((oo, ll), False)


def part2(file: str):
    with open(file, "r") as f:
        for line in f.readlines():
            match line.strip().split():
                case ["seeds:", *xs]:
                    xs = [((int(o), int(l)), False) for o, l in zip(xs[::2], xs[1::2])]
                case []:
                    xs = [(x, False) for x, _ in xs]
                case [d, s, r]:
                    mapping = (int(d), int(s), int(r))
                    xsn = []
                    for x, mapped in xs:
                        if not mapped:
                            for xn in remap(x, mapping):
                                xsn.append(xn)
                        else:
                            xsn.append((x, True))
                    xs = xsn
    return min(x for (x, _), _ in xs)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
