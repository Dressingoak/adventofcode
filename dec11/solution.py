data = open("input.txt").read().strip().split("\n")

class Seats:

    def __init__(self, seats):

        self.seats = dict()
        self.adjecent = dict()

        print("[DEBUG] Organizing seats")

        self.height = len(seats)
        for i, row in enumerate(seats):
            self.width = len(row)
            for j, seat in enumerate(row):
                if seat == ".":
                    continue
                self.seats[(i, j)] = seat
                idxs = []
                lmin, lmax = max(i-1, 0),min(i+2, self.height)
                for l, hz in enumerate(seats[lmin:lmax]):
                    kmin, kmax = max(j-1, 0),min(j+2, self.width)
                    for k, other in enumerate(hz[kmin:kmax]):
                        if other == "." or (lmin+l == i and kmin+k == j):
                            continue
                        idxs.append((lmin+l, kmin+k))
                self.adjecent[(i, j)] = idxs
    
    def update(self):
        seats = dict()
        for idx, seat in self.seats.items():
            adjecents = [self.seats[_] for _ in self.adjecent[idx]]
            if seat == "L":
                if len([_ for _ in adjecents if _ == "#"]) == 0:
                    seats[idx] = "#"
                else:
                    seats[idx] = "L"
            else:
                if len([_ for _ in adjecents if _ == "#"]) >= 4:
                    seats[idx] = "L"
                else:
                    seats[idx] = "#"
        self.seats = seats

    # For debug
    def show(self):
        canvas = ["."*self.width for _ in range(self.height)]
        for idx, seat in self.seats.items():
            (i, j) = idx
            canvas[i] = canvas[i][:j] + seat + canvas[i][j + 1:] 
        for _ in canvas:
            print(_)
        return None

    def occupied(self):
        return len([_ for _ in self.seats.values() if _ == "#"])

    def reset(self):
        for idx in self.seats.keys():
            self.seats[idx] = "L"

    def converge_part1(self):
        old_seats = self.seats
        converged = False
        c = 1
        while not converged:
            # print("[DEBUG] Iteration {}, occupied = {}.".format(c, s.occupied()))
            c += 1
            self.update()
            if self.seats == old_seats:
                converged = True
            else:
                old_seats = self.seats
        return self.occupied()

   
seats = Seats(data)
print("Part 1: {}".format(seats.converge_part1()))
