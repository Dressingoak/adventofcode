adapters = sorted(list(map(lambda x: int(x), open("input.txt").read().strip().split("\n"))))
# adapters = sorted([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])
# adapters = sorted([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3])

dist = {
    1: adapters[0], 
    3: 1 # Own device
}

for i in range(1, len(adapters)):
    diff = adapters[i] - adapters[i-1]
    if diff in dist:
        dist[diff] += 1
    else:
        raise Exception("Jontage difference not allowed (got {})".format(diff))

print("Part 1: {}".format(dist[1] * dist[3]))

def get_distinct_arrangements(adp, idx = 0):
    # print(adp)
    arrangements = 1
    for i in range(idx + 1, len(adp)-1):
        if adp[i+1] - adp[i-1] <= 3:
            arrangements += get_distinct_arrangements(adp[:i] + adp[(i+1):], i-1)
    return arrangements

def split_list(adp):
    for i in range(1, len(adp)):
        if adp[i] - adp[i-1] == 3:
            return [adp[:i]] + split_list(adp[i:])
    return [adp]

def get_distinct_arrangements_v2(adp, idx = 0):
    acc = 1
    for lst in split_list(adp):
        acc *= get_distinct_arrangements(lst, 0)
    return acc

print("Part 2: {}".format(get_distinct_arrangements_v2([0] + adapters)))
