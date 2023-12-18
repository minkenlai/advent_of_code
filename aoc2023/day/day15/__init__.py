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


def hash(s: str) -> int:
    v = 0
    for c in s:
        if c == "=" or c == "-":
            break
        v = v + ord(c)
        v *= 17
        v %= 256
    return v


def hash_chars(s: str) -> int:
    v = 0
    for c in s:
        if c == "=" or c == "-":
            break
        v = v + ord(c)
        v *= 17
        v %= 256
    return v


class Node:
    def __init__(self, label, lens=None):
        self.label = label
        self.lens = lens
        self.next = None

    def __str__(self):
        return f"[{self.label} {self.lens} {self.next}]"

    def __repr__(self):
        next_label = None if not self.next else self.next.label
        return f"Node({self.label}, {self.lens}, {next_label=})"


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, label, lens=None):
        new_node = Node(label, lens)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        if current.label == label:
            current.lens = lens
            return
        while current.next:
            current = current.next
            if current.label == label:
                current.lens = lens
                return
        current.next = new_node

    def remove(self, label):
        current = self.head
        if not current:
            return
        if current.label == label:
            LOG.info(f"remove head {current=}")
            self.head = current.next
            return
        prev = None
        while current.next:
            prev = current
            current = current.next
            if current.label == label:
                prev.next = current.next
                next_label = "None" if not prev.next else prev.next.label
                LOG.info(
                    f"removed {current.label=} by connecting {prev.label=} to {next_label=}"
                )
                break

    def display(self):
        current = self.head
        while current:
            print(current.label, current.lens, sep=":", end=" -> ")
            current = current.next
        print("None")

    def enumerate(self):
        current = self.head
        i = 0
        while current:
            yield i, current
            i += 1
            current = current.next

    def __str__(self):
        current = self.head
        s = []
        while current:
            s.append(f"[{current.label} {current.lens}]")
            current = current.next
        return " ".join(s)


def part1(values):
    sum = 0
    for v in values:
        h = hash(v)
        sum += h
        print(f"{v=} {h=} {sum=}")
    return sum


def part2(values):
    hm = {}
    for v in values:
        LOG.info(f'after "{v}":')
        h = hash_chars(v)
        if h not in hm:
            hm[h] = LinkedList()
        box = hm[h]
        if "=" in v:
            label, lens = v.split("=")
            box.append(label, int(lens))
        elif v[-1] == "-":
            LOG.info(f"remove {v[:-1]} from {h}")
            box.remove(v[:-1])
        else:
            raise Exception(f"unexpected op in {v=}")
        print(f"box {h}: {box}")

    sum = 0
    for i in range(256):
        if i in hm:
            for j, n in hm[i].enumerate():
                fp = (i + 1) * (j + 1) * n.lens
                print(f"box {i} slot {j} focal {n.lens} {fp=}")
                sum += fp
    print(f"{sum=}")
    return sum


def main():
    filename = "/input"
    if EXAMPLE:
        filename = "/example"
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, "r"), strip=True)
    print(f"input loaded, {len(lines)=}")

    values = lines[0].split(",")
    if PART1:
        part1(values)
    if PART2:
        part2(values)


if __name__ == "__main__":
    main()
