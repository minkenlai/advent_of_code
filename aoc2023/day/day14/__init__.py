import os
import sys
import functools
import itertools
import logging
import re

curr_dir = os.path.dirname(__file__)
aoc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(aoc_dir)
print(f"{sys.path=}")

import aoc2023.lib
from aoc2023.lib import all_lines, sample, input, LOG

EXAMPLE = 1
PART1 = 1
PART2 = 1

day_name = os.path.basename(os.path.dirname(__file__))
day_num = int(day_name[3:]) if day_name.startswith("day") else "unknown"
print(f"{day_name=} {day_num=}")


def count_load(lines) -> int:
    sum = 0
    weight = len(lines)
    for i, l in enumerate(lines):
        for c in l:
            if c == "O":
                sum += weight
        # print(f"after line {i} {sum=}")
        weight -= 1
    return sum


def shift_north(lines):
    shifted = []
    for i, l in enumerate(lines):
        if i == 0:
            updated = []
            for j, c in enumerate(l):
                if c == "." or isinstance(c, int):
                    updated.append(0)
                else:
                    updated.append(c)
            shifted.append(updated)
            continue
        updated = []
        for j, c in enumerate(l):
            above = shifted[i - 1][j]
            if c == "." or isinstance(c, int):
                if isinstance(above, int):
                    updated.append(above)
                else:
                    updated.append(i)
            elif c == "O" and isinstance(above, int):
                # place in north-most free space
                shifted[above][j] = "O"
                # remember the next free space
                updated.append(above + 1)
            else:
                updated.append(c)
        shifted.append(updated)

        if False:
            print(f"======= after {i} {l=}")
            for l in shifted:
                print("".join(str(v) for v in l))
    return shifted


def shift_south(lines):
    return list(reversed(shift_north(reversed(lines))))


def shift_west(lines, rev=False):
    shifted = []
    for i, l in enumerate(lines):
        updated = []
        prev = "#"
        if rev:
            l = reversed(l)
        for j, c in enumerate(l):
            if c == "." or isinstance(c, int):
                if isinstance(prev, int):
                    updated.append(prev)
                else:
                    updated.append(j)
                    prev = j
            elif c == "O" and isinstance(prev, int):
                updated[prev] = c
                prev += 1
                updated.append(prev)
            else:
                prev = c
                updated.append(c)
        if rev:
            updated = list(c for c in reversed(updated))
        # print(f"{''.join(str(v) for v in lines[i])} ==> {''.join(str(v) for v in updated)}")
        shifted.append(updated)
    return shifted


def shift_east(lines):
    return shift_west(lines, rev=True)


def main():
    filename = "/input"
    if EXAMPLE:
        filename = "/example"
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, "r"), strip=True)
    print(f"input loaded, {len(lines)=}")
    shifted = lines
    seen_cycles = set()
    repeated = []
    first_found = None
    cycles = 1000000000
    for i in range(1000000000):
        cycle = []
        shifted = shift_north(shifted)
        load = count_load(shifted)
        cycle.append(load)
        # print(f"after north, total {load=}")
        shifted = shift_west(shifted)
        load = count_load(shifted)
        cycle.append(load)
        # print(f"after west, total {load=}")
        shifted = shift_south(shifted)
        load = count_load(shifted)
        cycle.append(load)
        # print(f"after south, total {load=}")
        shifted = shift_east(shifted)
        load = count_load(shifted)
        cycle.append(load)
        # print(f"after east, total {load=}")
        print(f"{cycle=}")
        cycle = str(cycle)
        if cycle in seen_cycles:
            print(f"Found repeated {cycle=} at {i=}")
            if not first_found:
                first_found = i
            if cycle in repeated:
                print(f"Found double-repeated {cycle=}")
                print(f"{first_found=} {len(repeated)=}")
                print(f"{repeated=}")
                break
            repeated.append(cycle)
        seen_cycles.add(cycle)
        for l in shifted:
            print("".join("." if isinstance(c, int) else c for c in l))

    # calculate based on repeats:
    position = (cycles - first_found) % len(repeated)
    print(
        f"Answer should be load after the {position}th in the cycle of cycles, {repeated[position-1]}"
    )


if __name__ == "__main__":
    main()
