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


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
