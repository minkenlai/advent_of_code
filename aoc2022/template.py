from .lib import *
import functools
import itertools
import logging
import re

EXAMPLE = True
PART1 = True
PART2 = True


def parse(lines: list[str]):
    values = {}
    return values


def print_graph(graph):
    for l in graph:
        print(l)


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())
    # print_graph()

    if PART1:
        lowest = None
        highest = None
        ranges = []
        count = 0
        LOG.info(f"{ranges=}")
        for r in ranges:
            count += r[1] - r[0] + 1
        print(f"{count=}")

    if PART2:
        pass

LOG.info(f"done {__name__}")
