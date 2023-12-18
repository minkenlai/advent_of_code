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

table = None
cols = 0
rows = 0
queue = []


class Spot:
    def __init__(self, char, r, c):
        self.char = char
        self.r = r
        self.c = c
        self.lit_from = set()

    def from_left(self):
        if ">" in self.lit_from:
            return
        self.lit_from.add(">")
        if self.char in [".", "-"]:
            self.go_right()
        if self.char == "\\":
            self.go_down()
        if self.char == "/":
            self.go_up()
        if self.char == "|":
            self.go_up()
            self.go_down()

    def from_right(self):
        if "<" in self.lit_from:
            return
        self.lit_from.add("<")
        if self.char in [".", "-"]:
            self.go_left()
        if self.char == "\\":
            self.go_up()
        if self.char == "/":
            self.go_down()
        if self.char == "|":
            self.go_up()
            self.go_down()

    def from_up(self):
        if "v" in self.lit_from:
            return
        self.lit_from.add("v")
        if self.char in [".", "|"]:
            self.go_down()
        if self.char == "\\":
            self.go_right()
        if self.char == "/":
            self.go_left()
        if self.char == "-":
            self.go_left()
            self.go_right()

    def from_down(self):
        if "^" in self.lit_from:
            return
        self.lit_from.add("^")
        if self.char in [".", "|"]:
            self.go_up()
        if self.char == "\\":
            self.go_left()
        if self.char == "/":
            self.go_right()
        if self.char == "-":
            self.go_left()
            self.go_right()

    def go_right(self):
        if self.c + 1 < cols:
            queue.append((table[self.r][self.c + 1], ">"))

    def go_left(self):
        if self.c - 1 >= 0:
            queue.append((table[self.r][self.c - 1], "<"))

    def go_down(self):
        if self.r + 1 < rows:
            queue.append((table[self.r + 1][self.c], "v"))

    def go_up(self):
        if self.r - 1 >= 0:
            queue.append((table[self.r - 1][self.c], "^"))

    def is_lit(self):
        return len(self.lit_from)

    def clear(self):
        self.lit_from = set()

    def __str__(self):
        if self.char != "." or not self.lit_from:
            return self.char
        if len(self.lit_from) > 1:
            return str(len(self.lit_from))
        return list(self.lit_from)[0]


def count_from(spot, dir, clear=False):
    queue.append((spot, dir))
    while queue:
        # print(queue)
        spot, dir = queue.pop(-1)
        if dir == ">":
            spot.from_left()
        elif dir == "<":
            spot.from_right()
        elif dir == "v":
            spot.from_up()
        elif dir == "^":
            spot.from_down()
        else:
            raise Exception(f"unexpected {dir=} at {spot.r=} {spot.c=}")

    count = 0
    for row in table:
        for s in row:
            if s.is_lit():
                count += 1
            if clear:
                s.clear()
        # print(''.join([str(s) for s in row]))

    print(f"{count=}")
    return count


def main():
    filename = "/input"
    if EXAMPLE:
        filename = "/example"
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, "r"), strip=True)
    print(f"input loaded, {len(lines)=}")

    # convert to grid of Spot
    for i, l in enumerate(lines):
        lines[i] = list(Spot(c, i, j) for j, c in enumerate(l))
    table = lines
    rows = len(lines)
    cols = len(lines[0])

    if PART1:
        count = count_from(lines[0][0], ">", clear=True)

    if PART2:
        max_count = 0
        print("From left:")
        for r in range(rows):
            count = count_from(lines[r][0], ">", clear=True)
            max_count = max(max_count, count)
            print(f"{max_count=} {count=}")
        print("From right:")
        for r in range(rows):
            count = count_from(lines[r][-1], "<", clear=True)
            max_count = max(max_count, count)
            print(f"{max_count=} {count=}")
        print("From up:")
        for c in range(cols):
            count = count_from(lines[0][c], "v", clear=True)
            max_count = max(max_count, count)
            print(f"{max_count=} {count=}")
        print("From down:")
        for c in range(cols):
            count = count_from(lines[-1][c], "^", clear=True)
            max_count = max(max_count, count)
            print(f"{max_count=} {count=}")


if __name__ == "__main__":
    main()
