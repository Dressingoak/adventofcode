import re
data = open("input.txt").read().strip().split("\n")

values = {}
mask = ""

def format_36bit(number):
    return "{:0>36s}".format(bin(number)[2:])

def get_masked_combs(masked_string):
    cmbs = len([_ for _ in masked_string if _ == "X"])
    vals = []
    for i in range(2**cmbs):
        chars = tuple(_ for _ in ("{" + ":0>{}s".format(cmbs) + "}").format(bin(i)[2:]))
        vals.append(masked_string.replace("X", "{}").format(*chars))
    return vals

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
        bit_repr = format_36bit(address)
        masked_address = "".join(v if m =="0" else m for (m, v) in zip(mask, bit_repr))
        address_options = get_masked_combs(masked_address)
        # print("[DEBUG]        Address is {} ({}) and value is {}".format(bit_repr, address, value))
        # print("[DEBUG] Masked address is {}, resulting in possibilities:".format(masked_address))
        for _ in address_options:
            values[int(_, 2)] = value
            # print("[DEBUG] -> {} ({})".format(_, int(_, 2)))
        # print("[DEBUG] Masked value is {} ({})".format(masked_value, int(masked_value, 2)))
    else:
        raise Exception("Cannot infer line: {}".format(cmd))

print("Part 2: {}".format(sum(_ for _ in values.values())))
