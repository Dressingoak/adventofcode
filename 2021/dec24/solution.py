import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[str]:
    f = open(file, "r")
    return [line for line in map(lambda x: x.strip(), f.readlines())]

def monad_split(data: list[str]) -> list[list[str]]:
    subroutines = []
    r = -1
    for ins in data:
        if ins.split()[0] == "inp":
            r += 1
            subroutines.append([])
        subroutines[r].append(ins)
    return subroutines

def monad_extract(data: list[str]) -> tuple[int, int]:
    '''
    The MONAD has the special structure where either of two cases can happen.

    Case 1:
        Simplifying the ALU:
            z_new = (((((z % 26) + a) == w) == 0) * 25 + 1) * z + (w + b) * ((((z % 26) + a) == w) == 0)
        where a > 9, meaning that this reduces to:
            z_new = 26 * z + w + b
    Case 2:
        Simplifying the ALU:
            z_new = (z // 26) * (((((z % 26) + c) == w) == 0) * 25 + 1) + (w + d) * ((((z % 26) + c) == w) == 0)
        where c <= 0. This results in two cases:
            z_new = (z // 26) * 26 + w + d if (z % 26) + c != 0

            z_new = (z // 26) if (z % 26) + c != 0
        The latter case means that z will (potentially) be reduced, and can eventually reach 0.
    There are 7 Case 1 and 7 Case 2, so a Case 1 (i) followed by a Case 2 (j) implies the condition:
        w_j = w_i + b_i + c_j <=> w_i - w_j = -(b_i + c_j),
    i.e. a restriction on the difference between the digits coming from the cancelling cases.
    '''
    c = None
    v = None
    for ins in data:
        match ins.split():
            case ["div", "z", "1"]: c = 0
            case ["add", "y", a] if c == 0:
                try:
                    v = int(a)
                except:
                    continue
            case ["div", "z", "26"]: c = 1
            case ["add", "x", a] if c == 1:
                try:
                    v = int(a)
                except:
                    continue
    return c, v

def monad_conditions(data: list[str]):
    j = -1
    stack = []
    conditions = dict()
    for i, subroutine in enumerate(monad_split(data)):
        c, v = monad_extract(subroutine)
        if c == 0:
            stack.append(i)
            conditions[i] = v
        else:
            j = stack.pop()
            conditions[j] = (i, -(conditions[j] + v))
    return [(i, j, d) for i, (j, d) in conditions.items()]

def optimize_monad_conditions(conditions: list[tuple[int, int, int]], func) -> int:
    digits = []
    for i, j, d in conditions:
        wi = func(d)
        digits.append((i, wi))
        wj = wi - d
        digits.append((j, wj))
    return sum(d * 10**i for i, (_, d) in enumerate(reversed(sorted(digits))))

data = read(file)
conditions = monad_conditions(data)

print("Dec 24, part 1: {}".format(optimize_monad_conditions(conditions, lambda d: max(v for v in range(d + 1, d + 10) if v >= 1 and v < 10))))
print("Dec 24, part 2: {}".format(optimize_monad_conditions(conditions, lambda d: min(v for v in range(d + 1, d + 10) if v >= 1 and v < 10))))
