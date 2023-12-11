def part1(file: str):
    galaxies = []
    dist = 0
    with open(file, "r") as f:
        ii = 0
        cols = []
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if len(cols) == 0:
                cols = [
                    0,
                ] * len(line)
            found = 0
            for j, v in enumerate(_ for _ in line):
                if v == "#":
                    found += 1
                    galaxies.append((i + ii, j))
                    cols[j] += 1
            if found == 0:
                ii += 1
    jj = 0
    galaxies2 = []
    for j, v in enumerate(cols):
        if v == 0:
            jj += 1
        galaxies2.extend((i, l + jj) for (i, l) in galaxies if j == l)
    for i, (i1, j1) in enumerate(galaxies2):
        for i2, j2 in galaxies2[(i + 1) :]:
            d = abs(i1 - i2) + abs(j1 - j2)
            dist += d
    return dist


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
