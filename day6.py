""" https://adventofcode.com/2022/day/6 """

import sys

from collections import deque

def check_sequence(f, part2=False):
    nread = 0
    nunique = 14 if part2 else 4
    q = deque()

    while True:
        q.append(f.read(1))
        nread += 1

        # Fill queue up if it hasn't read nunique yet
        if len(q) != nunique:
            continue

        if len(set(q)) == nunique:
            return nread

        # Sequence not unique, remove oldest char from left.
        q.popleft()


with open('day6.input.txt') as f:
    n = check_sequence(f)
    print(f'First unique header (4 char) sequence found after processing {n} chars.')

    f.seek(0)

    n = check_sequence(f, part2=True)
    print(f'First unique message (14 char) sequence found after processing {n} chars.')





