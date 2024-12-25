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


def part1(file: str):
    states, connections = parse(file)
    bit = 0
    bits = 0
    while (node := f"z{bit:02}") in connections:
        z = find(node, states, connections)
        bits += z << bit
        bit += 1
    return bits


def find_node(connections, a, b, op):
    for k, v in connections.items():
        if v == (a, b, op) or v == (b, a, op):
            return k


def iter_nodes(connections, a, b, op):
    for k, v in connections.items():
        match a, b, op:
            case (None, None, _):
                if v[2] == op:
                    yield k, v
            case (_, None, _):
                if (v[0] == a or v[1] == a) and v[2] == op:
                    yield k, v
            case (None, _, _):
                if (v[0] == b or v[1] == b) and v[2] == op:
                    yield k, v
            case (_, _, _):
                if v == (a, b, op) or v == (b, a, op):
                    yield k, v


def swap(connections, swapped, n1, n2):
    # print(f"Swapping {n1} and {n2}")
    connections[n1], connections[n2] = connections[n2], connections[n1]
    swapped.extend([n1, n2])


def part2(file: str):
    _, connections = parse(file)
    s, c, e, f, g = [], [], [], [], []
    swapped = []
    bit = 0
    while (z := f"z{bit:02}") in connections:
        x = f"x{bit:02}"
        y = f"y{bit:02}"
        if bit == 0:
            _z = find_node(connections, x, y, "XOR")
            if _z != z:
                swap(connections, swapped, z, _z)
            s.append(z)
            c.append(None)
            e.append(None)
        elif bit == 1:
            _e = find_node(connections, x, y, "XOR")
            _c = find_node(connections, "x00", "y00", "AND")
            _z = find_node(connections, _e, _c, "XOR")
            if _z is None:
                raise NotImplementedError
            c.append(_c)
            e.append(_e)
            if _z != z:
                swap(connections, swapped, z, _z)
            s.append(z)
            f.append(None)
            g.append(None)
        else:
            xp = f"x{(bit-1):02}"
            yp = f"y{(bit-1):02}"
            _f = find_node(connections, e[-1], c[-1], "AND")
            _g = find_node(connections, xp, yp, "AND")
            # print(f"Trying to find c_{bit} as f_{bit-1} or g_{bit-1}: '{_f} OR {_g}'")
            _c = find_node(connections, _f, _g, "OR")
            if _c is None:
                raise NotImplementedError
            f.append(_f)
            g.append(_g)
            _e = find_node(connections, x, y, "XOR")
            if _e is None:
                break
            _z = find_node(connections, _e, _c, "XOR")
            if _z is None:
                options = [
                    (a if a != _e else b)
                    for (_, (a, b, _)) in iter_nodes(connections, _e, None, "XOR")
                ]
                if len(options) > 0:
                    swap(connections, swapped, _c, options[0])
                else:
                    options = [
                        (a if a != _c else b)
                        for (_, (a, b, _)) in iter_nodes(connections, _c, None, "XOR")
                    ]
                    swap(connections, swapped, _e, options[0])
                _c = find_node(connections, _f, _g, "OR")
                _e = find_node(connections, x, y, "XOR")
                _z = find_node(connections, _e, _c, "XOR")
            c.append(_c)
            e.append(_e)
            if _z != z:
                swap(connections, swapped, z, _z)
            s.append(z)
        # print(s, c, e, f, g)
        bit += 1
    return ",".join(sorted(swapped))


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
