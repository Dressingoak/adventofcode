def part1(file: str):
    rounded = {}
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if i == 0:
                top = [0] * len(line)
            for j, pos in enumerate(line):
                match pos:
                    case "O":
                        ii = top[j]
                        top[j] += 1
                        if ii not in rounded:
                            rounded[ii] = 1
                        else:
                            rounded[ii] += 1
                    case "#":
                        top[j] = i + 1
    return sum((i + 1 - ii) * c for ii, c in rounded.items())


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
