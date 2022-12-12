from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class MtnGrid(Grid):
    def __init__(self, grid):
        self.grid = grid
        super().__init__(len(grid[0]), len(grid))

    def canclimb(self, cur_x, cur_y, to_x, to_y):
        if not self.inside(to_x, to_y):
            return False

        dest_val = ord(self.grid[to_y][to_x])
        src_val = ord(self.grid[cur_y][cur_x])

        # Can only climb to coords that are '1 higher or less'
        # letter-wise.
        if dest_val - src_val <= 1:
            return True

        return False

    def neighbors(self, node, diagonal_movement=DiagonalMovement.never):
        """ Only let pathfinder see coords that are climbable as neighbors.

            Overrides Grid.neighbors().
        """
        x = node.x
        y = node.y
        neighbors = []

        # up
        if self.canclimb(x, y, x, y - 1):
            neighbors.append(self.nodes[y - 1][x])
        # right
        if self.canclimb(x, y, x + 1, y):
            neighbors.append(self.nodes[y][x + 1])
        # down
        if self.canclimb(x, y, x, y + 1):
            neighbors.append(self.nodes[y + 1][x])
        # left
        if self.canclimb(x, y, x - 1, y):
            neighbors.append(self.nodes[y][x - 1])

        return neighbors

def build_grid(f):
    grid = []
    for y, ln in enumerate(f.readlines()):
        row = list(ln.strip())
        grid.append(row)

        try:
            x = row.index('S')
            start_pos = (x, y)
            grid[y][x] = 'a'
        except ValueError:
            pass

        try:
            x = row.index('E')
            end_pos = (x, y)
            grid[y][x] = 'z'
        except ValueError:
            pass
    return (start_pos, end_pos, grid)

def get_potential_start_positions(grid):
    r = []
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == 'a':
                r.append((x, y))
    return r

def do_searches(f):
    spos, epos, raw_grid = build_grid(f)
    grid = MtnGrid(raw_grid)

    start = grid.node(*spos)
    end = grid.node(*epos)

    # part 1
    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)
    print(f'Shortest path length from S: {len(path) - 1}')

    shortest_path = None

    # part 2
    for spos in get_potential_start_positions(raw_grid):
        grid.cleanup()  # Important otherwise pathfinder breaks across multiple calls
        path, runs = finder.find_path(grid.node(*spos), end, grid)
        path_len = len(path) - 1
        if shortest_path is None or path_len < shortest_path and path_len > 0:
            shortest_path = path_len
    print(f'Shortest path length for all possible starting positions: {shortest_path}')

with open('day12.input.txt') as f:
    do_searches(f)



