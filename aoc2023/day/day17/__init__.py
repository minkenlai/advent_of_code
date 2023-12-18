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

EXAMPLE = 0
PART1 = 1
PART2 = 1

day_name = os.path.basename(os.path.dirname(__file__))
day_num = int(day_name[3:]) if day_name.startswith("day") else "unknown"
print(f"{day_name=} {day_num=}")

table = []
size_r = 0
size_c = 0
stack = []


def get_node(r, c):
    if r >= 0 and c >= 0 and r < size_r and c < size_c:
        return table[r][c]
    return None


def enqueue(node, from_dir, sum):
    stack.append((node, from_dir, sum))


class Node:
    def __init__(self, r, c, val):
        self.r = r
        self.c = c
        self.v = val
        self.best_sum = 0
        self.best_dir = None
        self.incoming = []

    def eval(self, from_dir, sum):
        # from_dir has the last three directions, e.g. ['>','>','>']
        if self.best_sum and sum > self.best_sum:
            LOG.warn(f"should not have entered {self} with {from_dir=} {sum=}")
            return
        if not self.best_dir:
            self.best_dir = from_dir
        elif self.best_dir[0] == self.best_dir[1]:
            if from_dir[0] != from_dir[1]:
                self.best_dir = from_dir
            elif self.best_dir[1] == self.best_dir[2] and from_dir[1] != from_dir[2]:
                self.best_dir = from_dir
            elif sum == self.best_sum:
                return
        elif sum == self.best_sum:
            return
        self.best_sum = sum
        for dir in [">", "v", "<", "^"]:
            if from_dir == [dir, dir, dir]:
                continue
            elif dir == ">" and from_dir[0] != "<":
                next_node = get_node(self.r, self.c + 1)
            elif dir == "v" and from_dir[0] != "^":
                next_node = get_node(self.r + 1, self.c)
            elif dir == "<" and from_dir[0] != ">":
                next_node = get_node(self.r, self.c - 1)
            elif dir == "^" and from_dir[0] != "v":
                next_node = get_node(self.r - 1, self.c)
            else:
                continue
            if not next_node:
                continue
            if next_node.best_sum and next_node.best_sum < self.best_sum + next_node.v:
                continue
            enqueue(
                next_node, [dir, from_dir[0], from_dir[1]], self.best_sum + next_node.v
            )
        return self.r, self.c, self.best_dir, self.best_sum, self.v

    def __str__(self):
        return f"[{self.r}, {self.c}]: from {self.best_dir} sum {self.best_sum}"


def main():
    module_dir = os.path.dirname(__file__)
    print(f"{module_dir=}")
    filename = "input"
    if EXAMPLE:
        filename = "example"
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(os.path.join(module_dir, filename), "r"), strip=True)
    print(f"input loaded, {len(lines)=}")

    size_r = len(lines)
    size_c = len(lines[0])
    for i, l in enumerate(lines):
        table.append(list(Node(i, j, int(val)) for j, val in enumerate(l)))

    enqueue(table[0][0], [">", "", ""], 0)
    i = 0
    while stack:
        node, from_dir, sum = stack.pop(-1)
        r = node.eval(from_dir, sum)
        if r:
            i += 1
            if i % 100 == 1:
                print(f"{i=} {r=}")

    if False:
        r = size_r - 1
        c = size_c - 1
        while (r, c) != (0, 0):
            table[r][c].best_dir[0]

    print(f"best at {str(get_node(size_r-1,size_c-1))}")


if __name__ == "__main__":
    main()
