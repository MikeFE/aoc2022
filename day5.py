""" https://adventofcode.com/2022/day/5

    [H]         [D]     [P]
[W] [B]         [C] [Z] [D]
[T] [J]     [T] [J] [D] [J]
[H] [Z]     [H] [H] [W] [S]     [M]
[P] [F] [R] [P] [Z] [F] [W]     [F]
[J] [V] [T] [N] [F] [G] [Z] [S] [S]
[C] [R] [P] [S] [V] [M] [V] [D] [Z]
[F] [G] [H] [Z] [N] [P] [M] [N] [D]
 1   2   3   4   5   6   7   8   9
"""

import re

stacks = ()

def reset_stacks():
    global stacks
    stacks = (
        'FCJPHTW', 'GRVFZJBH', 'HPTR',
        'ZSNPHT', 'NVFZHJCD', 'PMGFWDZ',
        'MVZWSJDP', 'NDS', 'DZSFM'
    )

    stacks = [list(v) for v in stacks]

def parse_line(ln):
    r = re.match(r'move (\d+) from (\d+) to (\d+)', ln)
    return [int(x) for x in (r.group(1), r.group(2), r.group(3))]

def move_crate(num, start_pos, end_pos, v1=True):
    """ Move crates between stacks """
    sidx, eidx, step = (None, -num - 1, -1) if v1 else (-num, None, None)

    stacks[end_pos - 1] += stacks[start_pos - 1][sidx:eidx:step]
    stacks[start_pos - 1] = stacks[start_pos - 1][:-num]

def move_crates(v1):
    reset_stacks()
    answer = ''

    with open('day5.input.txt') as f:
        for ln in f:
            if not ln.startswith('move'):
                continue

            num, start_pos, end_pos = parse_line(ln.strip())
            move_crate(num, start_pos, end_pos, v1)

        answer = ''.join(s[-1] for s in stacks)
    return answer

print(move_crates(True))
print(move_crates(False))