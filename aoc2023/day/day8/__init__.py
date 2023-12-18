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

EXAMPLE = 2
PART1 = 1
PART2 = 1

day_name = os.path.basename(os.path.dirname(__file__))
day_num = int(day_name[3:]) if day_name.startswith("day") else "unknown"
print(f"{day_name=} {day_num=}")

pattern = "[A-Z0-9]{3}"


def prime_factors(number):
    factors = []
    divisor = 2
    while divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)
            number = number // divisor
        else:
            divisor += 1
    if not factors:
        factors.append(number)
    return factors


class Node:
    def __init__(self, line):
        self.name, self.left, self.right = re.findall(pattern, line)
        if PART1:
            self.is_end = self.name == "ZZZ"
        if PART2:
            self.is_end = self.name.endswith("Z")

    def __str__(self):
        return f"{self.name}=({self.left},{self.right})"

    def __repr__(self):
        return str(self)


def main():
    filename = "/input"
    if EXAMPLE:
        filename = "/example"
        if EXAMPLE > 1:
            filename = filename + str(EXAMPLE)
    lines = all_lines(open(curr_dir + filename, "r"), strip=True)
    print(f"Loaded: {filename=} {len(lines)=}")

    nodes = {}
    for l in lines[2:]:
        node = Node(l)
        nodes[node.name] = node
    # print(nodes)

    def steps_until_end(start):
        n = start
        steps = 0
        while not n.is_end:
            for i in lines[0]:
                steps += 1
                if i == "L":
                    n = nodes[n.left]
                elif i == "R":
                    n = nodes[n.right]
                print(f"{steps=} {i=} {n=}")
                if n.is_end:
                    break
        print(f"{start=} {steps=} {n=}")
        return steps

    if PART1 and EXAMPLE < 3:
        steps_until_end(nodes["AAA"])

    if PART2 or (PART1 and EXAMPLE == 3):
        positions = list(n for n in nodes.values() if n.name.endswith("A"))
        print(f"{positions=}")
        steps = list(steps_until_end(n) for n in positions)
        print(f"{steps=}")

    if PART2:
        factors = set()
        for v in steps:
            for f in prime_factors(v):
                factors.add(f)
        print(f"{factors=}")
        total = 1
        for f in factors:
            total *= f
        print(f"{total=}")

    # bruteforce
    if False:
        positions = list(n for n in nodes.values() if n.name.endswith("A"))
        print(f"{positions=}")
        steps = 0

        def all_end(positions):
            for n in positions:
                if not n.is_end:
                    return False
            return True

        while not all_end(positions):
            for i in lines[0]:
                steps += 1
                for j, n in enumerate(positions):
                    if i == "L":
                        n = nodes[n.left]
                    elif i == "R":
                        n = nodes[n.right]
                    positions[j] = n
                if all_end(positions):
                    break
                if not (steps - 1) % 100:
                    print(f"{steps=} {positions=}")
        print(f"{steps=} {positions=}")


if __name__ == "__main__":
    main()
