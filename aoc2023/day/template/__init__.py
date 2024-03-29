import os
import sys
import collections
import functools
import itertools
import logging
import re

curr_dir = os.path.dirname(__file__)
aoc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if aoc_dir not in sys.path:
    sys.path.append(aoc_dir)
print(f"{sys.path=}")

import aoc2023.lib
from aoc2023.lib import read_lines, LOG

EXAMPLE = 1
PART1 = 1
PART2 = 1

day_name = os.path.basename(curr_dir)
day_num = day_name[3:] if day_name.startswith('day') else 'unknown'
print(f"{day_name=} {day_num=}")

def part1(lines):
    pass

def part2(lines):
    pass

def main():
    read_lines(curr_dir, EXAMPLE)
    if PART1:
        part1(lines)
    if PART2:
        part2(lines)

if __name__ == "__main__":
    main()
