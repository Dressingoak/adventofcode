from typing import TypeVar
import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def cut_range(r1: tuple[int, int], r2: tuple[int, int]):
    # print(r1, r2)
    match r1, r2:
        case (r1a, r1b), (r2a, r2b) if r2b <= r1a:
            # print("Case 1")
            d = {(r1a, r1b): True}
        case (r1a, r1b), (r2a, r2b) if r2a <= r1a and r1a <= r2b and r2b <= r1b:
            # print("Case 2")
            d = {(r1a, r2b): False, (r2b, r1b): True}
        case (r1a, r1b), (r2a, r2b) if r2a <= r1a and r1b <= r2b:
            # print("Case 3")
            d = {(r1a, r1b): False}
        case (r1a, r1b), (r2a, r2b) if r1a <= r2a and r2b <= r1b:
            # print("Case 4")
            d = {(r1a, r2a): True, (r2a, r2b): False, (r2b, r1b): True}
        case (r1a, r1b), (r2a, r2b) if r1a <= r2a and r2a <= r1b and r1b <= r2b:
            # print("Case 5")
            d = {(r1a, r2a): True, (r2a, r1b): False}
        case (r1a, r1b), (r2a, r2b) if r1b <= r2a:
            # print("Case 6")
            d = {(r1a, r1b): True}
        case _:
            raise Exception(f"Uncaught case: {r1}, {r2}")
    # print(d)
    return {(ra, rb): safe for (ra, rb), safe in d.items() if ra < rb}

SelfBox = TypeVar("SelfBox", bound="Box")
class Box:
    def __init__(self, x: tuple[int, int], y: tuple[int, int], z: tuple[int, int]) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Box<{self.x}, {self.y}, {self.z}>"

    def reduce_boxes(boxes: list[SelfBox]) -> list[SelfBox]:
        # print(len(boxes))
        for i in range(len(boxes)):
            for j in range(0, i):
                m = boxes[i].merge(boxes[j])
                if len(m) == 1:
                    return Box.reduce_boxes([b for (k, b) in enumerate(boxes) if k != i and k != j] + m)
        return boxes

    def cut(self, other: SelfBox) -> list[SelfBox]:
        xc = cut_range(self.x, other.x)
        if all(xc.values()):
            return [Box(self.x, self.y, self.z)]
        yc = cut_range(self.y, other.y)
        if all(yc.values()):
            return [Box(self.x, self.y, self.z)]
        zc = cut_range(self.z, other.z)
        if all(zc.values()):
            return [Box(self.x, self.y, self.z)]
        boxes = []
        for x, xs in xc.items():
            for y, ys in yc.items():
                for z, zs in zc.items():
                    if xs or ys or zs:
                        boxes.append(Box(x, y, z))
        return Box.reduce_boxes(boxes)

    def merge(self, other):
        match self.x, other.x, self.y, other.y, self.z, other.z:
            case (xl1, xl2), (xr1, xr2), yl, yr, zl, zr if xl2 == xr1 and yl == yr and zl == zr:
                return [Box((xl1, xr2), yl, zl)]
            case (xl1, xl2), (xr1, xr2), yl, yr, zl, zr if xl1 == xr2 and yl == yr and zl == zr:
                return [Box((xr1, xl2), yl, zl)]
            case xl, xr, (yl1, yl2), (yr1, yr2), zl, zr if xl == xr and yl2 == yr1 and zl == zr:
                return [Box(xl, (yl1, yr2), zl)]
            case xl, xr, (yl1, yl2), (yr1, yr2), zl, zr if xl == xr and yl1 == yr2 and zl == zr:
                return [Box(xl, (yr1, yl2), zl)]
            case xl, xr, yl, yr, (zl1, zl2), (zr1, zr2) if xl == xr and yl == yr and zl2 == zr1:
                return [Box(xl, yl, (zl1, zr2))]
            case xl, xr, yl, yr, (zl1, zl2), (zr1, zr2) if xl == xr and yl == yr and zl1 == zr2:
                return [Box(xl, yl, (zr1, zl2))]
            case xl, xr, yl, yr, zl, zr:
                return [Box(xl, yl, zl), Box(xr, yr, zr)]
    
    def volume(self):
        return len(range(*self.x)) * len(range(*self.y)) * len(range(*self.z))


def read(file: str) -> list[tuple[str, Box]]:
    r = re.compile('(on|off) x=(-*\d+)\.\.(-*\d+),y=(-*\d+)\.\.(-*\d+),z=(-*\d+)\.\.(-*\d+)')
    f = open(file, "r")
    instructions = []
    for line in map(lambda x: x.strip(), f.readlines()):
        m = r.match(line)
        state = m.group(1)
        x1, x2, y1, y2, z1, z2 = tuple(map(lambda x: int(x), list(m.group(2,3,4,5,6,7))))
        instructions.append((state, Box((x1, x2 + 1), (y1, y2 + 1), (z1, z2 + 1))))
    return instructions

def reboot(instructions: list[tuple[str, Box]]):
    boxes = []
    for i, (state, box) in enumerate(instructions):
        boxes = [b for cuts in [other.cut(box) for other in boxes] for b in cuts]
        # print(i, len(boxes))
        if state == "on":
            boxes.append(box)
    return boxes

def reboot_initialization(cube: Box, boxes: list[Box]):
    rr = reboot([("on", cube)] + [("off", y) for y in boxes])
    return cube.volume() - sum(b.volume() for b in rr)

data = read(file)
r = reboot(data)

print("Dec 22, part 1: {}".format(reboot_initialization(Box((-50, 51), (-50, 51), (-50, 51)), r)))
print("Dec 22, part 2: {}".format(sum(b.volume() for b in r)))
