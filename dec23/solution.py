from collections import deque
from progress.bar import Bar
import logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

class CrabCups:

    logger = logging.getLogger('CrabCups')

    def __init__(self, labeling, extended=None):
        self.labeling = deque([int(_) for _ in str(labeling)])
        self.moves = 0
        self.lowest = min(self.labeling)
        highest = max(self.labeling)
        if extended is not None:
            self.labeling.extend(range(highest+1, extended + 1))
            self.highest = max(highest, extended)
        else:
            self.highest = highest
        self.count = len(self.labeling)
        self.current = self.labeling[0]

    def __str__(self):
        return "".join(["({})".format(_) if _ == self.current else " {} ".format(_) for _ in self.labeling])

    def get_label(self):
        self.rotate_to(1)
        return "".join([str(_) for _ in list(self.labeling)[1:]])

    def get_star_positions(self):
        self.rotate_to(1)
        return (self.labeling[1], self.labeling[2])

    def rotate_to(self, value, offset=0):
        idx = self.labeling.index(value) + offset
        self.labeling.rotate(-idx)

    def move(self):
        self.moves += 1
        self.logger.info("-- move {} --".format(self.moves))
        self.logger.debug("cups: {}".format(self))
        self.rotate_to(self.current, 1)
        picked = deque([self.labeling.popleft() for _ in range(3)])
        destination = None
        tmp = self.current
        while destination is None:
            tmp -= 1
            tmp = (tmp - self.lowest) % self.count + self.lowest
            if tmp in self.labeling:
                destination = tmp
        self.logger.debug("pick up: {}".format(", ".join([str(_) for _ in picked])))
        self.logger.debug("destination: {}".format(destination))
        self.rotate_to(destination, 1)
        picked.extend(self.labeling)
        idx = (picked.index(self.current) + 1) % self.count
        self.current = picked[idx]
        self.labeling = picked
        self.logger.debug("")
        self.rotate_to(self.current, -self.moves)

# game = CrabCups("389125467")
init = "871369452"
CrabCups.logger.propagate = False
game_one = CrabCups(init)
[game_one.move() for _ in range(100)]
logging.info("Part 1: {}".format(game_one.get_label()))

CrabCups.logger.propagate = True
game_two = CrabCups(init, 30)

[game_two.move() for _ in range(10)]
# step = 100
# steps = 10_000_000
# class ShufflingBar(Bar):
#     message = "Shuffling"
#     suffix = "%(percent).1f%% (ETA: %(remaining_fmt)s, elapsed: %(elapsed_fmt)s)"
#     @property
#     def remaining_fmt(self):
#         days = self.eta // (60 * 60 * 24)
#         hours = (self.eta // (60 * 60)) % 24
#         minutes = (self.eta // 60) % 60
#         seconds = self.eta % 60
#         return "{}d {}h {}m {}s".format(days, hours, minutes, seconds)
#     @property
#     def elapsed_fmt(self):
#         days = self.elapsed // (60 * 60 * 24)
#         hours = (self.elapsed // (60 * 60)) % 24
#         minutes = (self.elapsed // 60) % 60
#         seconds = self.elapsed % 60
#         return "{}d {}h {}m {}s".format(days, hours, minutes, seconds)
# with ShufflingBar("Shuffling", max=steps//step) as bar:
#     for i in range(steps):
#         game_two.move()
#         if i % step == 0:
#             bar.next()
#     bar.finish()
(pos1, pos2) = game_two.get_star_positions()
logging.info("Part 2: {} (= {} * {})".format(pos1*pos2, pos1, pos2))
