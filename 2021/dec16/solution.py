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
        data = []
        while r:
            data += bits[i + 1:i + 5]
            r = bits[i]
            i += 5
        return i - c, version, binary_to_int(data, 0, len(data))
    else:
        length_type = bits[c + 6]
        i = c + 7
        values = []
        if not length_type: # length type ID: 0
            size = binary_to_int(bits, i, i + 15)
            i += 15
            acc = 0
            while acc < size:
                s, v, e = decode(bits, i)
                acc += s
                version += v
                i += s
                values.append(e)
        else: # length type ID: 1
            count = binary_to_int(bits, i, i + 11)
            i += 11
            for _ in range(count):
                s, v, e = decode(bits, i)
                version += v
                i += s
                values.append(e)
        match type:
            case 0: eval = sum(values)
            case 1:
                eval = 1
                for value in values:
                    eval *= value
            case 2: eval = min(values)
            case 3: eval = max(values)
            case 5: eval = int(values[0] > values[1])
            case 6: eval = int(values[0] < values[1])
            case 7: eval = int(values[0] == values[1])
        return i - c, version, eval

def compute_version_sum(bits: list[bool]) -> int:
    _, s, _ = decode(bits, 0)
    return s

def compute_evaluation(bits: list[bool]) -> int:
    _, _, e = decode(bits, 0)
    return e

data = read(file)

print("Dec 16, part 1: {}".format(compute_version_sum(data)))
print("Dec 16, part 2: {}".format(compute_evaluation(data)))
