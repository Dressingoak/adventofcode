from math import prod

data = open("input.txt").read().strip().split("\n")

schedule = {i: int(bus) for (i, bus) in enumerate(data[1].split(",")) if bus != "x"}

print("[DEBUG] Looking at bus schedule {}".format(schedule))

crt = {v: (v-k) % v for (k, v) in schedule.items()}

print("[DEBUG] Transforming to system of congruence equations:")
for (n, a) in crt.items():
    print("  x ≣ {} (mod {})".format(a, n))

def inverse(a, n):
    t = 0
    r = n
    newt = 1
    newr = a

    while newr != 0:
        quotient = r // newr
        (t, newt) = (newt, t - quotient * newt) 
        (r, newr) = (newr, r - quotient * newr)

    if r > 1:
        raise Exception("{} is not invertible".format(a))
    if t < 0:
        t = t + n

    return t

def solve_congruence_system(system):
    N = prod([_ for _ in system.keys()])
    y = [N // n for n in system.keys()]
    z = [inverse(yi, ni) for (yi, ni) in zip(y, system.keys())]
    return sum(ai*yi*zi for (ai, yi, zi) in zip(system.values(), y, z)) % N

print("Part 2: {}".format(solve_congruence_system(crt)))
