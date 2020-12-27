import re
import itertools

(data_rules, data_messages) = open("input.txt").read().strip().split("\n\n")
messages = data_messages.split("\n")

rules = dict()
pattern = re.compile(r'^(?P<rule>\d+)\:\s(\"(?P<char>\w)\"|(?P<r1>\d+(\s\d+)*)(\s\|\s(?P<r2>\d+(\s\d+)*))?)$')

for rule in data_rules.split("\n"):
    m = pattern.match(rule)
    if m:
        objs = m.groupdict()
        idx = int(objs["rule"])
        if objs["char"] is not None:
            rules[idx] = objs["char"]
        else:
            r1 = [int(_) for _ in objs["r1"].split(" ")]
            if objs["r2"] is not None:
                r2 = [int(_) for _ in objs["r2"].split(" ")]
                rules[idx] = [r1, r2]
            else:
                rules[idx] = [r1]
    else:
        raise Exception("Could not match rule: '{}'".format(rule))

def recognise_language(msg, state=0, s="", outer=True):
    if isinstance(rules[state], str):
        if s + rules[state] in msg:
            return [s + rules[state]]
        else:
            return []
    else:
        paths = rules[state]
        p = set()
        for path in paths:
            _p = set([s])
            for _state in path:
                _p_new = set()
                for _s in _p:
                    _p_new.update(set(recognise_language(msg, _state, _s, False)))
                _p = _p_new
            p.update(_p)
        if outer:
            return len([_ for _ in p if _ == msg]) == 1
        else:
            return list(p)

print("Part 1: {}".format(sum(1 if recognise_language(message) else 0 for message in messages)))

rules[8] = [[42], [42, 8]]
rules[11] = [[42, 31], [42, 11, 31]]

print("Part 2: {}".format(sum(1 if recognise_language(message) else 0 for message in messages)))
