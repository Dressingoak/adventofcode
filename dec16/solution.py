import re
import functools 

class Rule:

    def __init__(self, txt):
        m = re.match(r'^([\w\s]+)\:\s(\d+)\-(\d+)\sor\s(\d+)\-(\d+)$', txt)
        if m:
            self.descriptor = m.group(1)
            self.ranges = ([int(m.group(2)), int(m.group(3))], [int(m.group(4)), int(m.group(5))])
        else:
            raise Exception("Cannot parse rule: '{}'".format(txt))
    
    def __repr__(self):
        return "Rule<'{}', [{}, {}] U [{}, {}]>".format(self.descriptor, self.ranges[0][0], self.ranges[0][1], self.ranges[1][0], self.ranges[1][1])
    
    def isin(self, value):
        return (self.ranges[0][0] <= value and value <= self.ranges[0][1]) or (self.ranges[1][0] <= value and value <= self.ranges[1][1])

class Ticket:

    def __init__(self, values):
        self.values = list(map(lambda x: int(x), values.split(",")))

    def __repr__(self):
        return "Ticket<{}>".format(", ".join([str(_) for _ in self.values]))

    def __getitem__(self, key):
        return self.values[key]

    def get_possible_rules(self, rules):
        lst = dict()
        for i, value in enumerate(self.values):
            lst[i] = (value, [])
            for rule in rules:
                if rule.isin(value):
                    lst[i][1].append(rule.descriptor)
        return lst

# Get & parse data
(data_rules, data_my_ticket, data_nearby_tickets) = open("input.txt").read().strip().split("\n\n")
rules = list(map(lambda x: Rule(x), data_rules.split("\n")))
my_ticket = Ticket(data_my_ticket.split("\n")[1])
nearby_tickets = list(map(lambda x: Ticket(x), data_nearby_tickets.split("\n")[1:]))

invalid_tickets = {idx: [v for (k, (v, c)) in ticket.get_possible_rules(rules).items() if len(c) == 0] for (idx, ticket) in enumerate(nearby_tickets)}

ticket_scanning_error_rate = sum(sum(v) for (k, v) in invalid_tickets.items())

print("Part 1: {}".format(ticket_scanning_error_rate))

valid_tickets = {i: t.get_possible_rules(rules) for (i, t) in enumerate(nearby_tickets) if len(invalid_tickets[i]) == 0}

rules_string = set(rule.descriptor for rule in rules)
mat = {r: [] for r in rules_string}

for i, t in valid_tickets.items():
    idxs = {j: s for (j, s) in {k: rules_string.difference(set(opts)) for (k, (_, opts)) in t.items()}.items() if len(s) > 0}
    temp = {rule: [True] * len(rules_string) for rule in rules_string}
    for i, rules in idxs.items():
        for rule in rules:
            temp[rule][i] = False
    for rule in rules_string:
        mat[rule].append(temp[rule])

options = {r: functools.reduce(lambda x, y: [a & b for (a, b) in zip(x, y)], m) for (r, m) in mat.items()}
deduced = dict()
skip = []
for r, values in {v[0]: v[1] for v in sorted(options.items(), key=lambda item: item[1].count(True))}.items():
    for k, v in enumerate([False if k in skip else v for (k, v) in enumerate(values)]):
        if v == True:
            skip.append(k)
            deduced[r] = k
            break

# for (f, i) in (sorted(deduced.items(), key=lambda item: item[1])):
#     print("[DEBUG] Field {} is '{}'".format(i, f))

fields = [my_ticket[v] for (k, v) in deduced.items() if k.startswith("departure")]
print("Part 2: {}".format(functools.reduce(lambda x, y: x * y, fields)))
