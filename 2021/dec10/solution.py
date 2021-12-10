import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[list[int]]:
    f = open(file, "r")
    return [line.strip() for line in f.readlines()]

def validate(line: str):
    char_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    builder = ""
    for char in line:
        if char in [_ for _ in char_pairs.keys()]:
            builder += char
        elif char in [_ for _ in char_pairs.values()]:
            if char_pairs[builder[-1]] == char:
                builder = builder[:-1]
            else:
                return scores[char]
    return 0

def validate_all(lines: list[str]):
    return sum(validate(line) for line in lines)

data = read(file)

print("Dec 9, part 1: {}".format(validate_all(data)))
