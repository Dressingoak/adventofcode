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
        return i + 1


def get_mirror_value(rows: list[list[bool]]):
    rw, cw = [], [0] * len(rows[0])
    for i, row in enumerate(rows):
        r = 0
        for j, col in enumerate(row):
            if col:
                r += 2**j
                cw[j] += 2**i
        rw.append(r)
    if v := find_reflection(rw):
        return v * 100
    elif v := find_reflection(cw):
        return v
    else:
        return 0


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        rows = []
        for line in f.readlines():
            match line.strip():
                case "":
                    sum += get_mirror_value(rows)
                    rows = []
                case row:
                    cs = [c == "#" for c in row]
                    rows.append(cs)
    sum += get_mirror_value(rows)
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
