""" https://adventofcode.com/2022/day/15 """

import re
import sys

from dataclasses import dataclass, field

def dist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

@dataclass
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int
    beacon_dist: int = field(init=False)

    def __post_init__(self):
        self.beacon_dist = dist(self.x, self.y, self.beacon_x, self.beacon_y)


def row_coverage(s, row):
    dist_y = abs(row - s.y)
    if dist_y > s.beacon_dist:
        return None  # Beacon out of range, ignore
    range_x = s.beacon_dist - dist_y

    return (s.x - range_x, s.x + range_x + 1)

def validator(sensors, x, y):
    for s in sensors:
        if dist(x, y, s.x, s.y) <= s.beacon_dist:
            return False
    return True

with open('day15.input.txt') as f:
    sensors = []
    impossible_coords = set()
    for ln in f:
        r = re.findall(r'x=(-?\d+), y=(-?\d+)', ln.strip())

        sensor_coords = [int(x) for x in r[0]]
        beacon_coords = [int(x) for x in r[1]]

        sensors.append(Sensor(*sensor_coords, *beacon_coords))
    
    row = 2000000
    for s in sensors:
        imp_range = row_coverage(s, row)
        if not imp_range:
            continue

        impossible_coords.update(list(range(imp_range[0], imp_range[1])))
        if s.beacon_y == row:
            impossible_coords.discard(s.beacon_x)
    print(f'{len(impossible_coords)} positions cannot contain a beacon.')

    # part 2
    MAX_RANGE_X = MAX_RANGE_Y = 4000000

    directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    for s in sensors:
        for dx in range(s.beacon_dist + 2):
            dy = (s.beacon_dist + 1) - dx
            for sign_x, sign_y in directions:
                check_x = s.x + (dx * sign_x)
                check_y = s.y + (dy * sign_y)

                if not(0 <= check_x <= MAX_RANGE_X and 0 <= check_y <= MAX_RANGE_Y):
                    continue
                
                if validator(sensors, check_x, check_y):
                    print(f'Found beacon at ({check_x}, {check_y}): tuning freq={check_x * MAX_RANGE_X + check_y}') 
                    sys.exit()