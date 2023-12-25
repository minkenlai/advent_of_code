import os
import sys
import collections
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

day_name = os.path.basename(curr_dir)
day_num = day_name[3:] if day_name.startswith('day') else 'unknown'
print(f"{day_name=} {day_num=}")

class Plot:
    def __init__(self, r, c, rock=0):
        self.r = r
        self.c = c
        self.rock = rock
        self.step_num = []

    def enter(self, step_num) -> int:
        # returns 1 if it's the first time visiting on odd/even step_num
        if self.rock or len(self.step_num) >= 2:
            return 0
        if not self.step_num or (step_num - self.step_num[0]) % 2:
            self.step_num.append(step_num)
            print(self.describe())
            return 1
        return 0

    def describe(self):
        return f"{self.r},{self.c}:{self.step_num=}"

    def reachable(self, step_num):
        if self.rock or not self.step_num:
            return 0
        if len(self.step_num) == 2:
            return 1
        if (step_num - self.step_num[0]) % 2 == 0:
            return 1
        return 0

    def tile(self, step_num):
        if self.reachable(step_num):
            return 'O'
        elif self.rock:
            return '#'
        return '.'


def try_neighbor(rn, cn, step_num):
    global queues
    if rn>=0 and rn<num_rows and cn>=0 and cn<num_cols:
        n = garden[key(rn, cn)]
        if n.enter(step_num):
            queues[step_num].add((rn, cn))

def print_garden(step_num):
    for r in range(num_rows):
        for c in range(num_cols):
            print(garden[key(r, c)].tile(step_num), end='')
        print()

queues=[]

def part1(steps) -> int:
    global garden, queues, start
    for _ in range(num_rows):
        queues.append(set())
    queues[0].add((start[0], start[1]))
    for current_step in range(steps):
        for r, c in queues[current_step]:
            next_step = current_step + 1
            try_neighbor(r-1,c,next_step)
            try_neighbor(r+1,c,next_step)
            try_neighbor(r,c-1,next_step)
            try_neighbor(r,c+1,next_step)
        print(f"after trying all neighbors for {next_step=}")
        print_garden(next_step)
    num_reachable = 0
    for v in garden.values():
        if v.reachable(steps):
            num_reachable += 1
    print(f"{num_reachable=}")
    return num_reachable

def part2(steps) -> int:
    pass

def key(r, c):
    return f"{r}_{c}"

def main():
    global lines, garden, num_rocks, num_rows, num_cols, start
    filename = "input"
    if EXAMPLE:
        filename = "example"
        if EXAMPLE > 1:
            filename = filename + str(EXAMPLE)
    lines = all_lines(open(os.path.join(curr_dir, filename), "r"), strip=True)
    print(f"input loaded, {len(lines)=}")
    garden = {}
    num_rows = len(lines)
    num_cols = len(lines[0])
    num_rocks = 0
    start = None
    for r, l in enumerate(lines):
        for c, e in enumerate(l):
            rock = 1 if e=='#' else 0
            if not start and e=='S':
                start = (r, c)
            garden[key(r, c)] = Plot(r, c, rock)
            num_rocks += 1
    print(f"loaded {len(garden)} tiles and {num_rocks=} {start=}")
    if len(garden) != num_rows * num_cols:
        raise Exception(f"{num_rows=} {num_cols=} plots={len(garden)}")

    if PART1:
        part1(6 if EXAMPLE else 64)

    if PART2:
        part2(start)


if __name__ == "__main__":
    main()