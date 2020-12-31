from collections import deque
import logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

class CrabCups:

    logger = logging.getLogger('CrabCups')

    def __init__(self, labeling):
        self.labeling = deque([int(_) for _ in str(labeling)])
        self.moves = 0
        self.lowest = min(self.labeling)
        self.count = len(self.labeling)
        self.current = self.labeling[0]

    def __str__(self):
        return "".join(["({})".format(_) if _ == self.current else " {} ".format(_) for _ in self.labeling])

    def get_label(self):
        self.rotate_to(1)
        return "".join([str(_) for _ in list(self.labeling)[1:]])

    def rotate_to(self, value, offset=0):
        idx = self.labeling.index(value) + offset
        self.labeling.rotate(-idx)

    def move(self):
        self.moves += 1
        self.logger.debug("-- move {} --".format(self.moves))
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
game = CrabCups("871369452")
[game.move() for _ in range(100)]
logging.info("Part 1: {}".format(game.get_label()))
