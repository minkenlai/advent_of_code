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

EXAMPLE = True and False
EXAMPLE2 = False
PART1 = True
PART2 = True

day_name = os.path.basename(__file__)
day_num = re.search(r"\d+", day_name).group()
print(f"{day_name=} {day_num=}")

def parse(lines: list[str]):
    values = {}
    return values


def print_graph(graph):
    for l in graph:
        print(l)

def is_symbol(c):
    return c in '!@#$%^&*_+-=/'

gears={}

# PART1: Look for symbol on the line between start and end
# PART2: when '*' symbol is found, remember the number in a hash with the '*' coordinate key
def has_symbol(l, s, e, ln, num):
    if s < 0:
        i = 0
    else:
        i = s
    found = False
    while i < e and i < len(l):
        if PART2 and l[i] == '*':
            co = f"{ln}_{i}"
            if co in gears:
                gears[co].append(num)
            else:
                gears[co] = [num]
        if is_symbol(l[i]):
            found = True
            if not PART2:
                break
        i += 1
    # For debugging, print the segment checked:
    #print(f"checked {l[s:e]=}")
    return found
    

if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(open(curr_dir + '/example', 'r'), strip=True)
    elif EXAMPLE2:
        lines = all_lines(open(curr_dir + '/example2', 'r'), strip=True)
    else:
        lines = all_lines(open(curr_dir + '/input', 'r'), strip=True)
        print(f"{len(lines)=}")

    sum = 0
    last_line = None
    pattern = r"\d+"

    if PART1:
        for i, l in enumerate(lines):
            if i < len(lines) - 1:
                next_line = lines[i+1]
            else:
                next_line = None
            matches = re.findall(pattern, l)
            print(l)
            end = 0
            for match in matches:
                start = l.index(match, end)
                end = start + len(match)
                inline = has_symbol(l, start - 1, end + 1, i, int(match))
                above = (last_line and has_symbol(last_line, start - 1, end + 1, i-1, int(match)))
                below = (next_line and has_symbol(next_line, start -1, end + 1, i+1, int(match)))
                if inline or above or below:
                    sum += int(match)
                    print(f"{match=} {sum=}")
            last_line = l
        print(f"============= Answer to PART 1: {sum=}")
    if PART2:
        sum = 0
        gear = '[*]'
        print(gears)
        for i, l in enumerate(lines):
            if i < len(lines) - 1:
                next_line = lines[i+1]
            else:
                next_line = None
            matches = re.findall(gear, l)
            print(l)
            end = 0
            for match in matches:
                start = l.index(match, end)
                end = start + 1
                co = f"{i}_{start}"
                if co in gears:
                    gs = gears[co]
                    print(f"{co=} {gs=}")
                    if len(gs) == 2:
                        sum += gs[0] * gs[1]
                        print(f"{sum=}")
                    else:
                        print(f"{co=} not gear")
                else:
                    print(f"{co=} not gear")
        print(f"============= Answer to PART 2: {sum=}")

LOG.info(f"done {__name__}")

