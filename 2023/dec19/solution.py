def part1(file: str):
    total = 0
    workflows = {}
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                break
            name, wf = line.split("{")
            rules = wf[:-1].split(",")
            parsed = []
            for section in rules:
                match section.split(":"):
                    case [r, dst]:
                        parsed.append((r[0], r[1], int(r[2:]), dst))
                    case [dst]:
                        parsed.append(dst)
            workflows[name] = parsed
        for line in f:
            part = {
                (y := x.split("="))[0]: int(y[1])
                for x in line.strip().strip("{}").split(",")
            }
            goto = "in"
            while goto != "A" and goto != "R":
                for rule in workflows[goto]:
                    match rule:
                        case (cat, "<", value, nxt) if part[cat] < value:
                            goto = nxt
                            break
                        case (cat, "<", value, nxt):
                            continue
                        case (cat, ">", value, nxt) if part[cat] > value:
                            goto = nxt
                            break
                        case (cat, ">", value, nxt):
                            continue
                        case nxt:
                            goto = nxt
            if goto == "A":
                total += sum(_ for _ in part.values())
    return total


def evaluate(workflows, goto, part, i):
    if goto == "A":
        ways = 1
        for v in part.values():
            ways *= v[1] - v[0]
        yield ways
    elif goto == "R":
        pass
    else:
        match workflows[goto][i]:
            case (cat, "<", value, nxt):
                if part[cat][1] <= value:
                    yield (nxt, part, 0)
                elif part[cat][0] > value:
                    yield (goto, part, i + 1)
                else:
                    yield (goto, {**part, cat: (value, part[cat][1])}, i + 1)
                    yield (nxt, {**part, cat: (part[cat][0], value)}, 0)
            case (cat, ">", value, nxt):
                if part[cat][0] > value:
                    yield (nxt, part, 0)
                elif part[cat][1] <= value:
                    yield (goto, part, i + 1)
                else:
                    yield (nxt, {**part, cat: (value + 1, part[cat][1])}, 0)
                    yield (goto, {**part, cat: (part[cat][0], value + 1)}, i + 1)
            case nxt:
                yield (nxt, part, 0)


def part2(file: str):
    total = 0
    workflows = {}
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                break
            name, wf = line.split("{")
            rules = wf[:-1].split(",")
            parsed = []
            for section in rules:
                match section.split(":"):
                    case [r, dst]:
                        parsed.append((r[0], r[1], int(r[2:]), dst))
                    case [dst]:
                        parsed.append(dst)
            workflows[name] = parsed
    stack = [("in", {k: (1, 4001) for k in ["x", "m", "a", "s"]}, 0)]
    while len(stack) > 0:
        goto, part, i = stack.pop()
        for ret in evaluate(workflows, goto, part, i):
            match ret:
                case s if isinstance(s, int):
                    total += s
                case triple:
                    stack.append(triple)
    return total


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
