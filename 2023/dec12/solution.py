def splits(i, count):
    for v in range(i + 1):
        if i == 0 and count == 0:
            yield ()
        elif count > 0:
            for other in splits(i - v, count - 1):
                yield v, *other


def distribute(lst: list[int], count: int):
    for split in splits(len(lst), count):
        lsts = []
        last = 0
        for i in split:
            lsts.append(lst[last : last + i])
            last += i
        yield lsts


known = {}


def arrangements(row: str, groups: list[int]):
    print(len(known))
    if (row, t := tuple(groups)) in known:
        return known[(row, t)]
    seqs = [seq for seq in row.split(".") if len(seq) > 0]
    limits = [(seq.count("#"), len(seq)) for seq in seqs]
    count = 0
    for k, splits in enumerate(distribute(groups, len(seqs))):
        if k % 1_000_000 == 0:
            print(k)
        valid = True
        for (lo, hi), g in zip(limits, splits):
            s = sum(g, 0)
            if (c := len(g)) > 0:
                s += c - 1
            if lo > s or hi < s:
                valid = False
                break
        if not valid:
            continue
        inner = 1
        for r, (lo, hi), g in zip(seqs, limits, splits):
            if hi - lo == 0:
                continue  # All '#'
            dots = arrangements(r.replace("?", ".", 1).strip("."), g)
            subs = r.replace("?", "#", 1)
            match subs.find("?"):
                case -1 if len(g) > 0 and len(subs) == g[0]:
                    squares = 1
                case -1:
                    squares = 0
                case index if len(g) > 0 and index <= g[0]:
                    squares = arrangements(subs, g)
                case _:
                    squares = 0
            inner *= dots + squares
        count += inner
    known[(row, t)] = count
    return count


def count_seqs(file: str, mul: int = 1):
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row, groups = line.strip().split(" ")
            groups = [int(_) for _ in groups.split(",")]
            seqs = [seq for seq in row.split(".") if len(seq) > 0]
            row, groups = "?".join([row] * mul), groups * mul
            print(f"{i}: ", end="")
            size = 0
            for _ in distribute(groups, len(seqs)):
                size += 1
            print(size)


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row, groups = line.strip().split(" ")
            groups = [int(_) for _ in groups.split(",")]
            sum += (v := arrangements(row, groups))
            print(f"{i=}: {v}")
    return sum


def part2(file: str):
    sum = 0
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            row, groups = line.strip().split(" ")
            groups = [int(_) for _ in groups.split(",")]
            sum += arrangements("?".join([row] * 5), groups * 5)
            print(i)
    return sum


if __name__ == "__main__":
    count_seqs("input.txt", 5)
    # print(f"{part2('test.txt')=}")
    # print(len(known))

    # print(f"{part2('test.txt')=}")
