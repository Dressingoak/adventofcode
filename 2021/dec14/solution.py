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

known = dict()

def distribution_with_lookup(template: list[str], pairs: dict[tuple[str, str], str], n: int):
    key = (n, tuple(template))
    if key in known:
        return known[key]
    match template:
        case [l, r] if n == 0:
            counts = {l: 2} if l == r else {l: 1, r: 1}
        case [l, r]:
            counts = distribution_with_lookup([l, pairs[(l, r)], r], pairs, n - 1)
        case _:
            counts = {k: v for (k, v) in distribution_with_lookup(template[:2], pairs, n).items()}
            counts[template[1]] -= 1
            for (k, v) in distribution_with_lookup(template[1:], pairs, n).items():
                if k in counts:
                    counts[k] += v
                else:
                    counts[k] = v
    known[key] = counts
    return counts

def compute(template: list[str], pairs: dict[tuple[str, str], str], n: int):
    dist = distribution_with_lookup(template, pairs, n)
    return max(dist.values()) - min(dist.values())

template, pairs = read(file)

print("Dec 14, part 1: {}".format(compute(template, pairs, 10)))
print("Dec 14, part 2: {}".format(compute(template, pairs, 40)))
