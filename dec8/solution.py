import re

instructions = open("input.txt").read().strip().split("\n")
# instructions = [
#     "nop +0",
#     "acc +1",
#     "jmp +4",
#     "acc +3",
#     "jmp -3",
#     "acc -99",
#     "acc +1",
#     "jmp -4",
#     "acc +6"
# ]

def run_program(ins):
    acc = 0
    i = 0
    visited = set()
    while (i < len(ins)):
        if i not in visited:
            visited.add(i)
        else:
            return (False, acc)
        op = ins[i]
        m1 = re.match(r'^nop [\+|\-]\d+$', op)
        if m1:
            i += 1
            continue
        m2 = re.match(r'^acc \+*(\d+|-\d+)$', op)
        if m2:
            acc += int(m2.group(1))
            i += 1
            continue
        m3 = re.match(r'^jmp \+*(\d+|-\d+)$', op)
        if m3:
            i += int(m3.group(1))
    return (True, acc)

(_, acc) = run_program(instructions)

print("Part 1: {}".format(acc))

def swap_program_instructions(ins):
    j = 0
    while (j < len(ins)):
        m = re.match(r'^(jmp|nop) ([\+|\-]\d+)$', ins[j])
        if m:
            # print("[DEBUG] Trying line {} of {}.".format(i, len(possible_bags)))
            cpy = ins.copy()
            cpy[j] = "{} {}".format("jmp" if m.group(1) == "nop" else "nop", m.group(2))
            (success, acc) = run_program(cpy)
            if success:
                return acc
            else:
                j += 1
        else:
            j += 1
    raise Exception("Could not swap instructions.")

print("Part 2: {}".format(swap_program_instructions(instructions)))
