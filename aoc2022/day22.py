from .lib import *
import functools
import itertools
import logging
import re

max_x = 0
max_y = 0


def parse(lines: list[str]) -> tuple[list[str], list[int], list[int]]:
    global max_x, max_y
    land = []
    land_complete = 0
    steps = []
    turns = []
    for l in lines:
        if not l.strip():
            land_complete = 1
            LOG.info(f"completed reading {len(land)} lines for land")
            continue
        if not land_complete:
            max_y += 1
            l = l.rstrip()
            max_x = max(max_x, len(l))
            land.append(l)
            continue
        l = l.strip()
        steps = [int(v) for v in re.compile("[0-9]+").findall(l)]
        turns = [1 if c == "R" else -1 for c in re.compile("[LR]").findall(l)]
        LOG.info(f"found {len(steps)} steps and {len(turns)} turns")
        # add final no-op turn to make lengths match
        turns.append(0)
        LOG.debug(steps)
        LOG.debug(turns)
    return land, steps, turns


def print_graph(graph):
    for l in graph:
        if isinstance(l, list):
            s = ""
            for c in l:
                s = s + c
            l = s
        print(l)


def trans(d: int):
    if d == 0:
        return (0, 1)
    elif d == 1:
        return (1, 0)
    elif d == 2:
        return (0, -1)
    elif d == 3:
        return (-1, 0)
    raise ValueError


def is_wall(r, c, dr, dc) -> tuple[bool, int, int]:
    while not dc:
        r += dr
        LOG.debug(f"{r=} {c=}")
        if r < 0:
            r = max_y - 1
        elif r >= max_y:
            r = 0
        if c < len(land[r]) and c >= 0 and land[r][c] != " ":
            break
    while not dr:
        c += dc
        if c < 0:
            c = len(land[r]) - 1
        elif c >= len(land[r]):
            c = 0
        LOG.debug(f"{r=} {c=} {len(land[r])=} {land[r][c]=}")
        if c < len(land[r]) and c >= 0 and land[r][c] != " ":
            break
    return land[r][c] == "#", r, c


def get_char(d):
    if d == 0:
        return ">"
    if d == 1:
        return "v"
    if d == 2:
        return "<"
    if d == 3:
        return "^"
    raise ValueError


def part1(land, steps, turns) -> tuple[int, int, int]:
    r = 0
    c = land[r].index(".")
    d = 0  # direction 0 is EAST, each +1 is 90 degrees
    for s, t in zip(steps, turns, strict=True):
        dr, dc = trans(d)
        LOG.info(f"{r=} {c=} {dr=} {dc=} facing {d} going {s=}")
        for i in range(s):
            wall, nr, nc = is_wall(r, c, dr, dc)
            if wall:
                break
            row = list(land[r])
            row[c] = get_char(d)
            land[r] = row
            r = nr
            c = nc
        d += t
        d %= 4
    LOG.info(f"End @ {r=} {c=} facing {d=}")
    return r, c, d


EXAMPLE = 0
PART1 = 1
PART2 = 0
LOG.setLevel(logging.DEBUG)

if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())
    land, steps, turns = parse(lines)

    # print_graph()
    if PART1:
        LOG.info("===== part 1 =====")
        r, c, d = part1(land, steps, turns)
        print_graph(land)
        print(f"Part 1 results {(r+1)*1000 + (c+1)*4 + d}")

    if PART2:
        LOG.info("===== part 2 =====")

LOG.info(f"done {__name__}")
