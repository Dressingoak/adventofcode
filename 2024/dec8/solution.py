def part1(file: str):
    sum = 0
    antennas = {}
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            for j, e in enumerate(line.strip()):
                if e != ".":
                    if e in antennas:
                        antennas[e].append((i, j))
                    else:
                        antennas[e] = [(i, j)]
    rows, cols = i + 1, j + 1
    found = set()
    for antennas in antennas.values():
        for il in range(len(antennas) - 1):
            for ir in range(il + 1, len(antennas)):
                l, r = antennas[il], antennas[ir]
                diff = (r[0] - l[0], r[1] - l[1])
                antinodes = [
                    (l[0] - diff[0], l[1] - diff[1]),
                    (r[0] + diff[0], r[1] + diff[1]),
                ]
                for anti in antinodes:
                    if (
                        0 <= anti[0]
                        and anti[0] < rows
                        and 0 <= anti[1]
                        and anti[1] < cols
                        and anti not in found
                    ):
                        sum += 1
                        found.add(anti)
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
