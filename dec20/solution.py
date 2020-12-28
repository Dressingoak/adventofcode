import re

class Tile:

    pattern = re.compile(r'^Tile\s(\d{4})\:$')

    def __init__(self, data):
        rows = data.split("\n")
        m = self.pattern.match(rows[0])
        if m:
            self.id = m.group(1)
        else:
            raise Exception("Could not parse ID from tile data: '{}'".format(rows[0]))
        self.data = []
        for row in rows[1:]:
            self.width = len(row)
            self.data.append([True if _ == "#" else False for _ in row])
        self.height = len(self.data)

    def __str__(self):
        return "\n".join(["".join(["#" if self.data[i][j] else "." for j in range(self.width)]) for i in range(self.height)])

    def rotate(self):
        '''Rotate the image one time clockwise.'''
        data = []
        for j in range(self.width):
            data.append([self.data[i][j] for i in range(self.height - 1, -1, -1)])
        self.data = data
        (self.height, self.width) = (self.width, self.height)
        return
    
    def flip(self):
        '''Flip the image horizontally.'''
        for i in range(self.height):
            self.data[i] = [self.data[i][j] for j in range(self.width - 1, -1, -1)]
        return

    def get_border_hashes(self):
        return [
            int("".join(["1" if self.data[0][j] else "0" for j in range(self.width)]), 2), # Top
            int("".join(["1" if self.data[i][-1] else "0" for i in range(self.height)]), 2), # Right
            int("".join(["1" if self.data[-1][j] else "0" for j in range(self.width)]), 2), # Bottom
            int("".join(["1" if self.data[i][0] else "0" for i in range(self.height)]), 2) # Left
        ]

class TileBorders():

    def __init__(self, tile):
        self.id = tile.id
        self.hashes = dict()
        for f in range(2):
            for r in range(4):
                self.hashes[(f, r)] = tile.get_border_hashes()
                tile.rotate()
            tile.flip()

    def fit(self, orientation, other):
        yin = self.hashes[orientation]
        ways = []
        for perm, yang in other.hashes.items():
            if yin[0] == yang[2]:
                ways.append(("b", perm))
            if yin[1] == yang[3]:
                ways.append(("r", perm))
            if yin[2] == yang[0]:
                ways.append(("t", perm))
            if yin[3] == yang[1]:
                ways.append(("l", perm))
        return ways

tile_data = open("input.txt").read().strip().split("\n\n")

tiles = [Tile(t) for t in tile_data]
borders = [TileBorders(t) for t in tiles]

def is_square(num):
    for i in range(1, num):
        if i**2 == num:
            return i
    return False

def solve_jigsaw(remaining, current=None, size=None):
    if len(remaining) == 0:
        if len(current) != size**2:
            raise Exception("Expecting exactly {} placed tiles, found {}".format(size**2, len(current)))
        values = sorted([(position, tile) for (position, tile) in current.items()], key=lambda x: (x[0][1], x[0][0]))
        square = []
        for i in range(size):
            square.append([_[1] for _ in values[i*size:(i+1)*size]])
        return square
    if current is None:
        size = is_square(len(remaining))
        if size == False:
            raise Exception("Pieces should make up a square, got {} tiles (which is not the square of an integer).".format(len(remaining)))
        current = {(0, 0): ((0, 0), borders[0])}
        remaining = remaining[1:]
    # print("[DEBUG] Remaining tiles: {}".format(", ".join([tile.id for tile in remaining])))
    # print("[DEBUG] Placed tiles: {}".format(current))
    for (x, y), (orientation, tile) in current.items():
        look_r = max(_x for (_x,_y) in current.keys() if _y==y) - min(_x for (_x,_y) in current.keys() if _y==y) < size
        look_c = max(_y for (_x,_y) in current.keys() if _x==x) - min(_y for (_x,_y) in current.keys() if _x==x) < size
        adj_r = set([(x-1,y), (x+1,y)]) if look_r else set()
        adj_c = set([(x,y-1), (x,y+1)]) if look_c else set()
        adjecents = [pos for pos in adj_r.union(adj_c) if pos not in current]
        # print("[DEBUG] Looking at tile {}, adjecent positions are: {}".format(tile.id, ", ".join([str(_) for _ in adjecents])))
        # fits = []
        for n, other in enumerate(remaining):
            arrangements = tile.fit(orientation, other)
            for (rel, perm) in arrangements:
                if rel=="l":
                    pos = (x-1,y)
                elif rel=="r":
                    pos = (x+1,y)
                elif rel=="t":
                    pos = (x,y+1)
                elif rel=="b":
                    pos = (x,y-1)
                else:
                    raise Exception("Unknown relative position: '{}'".format(rel))
                if pos not in adjecents:
                    continue
                (_x, _y) = pos
                keys = set([(_x-1,_y), (_x+1,_y), (_x,_y-1), (_x,_y+1)])
                # keys.discard((x, y))
                placed = [v for (k, v) in current.items() if k in keys]
                existing_fits = all([len(set(_)) == len(_) for _ in [[_[0] for _ in filter(lambda v: v[1] == ori, other.fit(perm, existing))] for (ori, existing) in placed]])
                if not existing_fits:
                    continue
                solution = solve_jigsaw([v for (k, v) in enumerate(remaining) if k != n], {**current, **{pos: (perm, other)}}, size)
                if solution is not None:
                    return solution
                # fits.append((pos, perm, other))
        # print("[DEBUG] Possible arrangements:\n[DEBUG] - {}".format("\n[DEBUG] - ".join(["{} (o: {}) at {}".format(t.id, perm, pos) for (pos, perm, t) in fits])))
    return None

solution = solve_jigsaw(borders)

s = ""
for row in solution:
    s += " ".join([str(tile.id) for (_, tile) in row])
    s += "\n"
print(s.strip())

value = int(solution[0][0][1].id) * int(solution[0][-1][1].id) * int(solution[-1][-1][1].id) * int(solution[-1][0][1].id)
print("Part 1: {}".format(value))
