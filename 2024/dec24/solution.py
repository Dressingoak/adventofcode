def parse(file: str):
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
    return states, connections


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


def simulate(states, connections):
    bit = 0
    bits = 0
    while (node := f"z{bit:02}") in connections:
        z = find(node, states, connections)
        bits += z << bit
        bit += 1
    return bits


def part1(file: str):
    states, connections = parse(file)
    return simulate(states, connections)


def gate_equals(gate, a, b, op):
    match a, b:
        case None, None:
            return gate[2] == op
        case (x, None) | (None, x):
            return (gate[0], gate[2]) == (x, op)
        case _:
            return gate == (a, b, op) or gate == (b, a, op)


def find_node_for_gate(l, r, op, connections):
    for k, v in connections.items():
        if gate_equals(v, l, r, op):
            yield k


def find_gate_for_node(node, connections):
    return connections[node]


def part2(file: str):
    _, connections = parse(file)
    swapped = []
    a, b, c, s = [], [], [], []  # inputs (a, b), carry (c) and sum (s)
    i_xor, i_and, i_c = [], [], []  # internal gates
    bit = 0
    # {'z00': ('y00', 'x00', 'XOR')}
    # {'z01': ('rjr', 'sgt', 'XOR'), 'rjr': ('y00', 'x00', 'AND'), 'sgt': ('x01', 'y01', 'XOR')}
    # {'z02': ('fkm', 'hvb', 'XOR'), 'fkm': ('hqg', 'cff', 'OR'), 'hqg': ('x01', 'y01', 'AND'), 'cff': ('rjr', 'sgt', 'AND'), 'rjr': ('y00', 'x00', 'AND'), 'sgt': ('x01', 'y01', 'XOR'), 'hvb': ('y02', 'x02', 'XOR')}
    while (z := f"z{bit:02}") in connections:
        x = f"x{bit:02}"
        y = f"y{bit:02}"
        print(x, y, z)
        a.append(x)
        b.append(y)
        if bit == 0:  # Half adder
            node = next(find_node_for_gate(x, y, "XOR", connections))
            if node != z:
                print(f"Swapped {node} and {z}")
                swapped.extend([node, z])
                connections[z], connections[node] = connections[node], connections[z]
            s.append(z)
            c.append(next(find_node_for_gate(x, y, "AND", connections)))
        if bit > 0:  # Full adder
            n_xor = next(find_node_for_gate(x, y, "XOR", connections))
            for n in find_node_for_gate(None, c[-1], "XOR", connections):
                print(f"... {n}: {connections[n]}")
            node = next(find_node_for_gate(n_xor, c[-1], "XOR", connections))
            if node != z:
                print(f"Swapped {node} and {z}")
                swapped.extend([node, z])
                connections[z], connections[node] = connections[node], connections[z]
            n_and = next(find_node_for_gate(x, y, "AND", connections))
            n_c = next(find_node_for_gate(n_xor, c[-1], "AND", connections))
            node = next(find_node_for_gate(n_c, n_and, "OR", connections))
            s.append(z)
            c.append(node)
            i_and.append(n_and)
            i_xor.append(i_xor)
            i_c.append(node)

        bit += 1
        # print(a, b, c, s)
        # if bit > 2:
        #     break
    return 0


if __name__ == "__main__":
    print(f"{part1('test2.txt')=}")
    print(f"{part2('input.txt')=}")
