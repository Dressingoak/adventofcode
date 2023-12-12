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
    if (row, t := tuple(groups)) in known:
        return known[(row, t)]
    seqs = [seq for seq in row.split(".") if len(seq) > 0]
    count = 0
    for splits in distribute(groups, len(seqs)):
        skip = False
        for r, g in zip(seqs, splits):
            if sum(g) > len(r):
                skip = True
                break
        if skip:
            continue
        inner = 1
        for r, g in zip(seqs, splits):
            if set(r) == set("#"):
                if len(g) != 1 or g[0] != len(r):
                    inner *= 0
                else:
                    inner *= 1
            else:
                inner *= arrangements(r.replace("?", ".", 1), g) + arrangements(
                    r.replace("?", "#", 1), g
                )
        count += inner
    if (row, t) not in known:
        known[(row, t)] = count
    return count


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            row, groups = line.strip().split(" ")
            groups = groups.split(",")
            sum += arrangements(row, [int(_) for _ in groups])
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
