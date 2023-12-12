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

EXAMPLE = 1
PART1 = 1
PART2 = 1

day_name = os.path.basename(__file__)
day_num = re.search(r"\d+", day_name).group()
print(f"{day_name=} {day_num=}")


if __name__ == "__main__":
    filename = '/input'
    if EXAMPLE:
        filename = '/example'
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, 'r'), strip=True)
    print(f"input loaded, {len(lines)=}")

    num_rows = len(lines)
    num_cols = len(lines[0])
    galaxies = []  # list of [r,c] coordinates
    ne_cols = set() # non-empty cols
    ne_rows = set() # non-empty rows
    
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == '#':
                ne_rows.add(i)
                ne_cols.add(j)
                galaxies.append([i,j])
                
    print(f"{galaxies=}")
    print(f"{ne_cols=}")
    print(f"{ne_rows=}")

    sum = 0
    expanded = 0
    pairs = 0
    for i, g in enumerate(galaxies):
        for j, other in enumerate(galaxies[i+1:]):
            pairs += 1
            if g[0] == other[0]:
                steps_r=[]
                sum -= 1
            elif g[0] < other[0]:
                steps_r=list(range(g[0]+1,other[0]))
            else:
                steps_r=list(range(other[0]+1, g[0]))
            if g[1] == other[1]:
                steps_c=[]
                sum -= 1
            elif g[1] < other[1]:
                steps_c=list(range(g[1]+1,other[1]))
            else:
                steps_c=list(range(other[1]+1,g[1]))
            expanded_c = set(steps_c) - ne_cols
            expanded_r = set(steps_r) - ne_rows
            print(f"{i=} {j=} {g=} {other=}")
            print(f"{steps_r=} {expanded_r=}")
            print(f"{steps_c=} {expanded_c=}")
            sum += len(steps_r) + len(steps_c)  + 2
            expanded += len(expanded_r) + len(expanded_c)
            print(f"{sum=} {expanded=}")
    
    print(f"{pairs=} {sum=} {expanded=}")
    # Initially I didn't get the correct answer because we need to subtracting 1x expanded for the single "empty" already counted in the steps
    print(f"PART 2 expand 10x answer = {sum + 10 * expanded - expanded}")
    print(f"PART 2 expand 100x answer = {sum + 100 * expanded - expanded}")
    print(f"PART 2 expand 1000000x answer = {sum + 1000000 * expanded - expanded}")