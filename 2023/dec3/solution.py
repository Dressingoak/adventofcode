def part1(file: str):
    sum = 0
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
                except:
                    if digit > 0:
                        digits.append((digit, [(i, k) for k in range(j - digit_len, j)]))
                        digit = 0
                        digit_len = 0
                    match char:
                        case '.' | '\n': pass
                        case _:
                            grid[(i, j)] = char
    for (digit, positions) in digits:
        b = False
        for (i, j) in positions:
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


if __name__ == '__main__':
    print(f"{part1('input.txt')=}")
