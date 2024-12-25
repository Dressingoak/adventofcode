def part1(file: str):
    locks = []
    keys = []
    with open(file, "r") as f:
        parsing = False
        for line in f.readlines():
            line = line.strip()
            if not parsing:
                filled = [
                    0,
                ] * 5
                if line == "#####":
                    is_key = False
                else:
                    is_key = True
                parsing = True
            elif line == "":
                parsing = False
                if is_key:
                    keys.append([x - 1 for x in filled])
                else:
                    locks.append(filled)
            else:
                for i, x in enumerate(line):
                    if x == "#":
                        filled[i] += 1
    if is_key:
        keys.append([x - 1 for x in filled])
    else:
        locks.append(filled)

    fits = 0
    for lock in locks:
        for key in keys:
            fits += all(x + y <= 5 for x, y in zip(key, lock))
    return fits


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
