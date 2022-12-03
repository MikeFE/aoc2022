""" https://adventofcode.com/2022/day/3 """

def get_char_val(ch):
    if ch.isupper():
        return ord(ch) - ord('A') + 27
    return ord(ch) - ord('a') + 1

def part1(f):
    total = 0
    for ln in f.readlines():
        ln = ln.strip()
        # Split string in half, find common character between the two via set intersection
        total += get_char_val((set(ln[:len(ln) // 2]) & set(ln[len(ln) // 2:])).pop())
    print(f'Sum of mispacked items: {total}')

def part2(f):
    total = 0
    # "Grouper" pattern to read lines in batches of 3:
    # https://docs.python.org/3/library/itertools.html
    for group_sacks in zip(*[iter(f)] * 3):
        sack_sets = [set(g.strip()) for g in group_sacks]
        # Get common character between the 3 sacks
        total += get_char_val((sack_sets[0] & sack_sets[1] & sack_sets[2]).pop())
    print(f'Sum of badges: {total}')

with open('day3.input.txt') as f:
    part1(f)
    f.seek(0)
    part2(f)
