""" https://adventofcode.com/2022/day/13 """

from math import prod
from itertools import zip_longest
from functools import cmp_to_key

def isrightorder(left, right):
    if len(left) == 0 and len(right) > 0:
        return True
    elif len(left) > 0 and len(right) == 0:
        return False
    elif len(left) == 0 and len(right) == 0:
        return None  # Possible call from nested lists

    lhs = left[0]
    rhs = right[0]

    left = left[1:]
    right = right[1:]

    # One of them is int one is list, convert int to list
    if isinstance(lhs, int) and isinstance(rhs, list):
        lhs = [lhs]
    elif isinstance(lhs, list) and isinstance(rhs, int):
        rhs = [rhs]

    # Compare int vs. int
    if isinstance(lhs, int) and isinstance(rhs, int):
        if lhs < rhs:
            return True
        elif lhs > rhs:
            return False 

    # Compare list vs. list
    elif isinstance(lhs, list) and isinstance(rhs, list):
        # Elements in both lists are all flat ints, compare them
        if all(isinstance(x, int) for x in lhs) and all(isinstance(x, int) for x in rhs):
            for lv, rv in zip_longest(lhs, rhs):
                if lv is None:
                    return True
                elif rv is None:
                    return False

                if lv < rv:
                    return True
                elif lv > rv:
                    return False
        else:
            # Special case: Drill down into nested lists comparisons.
            # Will return None is it isn't fruitful, then we continue
            # comparing subsequent elements in the packet overall.
            r = isrightorder(lhs, rhs)
            if r is not None:
                return r

    # No order determined yet. Compare next elements in the packet.
    return isrightorder(left, right)

def part1(f):
    i = 1
    sum_indices = 0
    while True:
        lhs = eval(f.readline().strip())
        rhs = eval(f.readline().strip())

        if isrightorder(lhs, rhs):
            sum_indices += i

        end_of_pair = f.readline()
        if not end_of_pair:
            break

        i += 1

    print('Sum of indices for right ordered packes:', sum_indices)


def part2(f):
    packets = []
    decoders = ([[2]], [[6]])

    while True:
        lhs = eval(f.readline().strip())
        rhs = eval(f.readline().strip())
        packets.append(lhs)
        packets.append(rhs)

        end_of_pair = f.readline()
        if not end_of_pair:
            break

    packets += decoders
    packets.sort(key=cmp_to_key(lambda x, y: -1 if isrightorder(x, y) else 1))
    decoder_indices = []
    for n, el in enumerate(packets):
        if el in decoders:
            decoder_indices.append(n + 1)

    print(f'Decoder key: {prod(decoder_indices)}')

with open('day13.input.txt') as f:
    part1(f)
    f.seek(0)
    part2(f)
