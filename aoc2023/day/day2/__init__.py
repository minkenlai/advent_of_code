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
    else:
        lines = all_lines(open(curr_dir + "/input", "r"), strip=True)
        print(f"{len(lines)=}")

    limits = {"red": 12, "green": 13, "blue": 14}
    sum = 0
    power_sum = 0
    for l in lines:
        print(l)
        game, draws = l.split(": ")
        game = int(game.split(" ")[1])
        draws = draws.split("; ")
        possible = True
        required = {}
        for i, draw in enumerate(draws):
            per_color = draw.split(", ")
            for nc in per_color:
                n, c = nc.split(" ")
                print(f"{game=} {i=} {c=} {n=}")
                if c not in required:
                    required[c] = int(n)
                else:
                    required[c] = max(required[c], int(n))
                if limits[c] < int(n):
                    possible = possible and False
        if possible:
            sum += game
        power = 1
        for v in required.values():
            power = power * v
        power_sum += power
        print(f"{game=} {possible=} {sum=} {required=} {power=} {power_sum=}")


LOG.info(f"done {__name__}")


if __name__ == "__main__":
    main()
