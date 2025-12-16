def press(current: str, buttons: list[int]):
    return "".join(
        x if i not in buttons else ("." if x == "#" else "#")
        for i, x in enumerate(current)
    )


def part1(file: str):
    total = 0
    light_goals = []
    button_rules = []
    with open(file, "r") as f:
        for line in f.readlines():
            light, *rest = line.strip().split(" ")
            light_goals.append(light[1:-1])
            button_rules.append(
                [[int(_) for _ in b[1:-1].split(",")] for b in rest[:-1]]
            )
    for goal, all_buttons in zip(light_goals, button_rules):

        def find_shortest(current: str, buttons: list[int]):
            if current == goal:
                return 0
            if len(buttons) == 0:
                return None

            pressed = press(current, buttons[-1])
            a = find_shortest(current, buttons[:-1])
            b = find_shortest(pressed, buttons[:-1])
            match a, b:
                case None, None:
                    return None
                case x, None:
                    return x
                case None, y:
                    return y + 1
                case x, y:
                    return min(x, y + 1)

        total += find_shortest("." * len(goal), all_buttons)
    return total


def part2(file: str):
    import numpy as np
    from scipy import optimize

    total = 0
    button_rules = []
    joltage_requirements = []
    with open(file, "r") as f:
        for line in f.readlines():
            _, *rest = line.strip().split(" ")
            button_rules.append(
                [[int(_) for _ in b[1:-1].split(",")] for b in rest[:-1]]
            )
            joltage_requirements.append(
                tuple(int(_) for _ in rest[-1][1:-1].split(","))
            )
    for buttons, joltages in zip(button_rules, joltage_requirements):
        A = [[0 for _ in range(len(buttons))] for _ in range(len(joltages))]
        for j, b in enumerate(buttons):
            for i in range(len(joltages)):
                if i in b:
                    A[i][j] = 1
        A = np.array(A, dtype=np.int32)
        c = np.ones(len(buttons), dtype=np.int32)
        b = np.array(joltages, dtype=np.int32)

        total += int(
            optimize.linprog(c=c, A_eq=A, b_eq=b, integrality=1)
            .x.sum()
            .astype(np.int32)
        )

    return total


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
