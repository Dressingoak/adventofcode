def calculate_part1(file: str):
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


if __name__ == '__main__':
    print(f"Part 1: {calculate_part1('input.txt')}")
