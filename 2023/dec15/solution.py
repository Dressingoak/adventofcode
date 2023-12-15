def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            for seq in line.strip().split(","):
                current_value = 0
                for char in seq:
                    current_value += ord(char)
                    current_value *= 17
                    current_value %= 256
                sum += current_value
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
