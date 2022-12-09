""" https://adventofcode.com/2022/day/9 """

class Knot:
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.name = name

    def __str__(self):
        return f'{self.name} ({self.x}, {self.y})'

tlocs = {}

def moveh(H, direction):
    if direction == 'U':
        H.y += 1
    elif direction == 'D':
        H.y -= 1
    elif direction == 'L':
        H.x -= 1
    elif direction == 'R':
        H.x += 1


def istouching(leadknot, followknot):
    return abs(leadknot.x - followknot.x) < 2 and abs(leadknot.y - followknot.y) < 2


def follow(leadknot, followknot, recordpos=False):
    if istouching(leadknot, followknot):
        return

    if followknot.x != leadknot.x:
        followknot.x += 1 if leadknot.x > followknot.x else -1
    if followknot.y != leadknot.y:
        followknot.y += 1 if leadknot.y > followknot.y else -1

    if recordpos:
        tlocs[str(followknot)] = True


def part1(f):
    H = Knot('H')
    T = Knot('T')

    for ln in f:
        direction, num = ln.strip().split(' ')
        for _ in range(int(num)):
            moveh(H, direction)
            follow(H, T, True)

    print(f'Total tail locations: {len(tlocs.keys())}')


def part2(f):
    H = Knot('H')
    knots = [H]
    for n in range(9):
        knots.append(Knot(f'{n + 1}'))

    for ln in f:
        direction, num = ln.strip().split(' ')
        for _ in range(int(num)):
            moveh(knots[0], direction)

            # Move the knots following one after the other
            for n in range(1, 9):
                follow(knots[n - 1], knots[n])
            # Record Knot 9 aka the tail's positions
            follow(knots[8], knots[9], True)

    # +1 since starting position counts now
    print(f'Total tail locations: {len(tlocs.keys()) + 1}')


with open('day9.input.txt') as f:
    part1(f)
    f.seek(0)
    tlocs.clear()
    part2(f)