import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> set[tuple[str, int, int]]:
    f = open(file, "r")
    return [line for line in map(lambda x: x.strip(), f.readlines())]

def alu(instructions: list[str], input: list[int], init: dict[str, int] = None):
    c = 0
    if init is not None:
        vars = init
    else:
        vars = {k: 0 for k in ["w", "x", "y", "z"]}
    def get(char: str):
        try:
            return int(char)
        except:
            return vars[char]
    for ins in instructions:
        match ins.split():
            case ["inp", a]:
                vars[a] = input[c]
                c += 1
            case ["add", a, b]: vars[a] += get(b)
            case ["mul", a, b]: vars[a] *= get(b)
            case ["div", a, b]: vars[a] //= get(b)
            case ["mod", a, b]: vars[a] %= get(b)
            case ["eql", a, b]: vars[a] = int(vars[a] == get(b))
    return vars

def largest_valid_model_number(monad: list[str]):
    for i in range(10**14 - 1, 10**13 - 1, -1):
        n = [int(_) for _ in str(i)]
        if 0 in n:
            continue
        if alu(monad, [int(_) for _ in str(i)])["z"] == 0:
            return i

data = read(file)

print("Dec 24, part 1: {}".format(largest_valid_model_number(data)))
