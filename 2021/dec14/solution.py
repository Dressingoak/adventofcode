import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> tuple[list[str], dict[tuple[str, str], str]]:
    re_dots = re.compile('(\w)(\w) -> (\w)')
    f = open(file, "r")
    template = [_ for _ in f.readline().strip()]
    f.readline()
    pairs = dict()
    for line in map(lambda x: x.strip(), f.readlines()):
        m = re_dots.match(line)
        l, r, p = m.group(1, 2, 3)
        pairs[(l, r)] = p
    return (template, pairs)

def step(template: list[str], pairs: dict[tuple[str, str], str]):
    new_template = []
    for i in range(len(template) - 1):
        new_template.append(template[i])
        new_template.append(pairs[(template[i], template[i + 1])])
    new_template.append(template[-1])
    return new_template

def step_many(template: list[str], pairs: dict[tuple[str, str], str], n: int):
    new_template = [_ for _ in template]
    for _ in range(n):
        new_template = step(new_template, pairs)
    return new_template

def distribution(template: list[str]):
    counts = dict()
    for char in template:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1
    return counts

def compute(template: list[str], pairs: dict[tuple[str, str], str], n: int):
    final_template = step_many(template, pairs, 10)
    dist = distribution(final_template)
    return max(dist.values()) - min(dist.values())

template, pairs = read(file)

print("Dec 14, part 1: {}".format(compute(template, pairs, 10)))
