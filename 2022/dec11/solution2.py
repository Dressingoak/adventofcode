from typing import Tuple
import json

ops = {
    0: lambda x: x * 19,
    1: lambda x: x + 6,
    2: lambda x: x ** 2,
    3: lambda x: x + 3
}
mods = {
    0: 23,
    1: 19,
    2: 13,
    3: 17
}
maps = {
    0: (2, 3),
    1: (2, 0),
    2: (1, 3),
    3: (0, 1)
}

mem: dict[Tuple[int, int, int], dict[int, int]] = {}


        
def yielder(start_id: int, start_init: int):
    tests: dict[Tuple[int, int, int], int] = {}
    nexts: dict[Tuple[int, int, int], int] = {}
    inspc: dict[Tuple[int, int, int], dict] = {}

    def get_test(rem: int, id: int, init: int):
        if (rem, id, init) in nexts:
            return nexts[(rem, id, init)]
        if rem == 0:
            for other, mod in mods.items():
                tests[(0, other, init)] = init % mod
            nexts[(rem, id, init)] = id
            return id
        if rem > 0:
            next = get_test(rem - 1, id, init)
            value = tests[(rem - 1, next, init)]
            for other, mod in mods.items():
                tests[(rem, other, init)] = ops[next](value) % mod
            if tests[(rem, next, init)] == 0:
                nnext = maps[next][0]
            else:
                nnext = maps[next][1]
            nexts[(rem, id, init)] = nnext
            return nnext

    s, r, last = 0, 1, None
    while True:
        next = get_test(s, start_id, start_init)
        s += 1
        if last is not None and next < last:
            r += 1
        last = next
        yield r, next

inspections = {0: 0, 1: 0, 2: 0, 3: 0}
initial_values = {
    0: [79, 98],
    1: [54, 65, 75, 74],
    2: [79, 60, 97],
    3: [74]
}
for id, inits in initial_values.items():
    for init in inits:
        for (round, next) in yielder(id, init):
            if round > 20:
                break
            inspections[next] += 1

print(inspections)

# for k, v in tests.items():
#     print(k, v)



# def throw(rem, id, value):
#     if (rem, id, value) in mem:
#         return mem[(rem, id, value)]
#     conv = ops[id](value)
#     test = conv % mods[id]
#     next_value = ret(id, )
