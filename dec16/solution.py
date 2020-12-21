import re

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

    def get_possible_rules(self, rules):
        lst = dict()
        for value in self.values:
            lst[value] = []
            for rule in rules:
                if rule.isin(value):
                    lst[value].append(rule.descriptor)
        return lst

# Get & parse data
(data_rules, data_my_ticket, data_nearby_tickets) = open("input.txt").read().strip().split("\n\n")
rules = list(map(lambda x: Rule(x), data_rules.split("\n")))
my_ticket = Ticket(data_my_ticket.split("\n")[1])
nearby_tickets = list(map(lambda x: Ticket(x), data_nearby_tickets.split("\n")[1:]))

# for _ in rules:
#     print(_)
# print(my_ticket)
# for _ in nearby_tickets:
#     print(_)

ticket_scanning_error_rate = sum(sum(k for (k, v) in ticket.get_possible_rules(rules).items() if len(v) == 0) for ticket in nearby_tickets)

print("Part 1: {}".format(ticket_scanning_error_rate))
