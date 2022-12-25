from .lib import *
import functools
import itertools
import logging
import re

EXAMPLE = 0
PART1 = True
PART2 = True

max_digits = 0


def parse(lines: list[str]):
    global max_digits
    values = []
    for l in lines:
        max_digits = max(max_digits, len(l))
        l = list(l)
        l.reverse()
        values.append(l)
    return values


def print_graph(graph):
    for l in graph:
        print(l)


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample(), strip=True)
    else:
        lines = all_lines(input(), strip=True)
    values = parse(lines)
    print(f"parsed {len(values)} with {max_digits=}")

    def val_of(d) -> int:
        if d == "=":
            return -2
        if d == "-":
            return -1
        return int(d)

    if PART1:
        sums = [0 for _ in range(max_digits)]
        for v in values:
            for i, d in enumerate(v):
                sums[i] += val_of(d)
        LOG.info(f"sums (lowest to highest): {sums}")

        def to_decimal(sums):
            value = 0
            for i, d in enumerate(sums):
                v = d * 5**i
                value += v
                LOG.debug(f"{i}: {v=} {value=}")
            return value

        LOG.setLevel(logging.DEBUG)
        dec = to_decimal(sums)
        LOG.info(f"decimal value = {dec}")

        s = ""
        carry = 0
        for i, d in enumerate(sums):
            d += carry
            carry = 0
            if d > 0:
                carry = int(d / 5)
                d = d % 5
            if d < 0:
                carry = -int(abs(d) / 5)
                d = -(abs(d) % 5)
            if d == 4:
                carry += 1
                c = "-"
            elif d == 3:
                carry += 1
                c = "="
            elif d == -4:
                carry -= 1
                c = "1"
            elif d == -3:
                carry -= 1
                c = "2"
            elif d == -1:
                c = "-"
            elif d == -2:
                c = "="
            else:
                c = str(d)
            s = c + s
            LOG.info(f"{i}: {d=} {carry=} {c=} {s=}")

    if PART2:
        pass

LOG.info(f"done {__name__}")
