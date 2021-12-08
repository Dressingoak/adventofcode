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

data = read(file)

print("Dec 8, part 1: {}".format(count_special_segments(data)))
