import re
data = open("input.txt").read().strip().split("\n")

values = {}
mask = ""

def format_36bit(number):
    return "{:0>36s}".format(bin(number)[2:])

for cmd in data:
    m = re.match(r'^mask \= ([X0-1]{36})$', cmd)
    if m:
        mask = m.group(1)
        # print("[DEBUG] Mask is now {}".format(mask))
        continue
    m = re.match(r'^mem\[(\d+)\] \= (\d+)$', cmd)
    if m:
        address = int(m.group(1))
        value = int(m.group(2))
        bit_repr = format_36bit(value)
        masked_value = "".join(v if m =="X" else m for (m, v) in zip(mask, bit_repr))
        values[address] = int(masked_value, 2)
        # print("[DEBUG] Address is {} and value is {} ({})".format(address, bit_repr, value))
        # print("[DEBUG] Masked value is {} ({})".format(masked_value, int(masked_value, 2)))
    else:
        raise Exception("Cannot infer line: {}".format(cmd))

print("Part 1: {}".format(sum(_ for _ in values.values())))
