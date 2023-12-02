def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            allowed = True
            record, game = line.split(":")
            _, num = record.split()
            for pick in game.strip().split("; "):
                for selection in pick.split(", "):
                    match selection.split(" "):
                        case [x, "red"] if int(x) > 12:
                            allowed = False
                        case [x, "green"] if int(x) > 13:
                            allowed = False
                        case [x, "blue"] if int(x) > 14:
                            allowed = False
            if allowed:
                sum += int(num)
    return sum


def part2(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            allowed = True
            record, game = line.split(":")
            _, num = record.split()
            red, green, blue = 0, 0, 0
            for pick in game.strip().split("; "):
                for selection in pick.split(", "):
                    match selection.split(" "):
                        case [x, "red"]:
                            red = max(int(x), red)
                        case [x, "green"]:
                            green = max(int(x), green)
                        case [x, "blue"]:
                            blue = max(int(x), blue)
            sum += red * green * blue
    return sum


if __name__ == '__main__':
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
