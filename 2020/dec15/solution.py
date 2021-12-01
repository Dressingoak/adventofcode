class MemoryGame:

    def __init__(self, numbers):
        self.history = dict()
        self.turn = 0
        self.last = None

        starting_numbers = list(map(lambda x: int(x), numbers.split(",")))

        for n in starting_numbers:
            self.add_to_memory(n)
            self.last = n

    def say(self, stop):
        while self.turn < stop:
            if len(self.history[self.last]) > 1:
                diff = self.history[self.last][-1] - self.history[self.last][-2]
                # print("[DEBUG] Number {} have appeared before, its history is {}, yielding {}".format(self.last, self.history[self.last], diff))
                self.add_to_memory(diff)
                yield diff
            else:
                # print("[DEBUG] Number {} have not appeared before, yielding 0".format(self.last))
                self.add_to_memory(0)
                # print("[DEBUG] History: {}".format(self.history))
                yield 0

    def get_nth(self, n):
        last = None
        for last in self.say(n):
            pass
        return last

    def add_to_memory(self, number):
        if number in self.history:
            self.history[number].append(self.turn + 1)
        else:
            self.history[number] = [self.turn + 1]
        self.turn += 1
        self.last = number
        return

data = "1,20,11,6,12,0"

print("Part 1: {}".format(MemoryGame(data).get_nth(2020)))
print("Part 2: {}".format(MemoryGame(data).get_nth(30000000)))
