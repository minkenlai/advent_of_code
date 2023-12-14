import os
import sys
import functools
import itertools
import logging
import re

curr_dir = os.path.dirname(__file__)
aoc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(aoc_dir)
print(f"{sys.path=}")

import aoc2023.lib
from aoc2023.lib import all_lines, sample, input, LOG

EXAMPLE = 0
PART1 = 1
PART2 = 1

day_name = os.path.basename(__file__)
day_num = re.search(r"\d+", day_name).group()
print(f"{day_name=} {day_num=}")

def split_springs(springs):
    return springs.replace('.',' ').split()

sum = 0

def count_ways(s, g):
    print(f"count_ways({s}, {g})")
    return 1

def eliminate_known(springs, groups):
    global sum
    while len(springs) and len(groups):
        s = springs[0]
        g = groups[0]
        if len(s) < g:
            springs.pop(0)
        elif '#' in s and (len(s) == g):
            springs.pop(0)
            groups.pop(0)
            sum += count_ways(s, g)
        else:
            break
    while len(springs) and len(groups):
        s = springs[-1]
        g = groups[-1]
        if len(s) < g:
            springs.pop()
        elif '#' in s and (len(s) == g):
            springs.pop()
            groups.pop()
            sum += count_ways(s, g)
        else:
            break
    return springs, groups
                
LOG.setLevel('WARNING')

if __name__ == "__main__":
    filename = '/input'
    if EXAMPLE:
        filename = '/example'
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, 'r'), strip=True)
    LOG.info(f"input loaded, {len(lines)=}")

    for l in lines:
        springs, groups = l.split()
        springs = split_springs(springs)
        groups = list(int(g) for g in groups.split(','))
        LOG.info(f"{springs=} {groups=}")

        springs, groups = eliminate_known(springs, groups)
        LOG.info(f"after eliminate_known, {springs=} {groups=}")

        if len(springs) != len(groups):
            LOG.warn(f"unequal numbers: {springs=} {groups=}")