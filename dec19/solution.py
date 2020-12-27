import re
import itertools

(data_rules, data_messages) = open("input.txt").read().strip().split("\n\n")
data_rules = data_rules.split("\n")
data_messages = data_messages.split("\n")

rules = dict()

i = 0
while len(rules) < len(data_rules):
    # print("[DEBUG] Parsed rules {}/{}".format(len(rules), len(data_rules)))
    i = i % len(data_rules)
    m = re.match(r'^(\d+)\:\s(.+)$', data_rules[i])
    if m:
        rule = int(m.group(1))
        if rule in rules:
            i += 1
        else:
            mw = re.match(r'^\"(\w+)\"$', m.group(2))
            if mw:
                # print("[DEBUG] Adding rule {}: '{}'".format(rule, mw.group(1)))
                rules[rule] = set([mw.group(1)])
            else:
                mc = re.match(r'^(?P<first>[\d\s]+)(\s\|\s(?P<second>[\d\s]+))?$', m.group(2))
                if mc:
                    entries = mc.groupdict()
                    first = [int(_) for _ in entries["first"].split(" ")]
                    second = [] if entries["second"] is None else [int(_) for _ in entries["second"].split(" ")]
                    present = len(set(first).union(set(second)).difference(set(_ for _ in rules.keys()))) == 0
                    if present:
                        cmb_first = set(["".join(list(_)) for _ in itertools.product(*[rules[r] for r in first])])
                        # print("[DEBUG] For rule {} (first), values can be: {}".format(rule, sorted(list(cmb_first))))
                        if len(second) > 0:
                            cmb_second = set(["".join(list(_)) for _ in itertools.product(*[rules[r] for r in second])])
                            # print("[DEBUG] For rule {} (second), values can be: {}".format(rule, sorted(list(cmb_second))))
                            rules[rule] = cmb_first.union(cmb_second)
                        else:
                            rules[rule] = cmb_first
            i += 1
    else:
        raise Exception("Match error: {}".format(data_rules[i]))

rule0 = rules[0]
del rules
c = 0
for message in data_messages:
    if message in rule0:
        m = "MATCHED"
        c += 1
    else:
        m = "NOT MATCHED"
    # print("[DEBUG] Message '{}': {}".format(message, m))

print("Part 1: {}".format(c))
