numeric_positions = {
    "A": (3, 2),
    "0": (3, 1),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}

numeric_positions_rev = {v: k for k, v in numeric_positions.items()}


def keypad_numeric(current, target, acc=""):
    """
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+
    """
    if current == target:
        yield acc + "A"
    else:
        (i, j) = numeric_positions[current]
        (k, l) = numeric_positions[target]
        n = 0 if (k - i) == 0 else (k - i) // abs(k - i)
        m = 0 if (l - j) == 0 else (l - j) // abs(l - j)
        if len(acc) == 0:
            ordered = [0, 1]
        else:
            match acc[-1]:
                case "<" | ">":
                    ordered = [0, 1]
                case "v" | "^":
                    ordered = [1, 0]
        while len(ordered) > 0:
            o = ordered.pop()
            match o:
                case 0:
                    if n != 0 and not (i + n == 3 and j == 0):
                        yield from keypad_numeric(
                            numeric_positions_rev[(i + n, j)],
                            target,
                            acc + ("v" if n == 1 else "^"),
                        )
                case 1:
                    if m != 0 and not (i == 3 and j + m == 0):
                        yield from keypad_numeric(
                            numeric_positions_rev[(i, j + m)],
                            target,
                            acc + (">" if m == 1 else "<"),
                        )


directional_positions = {
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "^": (0, 1),
    "A": (0, 2),
}

directional_positions_rev = {v: k for k, v in directional_positions.items()}


def keypad_directional(current, target, acc=""):
    """
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """
    if current == target:
        yield acc + "A"
    else:
        (i, j) = directional_positions[current]
        (k, l) = directional_positions[target]
        n = 0 if (k - i) == 0 else (k - i) // abs(k - i)
        m = 0 if (l - j) == 0 else (l - j) // abs(l - j)
        if len(acc) == 0:
            ordered = [0, 1]
        else:
            match acc[-1]:
                case "<" | ">":
                    ordered = [0, 1]
                case "v" | "^":
                    ordered = [1, 0]
        while len(ordered) > 0:
            o = ordered.pop()
            match o:
                case 0:
                    if n != 0 and not (i + n == 0 and j == 0):
                        yield from keypad_directional(
                            directional_positions_rev[(i + n, j)],
                            target,
                            acc + ("v" if n == 1 else "^"),
                        )
                case 1:
                    if m != 0 and not (i == 0 and j + m == 0):
                        yield from keypad_directional(
                            directional_positions_rev[(i, j + m)],
                            target,
                            acc + (">" if m == 1 else "<"),
                        )


def push_code(keypad, code: str, current: str = "A", acc: str = ""):
    if code == "":
        yield acc
    else:
        for instructions in keypad(current, code[0]):
            yield from push_code(keypad, code[1:], code[0], acc + instructions)


def changes(seq: str) -> int:
    n = 0
    last = None
    for char in seq:
        if last == None or char != last:
            last = char
            n += 1
    return n


def part1(file: str):
    complexity = 0
    keypads = [keypad_numeric, keypad_directional, keypad_directional]
    with open(file, "r") as f:
        for line in f.readlines():
            code = line.strip()
            number = int(code[:-1])
            for keypad in keypads:
                code = min(
                    (c for c in push_code(keypad, code)),
                    key=lambda seq: (len(seq), changes(seq)),
                )
            length = len(code)
            print(f"{line.strip()}: {code} ({length})")
            complexity += length * number
    return complexity


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
