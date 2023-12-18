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

EXAMPLE = 1
PART1 = 1
PART2 = 1

day_name = os.path.basename(__file__)
day_num = re.search(r"\d+", day_name).group()
print(f"{day_name=} {day_num=}")


if __name__ == "__main__":
    filename = "/input"
    if EXAMPLE:
        filename = "/example"
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, "r"), strip=True)
    print(f"input loaded, {len(lines)=}")
