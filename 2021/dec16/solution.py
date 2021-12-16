import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def hex_to_binary(input: str):
    for char in input:
        v = int(char, 16)
        for i in range(3, -1, -1):
            yield bool((v >> i) % 2)

def read(file: str) -> list[bool]:
    f = open(file, "r")
    return list(hex_to_binary(f.readline().strip()))

def binary_to_int(bits: list[bool], start: int, end: int) -> int:
    return sum(int(b) * 2**i for (i, b) in enumerate(reversed(bits[start:end])))

def decode(bits: list[bool], c: int):
    version = binary_to_int(bits, c, c + 3)
    type = binary_to_int(bits, c + 3, c + 6)
    if type == 4:
        r = True
        i = c + 6
        # data = []
        while r:
            # data += bits[i + 1:i + 5]
            r = bits[i]
            i += 5
        return i - c, version
        # return [version, type, i - c, binary_to_int(data, 0, len(data))]
    else:
        length_type = bits[c + 6]
        i = c + 7
        if not length_type: # length type ID: 0
            size = binary_to_int(bits, i, i + 15)
            i += 15
            acc = 0
            while acc < size:
                s, v = decode(bits, i)
                acc += s
                version += v
                i += s
            return i - c, version
        else: # length type ID: 1
            count = binary_to_int(bits, i, i + 11)
            i += 11
            for _ in range(count):
                s, v = decode(bits, i)
                version += v
                i += s
            return i - c, version

def compute(bits: list[bool]) -> int:
    _, s = decode(bits, 0)
    return s

data = read(file)

print("Dec 16, part 1: {}".format(compute(data)))
