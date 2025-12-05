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


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
