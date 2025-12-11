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


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
