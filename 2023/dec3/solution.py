def read_input(
    file: str,
) -> (dict[tuple[int, int], str], list[int, list[tuple[int, int]]]):
    grid = {}
    digits = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            digit = 0
            digit_len = 0
            for j, char in enumerate(line):
                try:
                    d = int(char)
                    digit *= 10
                    digit += d
                    digit_len += 1
                except ValueError:
                    if digit > 0:
                        digits.append(
                            (digit, set([(i, k) for k in range(j - digit_len, j)]))
                        )
                        digit = 0
                        digit_len = 0
                    match char:
                        case "." | "\n":
                            pass
                        case _:
                            grid[(i, j)] = char
    return grid, digits


def part1(file: str):
    sum = 0
    grid, digits = read_input(file)
    for digit, positions in digits:
        b = False
        for i, j in positions:
            for ii in range(i - 1, i + 2):
                if b:
                    break
                for jj in range(j - 1, j + 2):
                    if (ii, jj) in grid:
                        sum += digit
                        b = True
                        break
                if b:
                    break
    return sum


def part2(file: str):
    sum = 0
    grid, digits = read_input(file)
    outline = {}
    for digit, positions in digits:
        for i, j in positions:
            for ii in range(i - 1, i + 2):
                for jj in range(j - 1, j + 2):
                    if (ii, jj) not in positions and (ii, jj) in grid:
                        if (ii, jj) not in outline:
                            outline[(ii, jj)] = set()
                        outline[(ii, jj)].add((grid[(ii, jj)], digit))
    for _, s in outline.items():
        match list(s):
            case [("*", l), ("*", r)]:
                sum += l * r
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
