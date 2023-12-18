import os
import sys
import functools
import itertools
import logging
import re
import heapq
from sortedcontainers import SortedList

curr_dir = os.path.dirname(__file__)
aoc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(aoc_dir)
print(f"{sys.path=}")

import aoc2023.lib
from aoc2023.lib import all_lines, sample, input, LOG

EXAMPLE = 0
EXAMPLE2 = 0
PART1 = 1
PART2 = 1

day_name = os.path.basename(os.path.dirname(__file__))
day_num = int(day_name[3:]) if day_name.startswith("day") else "unknown"
print(f"{day_name=} {day_num=}")

card_mapping = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

if PART2:
    card_mapping["J"] = 1


class Hand:
    def __init__(self, line: str):
        deal, bid = line.split()
        self.cards = []
        self.bid = int(bid)
        by_card = {}
        wilds = 0
        for c in deal:
            if c.isdigit():
                v = int(c)
            else:
                v = card_mapping[c]
            self.cards.append(v)
            if v == 1:  # PART2 J is wild but has lowest individual value
                wilds += 1
            elif v in by_card:
                by_card[v] += 1
            else:
                by_card[v] = 1
        self.sets = list(sorted(by_card.values(), reverse=True))
        if self.sets:
            self.sets[0] += wilds
        else:
            self.sets = [wilds]

    def __lt__(self, other: "Hand"):
        if self.sets > other.sets:
            return False
        elif self.sets < other.sets:
            return True
        for i in range(5):
            if self.cards[i] > other.cards[i]:
                return False
            elif self.cards[i] < other.cards[i]:
                return True
        raise Exception(f"two hands are equal? {self.cards=} {other.cards=}")

    def __str__(self):
        return f"{self.sets=} {self.cards=}"

    def __repr__(self):
        return str(self)


def main():
    if EXAMPLE:
        lines = all_lines(open(curr_dir + "/example", "r"), strip=True)
    elif EXAMPLE2:
        lines = all_lines(open(curr_dir + "/example2", "r"), strip=True)
    else:
        lines = all_lines(open(curr_dir + "/input", "r"), strip=True)
    print(f"input loaded, {len(lines)=}")

    all_hands = [Hand(l) for l in lines]
    heapq.heapify(all_hands)
    i = 0
    sum = 0
    while all_hands:
        i += 1
        min_val = heapq.heappop(all_hands)
        sum = sum + i * min_val.bid
        print(f"{i=} {min_val=} {sum=}")


if __name__ == "__main__":
    main()
