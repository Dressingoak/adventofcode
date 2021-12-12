import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[tuple[str, str]]:
    f = open(file, "r")
    return [tuple(_ for _ in line.strip().split("-")) for line in f.readlines()]

def connections(data: list[tuple[str, str]]):
    g = dict()
    for (l, r) in data:
        if l not in g:
            g[l] = {r}
        else:
            g[l].add(r)
        if r not in g:
            g[r] = {l}
        else:
            g[r].add(l)
    return g

def paths(g: dict[str, set[str]], c: str = "start", s: list[str] = ["start"]):
    if c == "end":
        return 1
    p = 0
    for e in g[c]:
        if e in s:
            continue
        sc = [_ for _ in s]
        if e.islower():
            sc.append(e)
        p += paths(g, e, sc)
    return p

data = read(file)
g = connections(data)

print("Dec 12, part 1: {}".format(paths(g)))
