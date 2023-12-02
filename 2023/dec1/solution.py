def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            first = True
            last = None
            for char in line:
                try:
                    v = int(char)
                    if first:
                        sum += v * 10
                        first = False
                    last = v
                except:
                    pass
            sum += last
    return sum


def part2(file: str):
    digits = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "1": 1, 
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6, 
        "7": 7, 
        "8": 8, 
        "9": 9,
    }

    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            full = len(line)
            first = True
            last = None
            loc = 0

            while full - loc > 0:
                for pattern, value in digits.items():
                    if line[loc:].startswith(pattern):
                        if first:
                            sum += value * 10
                            first = False
                        last = value
                        break
                loc += 1
            sum += last
    return sum


if __name__ == '__main__':
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
