def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            _, numbers = line.split(":")
            winning, actual = numbers.split("|")
            winning = set([int(i) for i in winning.split()])
            n = None
            for x in actual.split():
                if int(x) in winning:
                    if n is None:
                        n = 1
                    else:
                        n *= 2
            if n is not None:
                sum += n
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
