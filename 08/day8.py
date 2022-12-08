""" https://adventofcode.com/2022/day/8

3   0   3   7   3   
2   5   5   1   2
6   5   3   3   2
3   3   5   4   9
3   5   3   9   0
"""

DIRECTIONS = ('top', 'bottom', 'left', 'right')

def get_trees_in_direction(m, row, col, direction):
    if direction == 'left':
        vals = m[row][:col]
        vals.reverse()
    elif direction == 'right':
        vals = m[row][col + 1:]
    elif direction == 'top':
        vals = [v[col] for v in m[:row]]
        vals.reverse()
    elif direction == 'bottom':
        vals = [v[col] for v in m[row + 1:]]
    return vals


def visible(m, row, col, direction):
    vals = get_trees_in_direction(m, row, col, direction)
    return m[row][col] > max(vals)


def viewing_dist(cur_tree_val, distant_trees):
    n = 0
    for val in distant_trees:
        if cur_tree_val <= val:
            n += 1  # count the tree blocking the view
            break
        n += 1
    return n


def scenic_score(m, row, col):
    score = 1
    for d in DIRECTIONS:
        dist = viewing_dist(m[row][col], get_trees_in_direction(m, row, col, d))
        score *= dist
    return score


def part1(matrix):
    outer_trees = (len(matrix) * 2) + (len(matrix[0]) * 2) - 4
    nvisible = outer_trees

    # Check visibility of inner trees
    row = col = 1
    while row < len(matrix) - 1:
        col = 1
        while col < len(matrix[0]) - 1:
            for d in DIRECTIONS:
                if visible(matrix, row, col, d):
                    nvisible += 1
                    break
            col += 1
        row += 1
    print(f'Number trees visible: {nvisible}')


def part2(matrix):
    scores = []

    # Ignore outer trees as their scenic score will always be 0.
    row = col = 1
    while row < len(matrix) - 1:
        col = 1
        while col < len(matrix[0]) - 1:
            scores.append(scenic_score(matrix, row, col))
            col += 1
        row += 1
    print(f'Max scenic score: {max(scores)}')


with open('day8.input.txt') as f:
    matrix = []
    for ln in f:
        matrix.append([int(v) for v in list(ln.strip())])

    part1(matrix)
    part2(matrix)