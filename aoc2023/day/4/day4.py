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

EXAMPLE = 0
EXAMPLE2 = 0
PART1 = True
PART2 = True

day_name = os.path.basename(__file__)
day_num = re.search(r"\d+", day_name).group()
print(f"{day_name=} {day_num=}")

def run():
    if PART2:
        card_counts = [1] * len(lines)
        print(card_counts)
    sum = 0
    sum2 = 0
    for i, l in enumerate(lines):
        print(l)
        card, nums = l.split(': ')
        winners, nums = nums.split(' | ')
        winners = winners.split()
        nums = nums.split()
        inter = set(winners).intersection(set(nums))
        if PART2:
            for j in range(len(inter)):
                card_counts[i + j + 1] += card_counts[i]
            sum2 += card_counts[i]
        if inter:
            sum += 2 ** (len(inter) - 1)
        print(f"{i=} {card=} {winners=} {nums=} {inter=} {sum=}")
        if PART2:
            print(f"{i=} {card_counts=} {sum2=}")


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(open(curr_dir + '/example', 'r'), strip=True)
    elif EXAMPLE2:
        lines = all_lines(open(curr_dir + '/example2', 'r'), strip=True)
    else:
        lines = all_lines(open(curr_dir + '/input', 'r'), strip=True)
    print(f"{len(lines)=}")

    run()