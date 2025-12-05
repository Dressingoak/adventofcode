def part1(file: str):
    ranges = []
    c = 0
    with open(file, "r") as f:
        r = True
        for line in f.readlines():
            if (l := line.strip()) == "":
                r = False
                continue
            if r:
                a, b = l.split("-")
                ranges.append((int(a), int(b)))
            else:
                n = int(l)
                for a, b in ranges:
                    if n >= a and n <= b:
                        c += 1
                        break
    return c


def union(i1: tuple[int, int], i2: tuple[int, int]):
    x1, x2 = i1
    y1, y2 = i2
    if y1 < x1:
        yield from union(i2, i1)
    elif y1 <= x2 and y2 <= x2:
        yield i1
    elif y1 <= x2 and y2 > x2:
        yield (x1, y2)
    elif x2 < y1:
        yield i1
        yield i2


def reduce_intervals(intervals: list[tuple[int, int]], start_i=0):
    for i in range(start_i, n := len(intervals)):
        for j in range(i + 1, n):
            s = set(union(intervals[i], intervals[j]))
            if len(s) == 2:
                continue
            else:
                p = s.pop()
                to_reduce = (
                    intervals[:i] + [p] + intervals[i + 1 : j] + intervals[j + 1 :]
                )
                return reduce_intervals(to_reduce, i)
    return intervals


def part2(file: str):
    ranges = list()
    with open(file, "r") as f:
        for line in f.readlines():
            if (l := line.strip()) == "":
                break
            a, b = l.split("-")
            a, b = int(a), int(b) + 1  # left-inclusive, right-exclusive
            ranges.append((a, b))
    ingredients = 0
    for a, b in reduce_intervals(sorted(ranges)):
        ingredients += b - a
    return ingredients


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
