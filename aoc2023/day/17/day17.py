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

    def eval(self, from_dir, sum): 
        # from_dir has the last two directions, e.g. ['>','>']
        if not self.best_sum or sum + self.v < self.best_sum:
            self.best_sum = sum
            self.best_dir = from_dir
            for dir in ['>', 'v', '<', '^']:
                if from_dir == [dir, dir]:
                    continue
                elif dir == '>':
                    next_node = get_node(self.r, self.c+1)
                elif dir == 'v':
                    next_node = get_node(self.r+1, self.c)
                elif dir == '<':
                    next_node = get_node(self.r, self.c-1)
                elif dir == '^':
                    next_node = get_node(self.r-1, self.c)
                else:
                    raise Exception(f"unexpected {from_dir=} at {self.r}, {self.c}")
                if next_node:
                    enqueue(next_node, [from_dir[1], dir], self.best_sum + self.v)
        return self.r, self.c, self.best_dir, self.best_sum, self.v

    def __str__(self):
        return f"[{self.r}, {self.c}]: from {self.best_dir} sum {self.best_sum}"


if __name__ == "__main__":
    filename = '/input'
    if EXAMPLE:
        filename = '/example'
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, 'r'), strip=True)
    print(f"input loaded, {len(lines)=}")
    
    size_r = len(lines)
    size_c = len(lines[0])
    for i, l in enumerate(lines):
        table.append(list(Node(i, j, int(val)) for j, val in enumerate(l)))
    
    enqueue(table[0][0], ['', '>'], 0)
    while stack:
        node, from_dir, sum = stack.pop(-1)
        print(node.eval(from_dir, sum))
        
    print(f"best at [{size_r-1}, {size_c-1}] is {str(get_node(size_r-1,size_c-1))}")