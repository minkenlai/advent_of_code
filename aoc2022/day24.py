from .lib import *
import functools
import itertools
import logging
import re

EXAMPLE = 0
PART1 = 1
PART2 = 1


def to_bits(c: str) -> int:
    if c == "#":
        return 16  # or would 16 work better?
    if c == ".":
        return 0
    if c == ">":
        return 1
    if c == "v":
        return 2
    if c == "<":
        return 4
    if c == "^":
        return 8
    raise ValueError(f"unexpected {c}")


def from_bits(c: int) -> str:
    if c == 0:
        return "."
    if c == 16:
        return "#"
    if c.bit_count() > 1:
        return str(c.bit_count())
    if c & 1:
        return ">"
    if c & 2:
        return "v"
    if c & 4:
        return "<"
    if c & 8:
        return "^"
    raise ValueError(f"unexpected {c}")


def parse(lines: list[str]):
    values = []
    for l in lines:
        r = list(l.rstrip())
        r = [to_bits(c) for c in r]
        values.append(r)
    return values


def print_graph(graph, elves=[(0, 1)]):
    for i, r in enumerate(graph):
        print(
            "".join("E" if (i, j) in elves else from_bits(c) for j, c in enumerate(r))
        )


def advance(graph):
    new_graph = [[0 for c in r] for r in graph]
    assert len(new_graph) == len(graph)
    assert len(new_graph[0]) == len(graph[0])
    for r, row in enumerate(graph):
        new_r = new_graph[r]
        for c, v in enumerate(row):
            LOG.debug(f"({r}, {c}) {v=}")
            if v == 0:
                continue
            if v == 16:
                new_r[c] = v
                continue
            if v & 1:
                # go right
                nc = 1 if c >= max_c - 1 else c + 1
                new_r[nc] |= 1
                LOG.debug(f" . ({r}, {nc}) {v=} -> {new_r[nc]}")
            if v & 2:
                # go down
                nr = 1 if r >= max_r - 1 else r + 1
                new_graph[nr][c] |= 2
                LOG.debug(f" . ({nr}, {c}) {v=} -> {new_graph[nr][c]}")
            if v & 4:
                # go left
                nc = max_c - 1 if c <= 1 else c - 1
                new_r[nc] |= 4
                LOG.debug(f" . ({r}, {nc}) {v=} -> {new_r[nc]}")
            if v & 8:
                # go up
                nr = max_r - 1 if r <= 1 else r - 1
                new_graph[nr][c] |= 8
                LOG.debug(f" . ({nr}, {c}) {v=} -> {new_graph[nr][c]}")
    return new_graph


def candidates(e):
    r, c = e
    if r > 0:
        yield (r - 1, c)
    if r < max_r:
        yield (r + 1, c)
    for i in [c - 1, c, c + 1]:
        if i < max_c and i > 0:
            yield (r, i)


def possible_elves(graph, elves):
    new_elves = set()
    for e in elves:
        for n in candidates(e):
            r, c = n
            if graph[r][c] == 0:
                new_elves.add(n)
                LOG.info(f"{e=} -> {n}")
    return new_elves


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())
    graph = parse(lines)
    max_r = len(graph) - 1
    max_c = len(graph[0]) - 1
    print_graph(graph)

    def how_long(graph, start=(0, 1), end=(max_r, max_c - 1), t=1):
        elves = [start]
        for t in range(t, 30000):
            graph = advance(graph)
            elves = possible_elves(graph, elves)
            if LOG.isEnabledFor(logging.INFO):
                print(f"Minute {t=}")
                print_graph(graph, elves)
            if end in elves:
                break
        print(f"Minute {t=}")
        print_graph(graph, elves)
        return t, graph

    LOG.setLevel(logging.WARN)
    if PART1:
        t, graph = how_long(graph)

    if PART2:
        if not PART1:
            t, graph = how_long(graph)

        t, graph = how_long(graph, start=(max_r, max_c - 1), end=(0, 1), t=t + 1)
        t, graph = how_long(graph, t=t + 1)

LOG.info(f"done {__name__}")
