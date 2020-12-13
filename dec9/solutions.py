import re

data = list(map(lambda x: int(x), open("input.txt").read().strip().split("\n")))
# data = [
#     35,
#     20,
#     15,
#     25,
#     47,
#     40,
#     62,
#     55,
#     65,
#     95,
#     102,
#     117,
#     150,
#     182,
#     127,
#     219,
#     299,
#     277,
#     309,
#     576
# ]

def find_first_error(preamble_length, numbers):
    i = preamble_length
    while (i < len(numbers)):
        match = False
        for j in range(i - preamble_length, i):
            for k in range(j + 1, i):
                if numbers[j] + numbers[k] == numbers[i]:
                    match = True
                if match:
                    break
            if match:
                break
        if not match:
            return numbers[i]
        else:
            match = False
            i += 1
    raise Exception("Could not find invalid number.")

invalid_number = find_first_error(25, data)

print("Part 1: {}".format(invalid_number))

def find_contiguous_set(total, numbers):
    for i in range(len(numbers)):
        j = i + 1
        t = 0
        s = set([numbers[i]])
        while t < total:
            s.add(numbers[j])
            t = sum(s)
            if t == total:
                return s
            j += 1
    raise Exception("Could not find contiguous set.")

contiguous_set = find_contiguous_set(invalid_number, data)

print("Part 2: {}".format(min(contiguous_set) + max(contiguous_set)))
