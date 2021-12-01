data = open("input.txt").read().strip().split("\n")

class Seats:

    def __init__(self, seats):

        self.seats = dict()
        self.adjecent = dict()
        self.los = dict()

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

                los = []
                # North
                size = i
                for x in range(1,size+1):
                    (l, k) = (i-x, j)
                    other = seats[l][k]
                    if other == ".":
                        continue
                    else:
                        los.append((l, k))
                        break
                
                # North west
                size = min(i, (self.width-1)-j)
                for x in range(1,size+1):
                    (l, k) = (i-x, j+x)
                    other = seats[l][k]
                    if other == ".":
                        continue
                    else:
                        los.append((l, k))
                        break

                # West
                size = (self.width-1)-j
                for x in range(1,size+1):
                    (l, k) = (i, j+x)
                    other = seats[l][k]
                    if other == ".":
                        continue
                    else:
                        los.append((l, k))
                        break

                # South west
                size = min((self.height-1)-i, (self.width-1)-j)
                for x in range(1,size+1):
                    (l, k) = (i+x, j+x)
                    other = seats[l][k]
                    if other == ".":
                        continue
                    else:
                        los.append((l, k))
                        break

                # South
                size = (self.height-1)-i
                for x in range(1,size+1):
                    (l, k) = (i+x, j)
                    other = seats[l][k]
                    if other == ".":
                        continue
                    else:
                        los.append((l, k))
                        break

                # South east
                size = min((self.height-1)-i, j)
                for x in range(1,size+1):
                    (l, k) = (i+x, j-x)
                    other = seats[l][k]
                    if other == ".":
                        continue
                    else:
                        los.append((l, k))
                        break

                # East
                size = j
                for x in range(1,size+1):
                    (l, k) = (i, j-x)
                    other = seats[l][k]
                    if other == ".":
                        continue
                    else:
                        los.append((l, k))
                        break

                # North east
                size = min(i, j)
                for x in range(1,size+1):
                    (l, k) = (i-x, j-x)
                    other = seats[l][k]
                    if other == ".":
                        continue
                    else:
                        los.append((l, k))
                        break
                
                self.los[(i, j)] = los

    def update(self, seat_tolerance, method):
        seats = dict()
        if method == "adjecent":
            sr = self.adjecent
        else:
            sr = self.los
        for idx, seat in self.seats.items():
            adjecents = [self.seats[_] for _ in sr[idx]]
            if seat == "L":
                if len([_ for _ in adjecents if _ == "#"]) == 0:
                    seats[idx] = "#"
                else:
                    seats[idx] = "L"
            else:
                if len([_ for _ in adjecents if _ == "#"]) >= seat_tolerance:
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
        print("[DEBUG] Resetting")
        for idx in self.seats.keys():
            self.seats[idx] = "L"

    def converge(self, seat_tolerance, method):
        print("[DEBUG] Simulating")
        old_seats = self.seats
        converged = False
        c = 1
        while not converged:
            # print("[DEBUG] Iteration {}".format(c))
            # self.show()
            # print()
            # print("[DEBUG] Iteration {}, occupied = {}.".format(c, s.occupied()))
            c += 1
            self.update(seat_tolerance, method)
            if self.seats == old_seats:
                converged = True
            else:
                old_seats = self.seats
        return self.occupied()

   
seats = Seats(data)
print("Part 1: {}".format(seats.converge(4, "adjecent")))

seats.reset()
print("Part 2: {}".format(seats.converge(5, "los")))
