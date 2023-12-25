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

lines=[]
max_r = None
max_c = None
visited=set()

directions = {
    '>': [0,1],
    '<': [0,-1],
    '^': [-1,0],
    'v': [1,0]
}

class Tile:
    def __init__(self, r, c, prev=[-1,-1]):
        self.r = r
        self.c = c
        self.prev = prev

    def name(self) -> str:
        return f"{self.r}_{self.c}"

    def exits(self) -> list('Tile'):
        visited.add(self)
        results = []
        for offset in [[-1,0],[0,1],[1,0],[0,-1]]:
            ro, co = offset
            rn = self.r+ro
            cn = self.c+co
            if self.is_entry(rn, cn):
                continue
            t = Tile(rn, cn) if 0 <= rn and rn < max_r and 0 <= cn and cn < max_c else None
            if t.type() == '.':
                results.append(t)
            elif (t.type() in directions and directions[t.type()] == offset):
                results.append(t)
            elif t.type() != '#':
                LOG.warn(f"{self} -> {ro},{co} -> {t.type()=}")
        return results

    def is_entry(self, r, c) -> bool:
        return self.prev == [r, c]

    def type(self):
        return lines[self.r][self.c]


class Path:
    # graph edge
    def __init__(self, length, direction='both'):
        self.length = length
        self.direction = direction

class Node(Tile):
    # graph vertex
    def __init__(self, r, c, connected):
        super.__init__(r, c)
        self.connected = connected

def lines2graph(lines):
    global nodes, paths
    queue = collections.deque()
    start_c = lines[0].index('.')
    end_c = lines[len(lines)-1].index('.')
    print(f"{start_c=} {end_c=}")
    queue.append(Tile(0, start_c, [-1,0]))
    # follow path to reach an intersection
    while queue:
        tile = queue.popleft()
        outs = tile.exits()
        queue.extend(t for t in outs if t not in visited)

def main():
    global lines, max_r, max_c
    filename = "input"
    if EXAMPLE:
        filename = "example"
        if EXAMPLE > 1:
            filename = filename + str(EXAMPLE)
    lines = all_lines(open(os.path.join(curr_dir, filename), "r"), strip=True)
    max_r = len(lines)
    max_c = len(lines[0])
    print(f"input loaded, {len(lines)=}")



if __name__ == "__main__":
    main()