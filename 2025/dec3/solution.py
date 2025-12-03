def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            joltages = [int(_) for _ in line.strip()]
            lead_max = 0
            max_joltage = 0
            for i in range(len(joltages)):
                if (d1 := joltages[i]) < lead_max:
                    continue
                lead_max = d1
                for j in range(i + 1, len(joltages)):
                    d2 = joltages[j]
                    if (joltage := d1 * 10 + d2) > max_joltage:
                        max_joltage = joltage
            sum += max_joltage
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
