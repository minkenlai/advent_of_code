import os
import sys

curr_dir = os.path.dirname(__file__)
aoc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(aoc_dir)
print(f"{sys.path=}")

import aoc2023.lib
from aoc2023.lib import all_lines, sample, input, LOG
import functools
import itertools
import logging
import re

EXAMPLE = False
EXAMPLE2 = False
PART1 = True
PART2 = True

day_name = os.path.basename(os.path.dirname(__file__))
day_num = int(day_name[3:]) if day_name.startswith("day") else "unknown"
print(f"{day_name=} {day_num=}")


def parse(lines: list[str]):
    values = {}
    return values


def print_graph(graph):
    for l in graph:
        print(l)


def main():
    if EXAMPLE:
        lines = all_lines(open(curr_dir + "/example", "r"), strip=True)
    elif EXAMPLE2:
        lines = all_lines(open(curr_dir + "/example2", "r"), strip=True)
    else:
        lines = all_lines(open(curr_dir + "/input", "r"), strip=True)
        print(f"{len(lines)=}")

    sum = 0
    for l in lines:
        print(l)
        first = None
        for i, c in enumerate(l):
            if c.isdigit():
                first = c
                break
            ss = l[i:]
            if ss.startswith("one"):
                first = "1"
                break
            if ss.startswith("two"):
                first = "2"
                break
            if ss.startswith("three"):
                first = "3"
                break
            if ss.startswith("four"):
                first = "4"
                break
            if ss.startswith("five"):
                first = "5"
                break
            if ss.startswith("six"):
                first = "6"
                break
            if ss.startswith("seven"):
                first = "7"
                break
            if ss.startswith("eight"):
                first = "8"
                break
            if ss.startswith("nine"):
                first = "9"
                break
        r = reversed(l)
        last = None
        for i, c in enumerate(r):
            if c.isdigit():
                last = c
                break
            ss = l
            if i > 0:
                ss = ss[:-i]
            print(f"{i=} {ss=}")
            if ss.endswith("one"):
                last = "1"
                break
            if ss.endswith("two"):
                last = "2"
                break
            if ss.endswith("three"):
                last = "3"
                break
            if ss.endswith("four"):
                last = "4"
                break
            if ss.endswith("five"):
                last = "5"
                break
            if ss.endswith("six"):
                last = "6"
                break
            if ss.endswith("seven"):
                last = "7"
                break
            if ss.endswith("eight"):
                last = "8"
                break
            if ss.endswith("nine"):
                last = "9"
                break
        v = int(first + last)
        sum += v
        print(f"{v=} {sum=}")


LOG.info(f"done {__name__}")


if __name__ == "__main__":
    main()
