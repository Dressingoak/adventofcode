def part1(file: str):
    dial = 50
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            r = (-1 if line[0] == "L" else 1) * int(line[1:].strip())
            dial = (dial + r) % 100
            if dial == 0:
                sum += 1
    return sum


def part2(file: str):
    dial = 50
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            r = int(line[1:].strip())
            m = r // 100
            r %= 100
            match line[0]:
                case "L":
                    if dial == 0:
                        dial = 100
                    sum += int(r >= dial) + m
                    dial = (dial - r) % 100
                case "R":
                    sum += int((r + dial) >= 100) + m
                    dial = (dial + r) % 100
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
