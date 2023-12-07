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
EXAMPLE2 = 0
PART1 = 0
PART2 = 1

day_name = os.path.basename(__file__)
day_num = re.search(r"\d+", day_name).group()
print(f"{day_name=} {day_num=}")

    
def part1():
    times = list(int(t) for t in lines[0].split()[1:])
    dists = list(int(d) for d in lines[1].split()[1:])
    answer = 1
    for i in range(len(times)):
        time = times[i]
        dist = dists[i]
        count = 0
        for j in range(1, time - 1):
            if j * (time - j) > dist:
                print(f"holding for {j} wins with {j * (time - j)=} more than {dist=}")
                count += 1
        print(f"for race with {time=} total {count=}")
        answer *= count
    print(f"{answer=}")


def approximate_start(low, high):
    while (high - low) > 1:
        hold = int((high + low) / 2)
        result = (time - hold) * hold
        if result > dist:
            high = hold
        if result < dist:
            low = hold
        print(f"{result=} next {low=} {high=}")
    return low, high
        
def approximate_end(low, high):
    print(f"start {low=} {high=}")
    while (high - low) > 1:
        hold = int((high + low) / 2)
        result = (time - hold) * hold
        if result > dist:
            low = hold
        if result < dist:
            high = hold
        print(f"{result=} next {low=} {high=}")
    return low, high


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(open(curr_dir + '/example', 'r'), strip=True)
    elif EXAMPLE2:
        lines = all_lines(open(curr_dir + '/example2', 'r'), strip=True)
    else:
        lines = all_lines(open(curr_dir + '/input', 'r'), strip=True)
    print(f"{len(lines)=}")

    if PART1:
        part1()

    if PART2:
        times = list(t for t in lines[0].split()[1:])
        dists = list(d for d in lines[1].split()[1:])
        time = int(str.join('', times))
        dist = int(str.join('', dists))
        mid = int(dist ** 0.5)
        start = approximate_start(1, mid)
        end = approximate_end(mid, time-1)
        print(f"{start=} {end=} {end[0]-start[0]=}")
