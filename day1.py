""" https://adventofcode.com/2022/day/1 """

import sys

def get_inventories():
    """ Total up calories for each elf's rations.

    Each ration calorie total is inputted on a new line, a blank line indicates the end of an elf's inventory.

    Returns a list of ints (calorie totals) per elf inventory.
    """

    try:
        calorie_totals = []

        while True:
            cur_total = 0

            for ln in sys.stdin:
                ln = ln.rstrip()  # Remove newline characters

                # Blank line indicating end of this particular elf's inventory
                if ln == '':
                    calorie_totals.append(cur_total)
                    break

                cur_total += int(ln)

    except (EOFError, KeyboardInterrupt):
        sys.stdout.flush()
    except Exception as e:
        print(f'Unknown exception - {e}')
        sys.exit()
    finally:
        return calorie_totals

def get_top3_inventories(inventories):
    """ Return list of top 3 highest calorie integer totals

        inventories - list of integers indicating calorie totals for each elf's inventory.
    """
    assert inventories and len(inventories) >= 3
    return sorted(inventories, reverse=True)[0:3]

def main():
    inv = get_inventories()
    print(f'Max calories carried by an elf: {max(inv)}')

    top3_inv = get_top3_inventories(inv)
    print(f'Calories carried by top 3 elf inventories: {sum(top3_inv)}')

if __name__ == '__main__':
    main()