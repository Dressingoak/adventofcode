data = open("test.txt").read().strip().split("\n")
earliest = int(data[0])
busses = data[1].split(",") # list(map(lambda x: int(x), data[0].split(",")))

def get_earliest(timestamp, bus):
    if bus == "x":
        return None
    idnum = int(bus)
    rem = timestamp % idnum
    if rem == 0:
        return (idnum, 0)
    else:
        quo = timestamp // idnum
        return (idnum, (quo + 1) * idnum - timestamp)

bus_delays = [_ for _ in (map(lambda _: get_earliest(earliest, _), busses)) if _ is not None]
earliest_bus = min(bus_delays, key = lambda t: t[1])

print("Part 1: {}".format(earliest_bus[0] * earliest_bus[1]))

def is_subsequent(timestamp, schedule):
    lst = list((map(lambda _: get_earliest(timestamp, _), schedule)))
    for k, v in enumerate(lst):
        if v is not None and k != v[1]:
            return False
    return True

max_id = max(int(_) for _ in busses if _ != "x")
max_id_idx = busses.index(str(max_id))

ts = max_id - max_id_idx
ended = False
while not ended:
    if is_subsequent(ts, busses):
        ended = True
    else:
        ts += max_id

print("Part 2: {}".format(ts))
