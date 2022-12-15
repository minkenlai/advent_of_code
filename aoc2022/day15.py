from .lib import *
import functools
import itertools
import logging
import re

logging.basicConfig()
LOG = logging.getLogger("aoc_day15")
LOG.setLevel(logging.INFO)

EXAMPLE = True
PART1 = True
PART2 = True


def sample():
    global target_row, part2_max
    target_row = 10
    part2_max = 20
    return open("aoc2022/inputs/day15-example.txt", "r")


def input():
    global target_row, part2_max
    target_row = 2000000
    part2_max = 4000000
    return open("aoc2022/inputs/day15.txt", "r")


def dist(x, y, u, v):
    return abs(x - u) + abs(y - v)


beacons: list[tuple[int, int]] = []
max_max_x: int
min_min_x: int


def parse(lines: list[str]):
    global beacons, sensors, max_x, max_y, min_x, min_y, max_d, max_max_x, min_min_x
    p = re.compile("[xy]=-?[0-9]*")
    beacons = []
    sensors = {}
    min_x = None
    for l in lines:
        x, y, u, v = (int(e[2:]) for e in p.findall(l))
        if min_x is None:
            min_x = x
            min_min_x = x
            min_y = y
            max_x = x
            max_max_x = x
            max_y = y
            max_d = 0
        print(f"{x=} {y=} {u=} {v=}")
        d = dist(x, y, u, v)
        sensors[(x, y)] = d
        beacons.append((u, v))
        max_d = max_d if max_d is not None and max_d > d else d
        max_x = max_x if max_x > x else x
        max_y = max_y if max_y > y else y
        min_x = min_x if min_x < x else x
        min_y = min_y if min_y < y else y
        val = x - d
        min_min_x = min_min_x if min_min_x < val else val
        val = x + d
        max_max_x = max_max_x if max_max_x > val else val
    return sensors


def print_graph():
    print(f"beacon dist={sensors[(8,7)]}")
    for r in range(min_y, max_y + 1):
        l = ""
        for c in range(min_min_x, max_max_x + 1):
            if (c, r) in sensors:
                l += "S"
            elif dist(8, 7, c, r) <= sensors[(8, 7)]:
                # print(f"dist={dist(8, 7, c, r)}")
                l += "#"
            else:
                l += "."
        print(l)


def intercept_row(x, y, r):
    d = sensors[(x, y)]
    dx = d - abs(r - y)
    if dx < 0:
        return None, None
    LOG.info(f"row {r} is in range of sensor ({x}, {y}) from {x-dx=} to {x+dx=}")
    return x - dx, x + dx


if __name__ == "__main__":
    target_row = 0
    part2_max = 0
    min_x = 0
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())
    sensors = parse(lines)
    for c in sensors:
        LOG.info(f"{c=} {sensors[c]=}")
    # print_graph()

    if PART1:
        lowest = None
        highest = None
        ranges = []
        for s in sensors:
            x, y = s
            lo, hi = intercept_row(x, y, target_row)
            if lo is None or hi is None:
                continue
            ranges = merge_ranges(ranges, (lo, hi))
            if lowest is None or highest is None:
                lowest = lo
                highest = hi
            if lo < lowest:
                lowest = lo
            if hi > highest:
                highest = hi
        count = 0
        LOG.info(f"{ranges=}")
        for r in ranges:
            count += r[1] - r[0] + 1
        b_in_row = set()
        for b in beacons:
            if b[1] == target_row:
                b_in_row.add(b)
        count -= len(b_in_row)
        print(f"{count=}")

    if PART2:
        gaps = []
        lowest = 0
        highest = part2_max
        for target_row in range(lowest, highest + 1):
            ranges = []
            for s in sensors:
                x, y = s
                lo, hi = intercept_row(x, y, target_row)
                if lo is None or hi is None:
                    continue
                ranges = merge_ranges(ranges, (lo, hi))
                if lowest is None or highest is None:
                    lowest = lo
                    highest = hi
                if lo < lowest:
                    lowest = lo
                if hi > highest:
                    highest = hi
            print(f"{target_row=} {ranges=}")
            prev = (0, 0)
            for r in ranges:
                if r[0] - prev[1] > 1:
                    print(
                        f"======= row {target_row} has a gap between {prev[1]} and {r[0]}"
                    )
                    gaps.append((target_row, prev[1], r[0]))
                prev = r
        print(f"{gaps=}")

print(f"done {__name__}")
