""" https://adventofcode.com/2022/day/10 """

def get_op(cycle, ln):
    """ Returns new current operation info

    Returns:
        Tuple: (cycle_num, op_str)
        cycle_num is the target cycle# the operation will complete.
    """
    if ln.startswith('noop'):
        return (cycle + 1, 'noop')
    elif ln.startswith('addx'):
        return (cycle + 2, ln.strip())
    else:
        raise Exception(f'Invalid op: {ln}')

def perform_op(X, cur_op):
    if cur_op[1].startswith('addx'):
        return X + int(cur_op[1][5:])
    return X

def add_signal_strength(signal_strengths, cycle):
    if (cycle - 20) % 40 == 0:
        signal_strengths.append(cycle * X)

def print_crt(cycle, X):
    hpos = X + 1
    row_pixel = cycle % 40

    if row_pixel == 0:
        print()  # new crt line
        return

    if row_pixel in (hpos - 1, hpos, hpos + 1):
        print('#', end='')
    else:
        print('.', end='')

with open('day10.input.txt') as f:
    X = 1
    CRT_WIDTH = 240
    cur_op = None
    signal_strengths = []
    cycle = 1

    while cycle < CRT_WIDTH:
        add_signal_strength(signal_strengths, cycle)
        print_crt(cycle, X)

        if not cur_op:
            ln = f.readline()
            if ln:
                cur_op = get_op(cycle, ln)

        cycle += 1

        # Current operation completed
        if cur_op and cycle == cur_op[0]:
            X = perform_op(X, cur_op)
            cur_op = None

    print(f'\nSum signal strengths: {sum(signal_strengths)}')