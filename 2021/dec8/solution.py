import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[tuple[list[str], list[str]]]:
    f = open(file, "r")
    return [tuple(_.strip().split() for _ in line.split("|")) for line in f.readlines()]

def count_special_segments(data):
    sizes = [len(s) for entry in data for s in entry[1]]
    accepted = {2, 4, 3, 7}
    return len([s for s in sizes if s in accepted])

def find_by_length(segments: set[str], size: int):
    return list(filter(lambda x: len(x) == size, segments))

def deduce(entry: list[str]):
    sets = [set(_ for _ in s) for s in entry]
    digits = {
        1: find_by_length(sets, 2)[0],
        4: find_by_length(sets, 4)[0],
        7: find_by_length(sets, 3)[0],
        8: find_by_length(sets, 7)[0]
    }
    sixes = find_by_length(sets, 6) # 0, 6, 9
    for digit in sixes:
        if len(digit.difference(digits[4])) == 2:
            digits[9] = digit
        elif len(digit.difference(digits[1])) == 5:
            digits[6] = digit
        else:
            digits[0] = digit
    fives = find_by_length(sets, 5) # 2, 3, 5
    for digit in fives:
        if len(digit.difference(digits[4])) == 3:
            digits[2] = digit
        elif len(digit.difference(digits[6])) == 0:
            digits[5] = digit
        else:
            digits[3] = digit
    return digits

def map_digits(entry: tuple[list[str], list[str]]):
    deduced = deduce(entry[0])
    digits = []
    for number in entry[1]:
        sets = set(_ for _ in number)
        for (value, segments) in deduced.items():
            if sets == segments:
                digits.append(value)
                break
    n = len(digits)
    return sum(d * 10**(n - i - 1) for (i, d) in enumerate(digits))

def sum_output_digits(data: list[tuple[list[str], list[str]]]):
    return sum(map_digits(entry) for entry in data)

data = read(file)

print("Dec 8, part 1: {}".format(count_special_segments(data)))
print("Dec 8, part 2: {}".format(sum_output_digits(data)))
