def find(node, states, connections):
    if node in states:
        return states[node]
    else:
        a, b, op = connections[node]
        a = find(a, states, connections)
        b = find(b, states, connections)
        match op:
            case "AND":
                c = a and b
            case "OR":
                c = a or b
            case "XOR":
                c = a ^ b
        states[node] = c
        return c


def part1(file: str):
    states = {}
    connections = {}
    with open(file, "r") as f:
        parse_connections = False
        for line in f.readlines():
            if (line := line.strip()) == "":
                parse_connections = True
                continue
            if not parse_connections:
                a, v = line.split(": ")
                states[a] = bool(int(v))
            else:
                a, op, b, _, c = line.split(" ")
                connections[c] = (a, b, op)
    bit = 0
    bits = 0
    while (node := f"z{bit:02}") in connections:
        z = find(node, states, connections)
        bits += z << bit
        bit += 1
    return bits


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
