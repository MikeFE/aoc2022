""" https://adventofcode.com/2022/day/11 """

import re
from collections import deque
from math import prod

class Monkey:
    def __init__(self, name, start_items, operation, test):
        self.name = name
        self.items = deque(start_items)
        self.op_eval = operation[len('new = '):]
        self.test_vals = test
        self.num_inspections = 0

    def operation(self, item):
        self.num_inspections += 1
        old = item
        return eval(self.op_eval)

    def test(self, item):
        if item % self.test_vals[0] == 0:
            return self.test_vals[1]
        return self.test_vals[2]

def get_monkeys(s):
    monkeys = []
    pattern = (
        r'Monkey (\d+):$'
        r'.*?Starting items: (.+?)$'
        r'.*?Operation: (.+?)$'
        r'.*?Test: divisible by (\d+?)$'
        r'.*?If true: throw to monkey (\d+?)$'
        r'.*?If false: throw to monkey (\d+?)$'
    )

    matches = re.findall(pattern, s, re.M | re.S)
    for r in matches:
        m = Monkey(
            name=r[0],
            start_items=[int(v) for v in r[1].split(', ')],
            operation=r[2],
            test=[int(v) for v in r[3:]]
        )

        monkeys.append(m)
    return monkeys

def do_round(f, num_rounds, can_reduce_worry):
    monkeys = get_monkeys(f.read())

    for _ in range(num_rounds):
        for m in monkeys:
            while len(m.items):
                m.items[0] = m.operation(m.items[0])  # inspect item, raise worry
                if can_reduce_worry:
                    m.items[0] //= 3  # done inspect, lower worry
                monkey_to = m.test(m.items[0])  # determine what monkey to toss to based on worry
                monkeys[monkey_to].items.append(m.items.popleft())  # toss to other monkey

    inspection_counts = [m.num_inspections for m in monkeys]
    inspection_counts.sort(reverse=True)
    monkey_business = prod(inspection_counts[:2])
    print(f'Monkey business: {monkey_business}')

with open('day11.input.txt') as f:
    do_round(f, 20, True)
    f.seek(0)
    do_round(f, 10000, False)