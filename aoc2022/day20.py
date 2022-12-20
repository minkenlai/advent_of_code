from .lib import *
import functools
import itertools
import logging
import re

EXAMPLE = 0
PART1 = 0
PART2 = 1


def parse(lines: list[str]):
    values = []
    for l in lines:
        values.append(int(l))
    return values


def print_graph(graph):
    for l in graph:
        print(l)


class Node:
    def __init__(self, val: int, p: "Node", n: "Node"):
        self.val = val
        self.op = p
        self.on = n
        self.p = p
        self.n = n

    def mix(self):
        if self.val == 0:
            return
        s = self
        n = self.n
        p = self.p
        # traverse to new spot
        assert length == len(ls)
        if self.val > 0:
            val = self.val % (length - 1)
            c = n
            LOG.debug(f"forward to {c=}")
            for _ in range(1, val):
                c = c.n
                LOG.debug(f"forward to {c=}")
            n = c.n
            p = c
        elif self.val < 0:
            val = abs(self.val) % (length - 1)
            c = p
            LOG.debug(f"back to {c=}")
            for _ in range(1, val):
                c = c.p
                LOG.debug(f"back to {c=}")
            p = c.p
            n = c
        # remove self from previous spot
        LOG.debug(f"removing {s=} between {self.p=} and {self.n=}")
        self.n.p = self.p
        self.p.n = self.n
        # insert self at new spot
        LOG.debug(f"inserting {s=} between {p=} and {n=}")
        p.n = s
        s.n = n
        n.p = s
        s.p = p

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return f"Node({self.val}, p={self.p}, n={self.n})"


def convert_to_nodes(key=1):
    global ls, length
    length = len(ls)
    prev = None
    for i in range(length):
        ls[i] = Node(ls[i] * key, prev, None)
        prev = ls[i]
    ls[0].p = ls[-1]
    for i in range(length - 1):
        assert ls[i].p
        ls[i].n = ls[i + 1]
    ls[length - 1].n = ls[0]
    assert len(ls) == length


def print_list():
    c = ls[0]
    s = ""
    for _ in range(len(ls)):
        s += str(c.val) + ", "
        c = c.n
    print(s)


def get_answers():
    c = z
    count = 0
    sum = 0
    for _ in range(1000):
        c = c.n
        count += 1
    print(f"After {count}, {c.val=} {c.p.val=} {c.n.val=}")
    sum += c.val
    for _ in range(1000):
        c = c.n
        count += 1
    print(f"After {count}, {c.val=} {c.p.val=} {c.n.val=}")
    sum += c.val
    for _ in range(1000):
        c = c.n
        count += 1
    print(f"After {count}, {c.val=} {c.p.val=} {c.n.val=}")
    sum += c.val
    print(f"{sum=}")
    return sum


z = None


def part1():
    global z
    for n in ls:
        n.mix()
        if n.val == 0:
            z = n
        if LOG.isEnabledFor(logging.DEBUG):
            print_list()
    get_answers()


def part2():
    assert not PART1
    for _ in range(10):
        part1()
    get_answers()


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())
    ls = parse(lines)
    LOG.setLevel(logging.INFO)

    if PART1:
        convert_to_nodes()
        part1()
    if PART2:
        convert_to_nodes(key=811589153)
        part2()


LOG.info(f"done {__name__}")
