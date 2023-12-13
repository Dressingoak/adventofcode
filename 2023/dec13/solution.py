def parse(file: str):
    with open(file, "r") as f:
        rows = []
        for line in f.readlines():
            match line.strip():
                case "":
                    yield rows
                    rows = []
                case row:
                    cs = [c == "#" for c in row]
                    rows.append(cs)
    yield rows


def find_reflection(lst: list[int]):
    s = len(lst)
    odd = s % 2 == 1
    m = s // 2 - 1
    for i in range(s - 1):
        sub = 2 * max(0, i - m)
        size = i + 1 - sub + (1 if sub > 0 and odd else 0)
        cont = False
        for l, r in zip(lst[(i + 1 - size) : i + 1], lst[i + size : i : -1]):
            if l != r:
                cont = True
                break
        if cont:
            continue
        yield i + 1


def get_mirror_value(rows: list[list[bool]]):
    rw, cw = [], [0] * len(rows[0])
    for i, row in enumerate(rows):
        r = 0
        for j, col in enumerate(row):
            if col:
                r += 2**j
                cw[j] += 2**i
        rw.append(r)
    for i in find_reflection(rw):
        yield i * 100
    for j in find_reflection(cw):
        yield j


def part1(file: str):
    return sum(next(get_mirror_value(rows)) for rows in parse(file))


def get_mirror_value_corrected(rows: list[list[bool]]):
    y = next(get_mirror_value(rows))
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = not rows[i][j]
            for x in get_mirror_value(rows):
                if x == y:
                    continue
                return x
            rows[i][j] = not rows[i][j]


def part2(file: str):
    return sum(get_mirror_value_corrected(rows) for rows in parse(file))


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
