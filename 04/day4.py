""" https://adventofcode.com/2022/day/4 """

def part1(r1_l, r1_u, r2_l, r2_u):
    if (r1_l >= r2_l and r1_u <= r2_u) or (r2_l >= r1_l and r2_u <= r1_u):
        return 1
    return 0

def part2(r1_l, r1_u, r2_l, r2_u):
    if r1_l <= r2_u and r2_l <= r1_u:
        return 1
    return 0

with open('day4.input.txt') as f:
    n_total_overlapping = 0
    n_partly_overlapping = 0

    for ln in f:
        r1, r2 = ln.strip().split(',')

        r1_l, r1_u = [int(v) for v in r1.split('-')]
        r2_l, r2_u = [int(v) for v in r2.split('-')]

        n_total_overlapping += part1(r1_l, r1_u, r2_l, r2_u)
        n_partly_overlapping += part2(r1_l, r1_u, r2_l, r2_u)

    print(f'Got {n_total_overlapping} totally overlapping ranges')
    print(f'Got {n_partly_overlapping} partially overlapping ranges')