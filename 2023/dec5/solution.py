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


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
