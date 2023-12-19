def parse_workflows(f):
    workflows = {}
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
    return workflows


def part1(file: str):
    total = 0
    with open(file, "r") as f:
        workflows = parse_workflows(f)
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


def part2(file: str):
    with open(file, "r") as f:
        workflows = parse_workflows(f)

    def evaluate(goto, part, i):
        if goto == "A":
            ways = 1
            for v in part.values():
                ways *= v[1] - v[0]
            return ways
        elif goto == "R":
            return 0
        else:
            match workflows[goto][i]:
                case (cat, "<", value, nxt):
                    if part[cat][1] <= value:
                        return evaluate(nxt, part, 0)
                    elif part[cat][0] > value:
                        return evaluate(goto, part, i + 1)
                    else:
                        return evaluate(
                            goto, {**part, cat: (value, part[cat][1])}, i + 1
                        ) + evaluate(
                            nxt, {**part, cat: (part[cat][0], value)}, 0
                        )
                case (cat, ">", value, nxt):
                    if part[cat][0] > value:
                        return evaluate(nxt, part, 0)
                    elif part[cat][1] <= value:
                        return evaluate(goto, part, i + 1)
                    else:
                        return evaluate(
                            nxt, {**part, cat: (value + 1, part[cat][1])}, 0
                        ) + evaluate(
                            goto, {**part, cat: (part[cat][0], value + 1)}, i + 1
                        )
                case nxt:
                    return evaluate(nxt, part, 0)
    return evaluate("in", {k: (1, 4001) for k in ["x", "m", "a", "s"]}, 0)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
