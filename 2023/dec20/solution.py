def parse(file: str):
    modules = {}
    connections = {}
    with open(file, "r") as f:
        for line in f:
            src, dst = line.strip().split(" -> ")
            dst = dst.split(", ")
            match src:
                case _ if src[0] == "%":
                    modules[src[1:]] = ["%", dst, False]
                    module = src[1:]
                case _ if src[0] == "&":
                    modules[src[1:]] = ["&", dst]
                    module = src[1:]
                case "broadcaster":
                    modules[src] = dst
                    module = src
            for d in dst:
                if d not in connections:
                    connections[d] = [module]
                else:
                    connections[d].append(module)
    for module, props in modules.items():
        if props[0] == "&":
            modules[module].append({k: False for k in connections[module]})
    return modules


def press(modules):
    pulses = {False: 1, True: 0}
    handle = [("button", "broadcaster", False)]  # Treat as FIFO
    while len(handle) > 0:
        src, dst, s = handle.pop(0)  # O(n) front pop cost due to list != deque
        # print(f"{src} -{'high' if s else 'low'}-> {dst}")
        if dst in modules:
            match dst, modules[dst]:
                case "broadcaster", targets:
                    for d in targets:
                        pulses[False] += 1
                        handle.append((dst, d, False))
                case _, ["%", targets, t] if s == False:
                    modules[dst][2] = not t  # Store flip-flop state
                    t = modules[dst][2]
                    for d in targets:
                        pulses[t] += 1
                        handle.append((dst, d, t))
                case _, ["&", targets, memory]:
                    memory[src] = s  # Update conjunction memory
                    t = not all(_ for _ in memory.values())
                    for d in targets:
                        pulses[t] += 1
                        handle.append((dst, d, t))
    initial = True
    for module in modules.values():
        match module:
            case ["%", _, s] if s:
                initial = False
                break
            case ["&", _, memory] if any(_ for _ in memory.values()):
                initial = False
                break
    return initial, pulses[False], pulses[True]


def part1(file: str):
    modules = parse(file)
    cycles = []
    N = 1000
    for _ in range(N):
        initial, low, high = press(modules)
        cycles.append((low, high))
        if initial:
            break

    n = len(cycles)
    low = sum(s[0] for s in cycles) * (N // n)
    high = sum(s[1] for s in cycles) * (N // n)
    low += sum(s[0] for s in cycles[: (N % n)])
    high += sum(s[1] for s in cycles[: (N % n)])

    return low * high


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
