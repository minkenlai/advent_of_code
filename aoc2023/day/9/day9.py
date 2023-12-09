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


def all_zeros(l: list) -> bool :
    for v in l:
        if v:
            return False
    return True

def extrapolate(m: list) -> int:
    # extrapolate from bottom up
    d = 0
    for j in range(len(m)-1, -1, -1):
        d = m[j][-1] + d
        print(f"{m[j]} {d}")
    return d

def derivatives(values) -> list:
    m = []
    while not all_zeros(values):
        m.append(values)
        row = []
        for i in range(1, len(values)):
            row.append(values[i] - values[i-1])
        print(row)
        values = row
    return m

def run(lines: list, rev=False):
    answer = 0
    for l in lines:
        print(l)
        values = [int(v) for v in l.split()]
        if rev:
            values = list(reversed(values))
        else:
            values = [int(v) for v in l.split()]
        m = derivatives(values)
        answer += extrapolate(m)
        print(f"{answer=}")

if __name__ == "__main__":
    filename = '/input'
    if EXAMPLE:
        filename = '/example'
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, 'r'), strip=True)
    print(f"input loaded, {len(lines)=}")

    if PART1:
        run(lines)
    if PART2:
        run(lines, rev=True)
        