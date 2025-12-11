def part1(file: str):
    adj = {}
    with open(file, "r") as f:
        for line in f.readlines():
            src, *dst = line.strip().split(" ")
            adj[src[:-1]] = dst

    mem = {}

    def ways(device):
        if device in mem:
            return mem[device]
        match device:
            case "out":
                n = 1
            case _ if device not in adj:
                n = 0
            case _:
                n = sum(ways(dst) for dst in adj[device])
        mem[device] = n
        return n

    return ways("you")


def part2(file: str):
    adj = {}
    with open(file, "r") as f:
        for line in f.readlines():
            src, *dst = line.strip().split(" ")
            adj[src[:-1]] = dst

    mem = {}

    def ways(src, dst):
        if (n := mem.get((src, dst))) is not None:
            return n
        if src == dst:
            n = 1
        elif src not in adj:
            n = 0
        else:
            n = sum(ways(s, dst) for s in adj[src])
        mem[(src, dst)] = n
        return n

    p1 = ways("svr", "dac") * ways("dac", "fft") * ways("fft", "out")
    p2 = ways("svr", "fft") * ways("fft", "dac") * ways("dac", "out")

    return p1 + p2


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
