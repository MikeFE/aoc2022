""" https://adventofcode.com/2022/day/14 """

class Cave:
    def __init__(self, width, height, offset_x):
        self.width = width
        self.height = height
        self.offset = offset_x
        self.grid = []
        for y in range(height):
            row = []
            for col in range(width):
                row.append('.')
            self.grid.append(row)

        self.grid[0][500 - offset_x] = '+'  # sand source

    def add_rock_line(self, x1, y1, x2, y2):
        """ Takes offset coords as given in user input.

        We convert it to friendly 0 based coords for our grid.
        """
        x1 -= self.offset
        x2 -= self.offset

        self.grid[y1][x1] = '#'
        self.grid[y2][x2] = '#'

        # Vertical line
        if x1 == x2:
            if y1 < y2:
                while y1 < y2:
                    self.grid[y1][x1] = '#'
                    y1 += 1
            elif y2 < y1:
                while y2 < y1:
                    self.grid[y2][x1] = '#'
                    y2 += 1
            else:
                raise ValueError(f'y coords same along with x')

        # Horizontal line
        elif y1 == y2:
            if x1 < x2:
                while x1 < x2:
                    self.grid[y1][x1] = '#'
                    x1 += 1
            elif x2 < x1:
                while x2 < x1:
                    self.grid[y1][x2] = '#'
                    x2 += 1
            else:
                raise ValueError(f'x coords same along with y')

    def move_sand(self, x1, y1, x2, y2):
        """ Attempts to move sand unit.
        Returns: (result, new_x, new_y)
        result vals:
            -1 if sand fell into abyss
            0 if sand can't move there due to rock or other sand
            1 if sand moved successfully
        """
        # Fell into abyss
        if y2 >= self.height or x2 >= self.width:
            self.grid[y1][x1] = '.'
            return (-1, None, None)

        # Fell onto rock or other sand
        if self.grid[y2][x2] in ['#', 'o']:
            return (0, x1, y1)
        else:
            # Moved successfully
            self.grid[y1][x1] = '.'
            self.grid[y2][x2] = 'o'
            return (1, x2, y2)

    def drop_sand(self):
        """ Drop sand from set location

        Returns:
            True if sand comes to rest, False if it falls into abyss or
            plugs drop point.
        """
        dp_x, dp_y = 500 - self.offset, 0
        self.grid[dp_y][dp_x] = 'o'  # sand drop point
        x, y = dp_x, dp_y  # start at drop point

        while True:
            r, x, y = self.move_sand(x, y, x, y + 1)
            if r == 0:
                # try diagonal down left
                r, x, y = self.move_sand(x, y, x - 1, y + 1)
                if r == 0:
                    # try diagonal down right
                    r, x, y = self.move_sand(x, y, x + 1, y + 1)
                    if r == 0:
                        if x == dp_x and y == dp_y:
                            return False  # Sand drop point plugged
                        return True
            if r == -1:
                return False  # Fell into abyss

    def __str__(self):
        r = ''
        for row in self.grid:
            for col in row:
                r += col
            r += '\n'
        return r

def get_cave_and_paths(f, hasfloor=False):
    f.seek(0)
    rock_paths = []
    min_x = max_x = max_y = None
    for ln in f:
        ln = ln.strip().split(' -> ')
        lines = []
        for line_coord in ln:
            coords = [int(x) for x in line_coord.split(',')]
            if min_x is None or min_x > coords[0]:
                min_x = coords[0]
            if max_x is None or max_x < coords[0]:
                max_x = coords[0]
            if max_y is None or max_y < coords[1]:
                max_y = coords[1]

            lines.append(coords)
        rock_paths.append(lines)

    if hasfloor:
        max_y += 2
        min_x, max_x = min_x - 500, max_x + 500
        rock_paths.append([[min_x, max_y], [max_x, max_y]])

    c = Cave(max_x - min_x + 1, max_y + 1, min_x)
    return (c, rock_paths)

def run_simulation(c, rock_paths):
    for line in rock_paths:
        for coord1, coord2 in zip(line, line[1:]):
            c.add_rock_line(*coord1, *coord2)

    nsand = 0
    while True:
        if not c.drop_sand():
            break
        nsand += 1
    return nsand

with open('day14.input.txt') as f:
    # Part 1
    r = run_simulation(*get_cave_and_paths(f))
    print(f'Total sand at rest: {r}')

    # Part 2
    r = run_simulation(*get_cave_and_paths(f, True))
    # +1 since we have a floor and the top sand drop point
    # being 'clogged' counts.
    print(f'Total sand at rest: {r + 1}')
