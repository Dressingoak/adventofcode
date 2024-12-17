def parse(file: str):
    parse_registers = True
    registers = {}
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                parse_registers = False
                continue
            if parse_registers:
                _, r, v = line.split()
                registers[r[:-1]] = int(v)
            else:
                _, p = line.split()
                program = [int(_) for _ in p.split(",")]
                return registers, program


def combo(registers, v):
    match v:
        case 0 | 1 | 2 | 3:
            return v
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case _:
            raise RuntimeError


def calculate(registers: dict[str, int], program: list[int]):
    p = 0  # pointer
    out = []
    while True:
        try:
            nxt = p + 2
            match opcode := program[p]:
                case 0 | 6 | 7:  # adv, bdv, cdv
                    registers["A" if opcode == 0 else ("B" if opcode == 6 else "C")] = (
                        registers["A"] // 2 ** combo(registers, program[p + 1])
                    )
                case 1:  # bxl
                    registers["B"] = registers["B"] ^ program[p + 1]
                case 2:  # bst
                    registers["B"] = combo(registers, program[p + 1]) % 8
                case 3:  # jnz
                    if registers["A"] != 0:
                        nxt = program[p + 1]
                case 4:  # bxc
                    registers["B"] = registers["B"] ^ registers["C"]
                case 5:  # out
                    out.append(combo(registers, program[p + 1]) % 8)
                case _:
                    raise RuntimeError
            p = nxt
        except IndexError:
            break

    return out


def part1(file: str):
    registers, program = parse(file)
    out = calculate(registers, program)
    return ",".join([str(_) for _ in out])


def part2(file: str):
    _, program = parse(file)
    a = 0
    while True:
        out = calculate({"A": a, "B": 0, "C": 0}, program)
        if program == out:
            break
        a += 1
    return a


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
