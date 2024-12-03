import re

def part1(file: str):
    sum = 0
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    with open(file, "r") as f:
        for line in f.readlines():
            for match in pattern.finditer(line):
                sum += int(match.group(1)) * int(match.group(2))
    return sum

if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
