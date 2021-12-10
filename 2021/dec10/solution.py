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
                return (builder, scores[char])
    return (builder, 0)

def validate_all(lines: list[str]):
    return sum(validate(line)[1] for line in lines)

def autocomplete(line: str):
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    score = 0
    for char in reversed(line):
        score *= 5
        score += scores[char]
    return score

def autocomplete_all(lines: list[str]):
    incomplete = [built for (built, score) in map(validate, lines) if score == 0]
    scores = list(map(autocomplete, incomplete))
    scores.sort()
    return scores[len(scores) // 2]

data = read(file)

print("Dec 10, part 1: {}".format(validate_all(data)))
print("Dec 10, part 2: {}".format(autocomplete_all(data)))
