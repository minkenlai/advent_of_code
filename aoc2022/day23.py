from .lib import *
import functools
import itertools
import logging
import re

EXAMPLE = 0
PART1 = True
PART2 = True

search_pattern = [
    [(-1, 0), (-1, 1), (-1, -1)],
    [(1, 0), (1, 1), (1, -1)],
    [(0, -1), (-1, -1), (1, -1)],
    [(0, 1), (-1, 1), (1, 1)],
]


def parse(lines: list[str]) -> set[tuple[int, int]]:
    values: set[tuple[int, int]] = set()
    for r, l in enumerate(lines):
        for c, e in enumerate(l):
            if e == "#":
                values.add((r, c))
    return values


def print_graph(vals):
    LOG.info(f"{min_r=}, {max_r=}, {min_c=}, {max_c=}")
    for r in range(min(0, min_r), max_r + 1):
        s = ""
        for c in range(min(0, min_c), max_c + 1):
            if (r, c) in vals:
                s += "#"
            else:
                s += "."
        print(s)


def do_round(vals: set[tuple[int, int]]) -> set[tuple[int, int]]:
    global min_r, max_r, min_c, max_c, search_pattern
    proposals: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for r, c in vals:
        pro = None
        n = 0
        # check each Cardinal Direction
        for cd in search_pattern:
            blocked = 0
            # check 3 adjacent
            for d in cd:
                dr, dc = d
                nr, nc = r + dr, c + dc
                if (nr, nc) in vals:
                    blocked += 1
                    LOG.debug(f"{(r, c)} saw {(nr, nc)} so cannot go {d}")
                    break
            if blocked:
                n += 1
            else:
                if not pro:
                    pro = (r + cd[0][0], c + cd[0][1])
        if pro and n > 0:
            LOG.debug(f"{(r, c)} proposes {pro}")
            if pro in proposals:
                proposals[pro].append((r, c))
            else:
                proposals[pro] = [(r, c)]
        elif n == 0:
            LOG.debug(f"{(r, c)} has no neighbors and stays")
            proposals[(r, c)] = [(r, c)]
        else:
            LOG.debug(f"{(r, c)} is blocked on all sides and stays")
            proposals[(r, c)] = [(r, c)]
    search_pattern = search_pattern[1:] + search_pattern[:1]
    LOG.debug(search_pattern)
    new_vals = set()
    for s, l in proposals.items():
        if len(l) > 1:
            for e in l:
                new_vals.add(e)
        else:
            new_vals.add(s)
            min_r, max_r, min_c, max_c = (
                min(min_r, s[0]),
                max(max_r, s[0]),
                min(min_c, s[1]),
                max(max_c, s[1]),
            )
    return new_vals


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())
    vals = parse(lines)
    min_r, max_r, min_c, max_c = len(lines), 0, len(lines[0]), 0
    print_graph(vals)
    LOG.info(f"parsed {len(vals)} elves")

    new_vals = vals
    if PART1:
        # LOG.setLevel(logging.DEBUG)
        for count in range(10):
            # breakpoint()
            new_vals = do_round(new_vals)
            assert len(vals) == len(new_vals)
            # LOG.info(f"{count=}: {min_r=}, {max_r=}, {min_c=}, {max_c=}")
            if LOG.isEnabledFor(logging.INFO):
                print(f"== End of Round {count + 1} ==")
                print_graph(new_vals)
        spaces = (max_r - min_r + 1) * (max_c - min_c + 1) - len(vals)
        print(f"empty {spaces=}")

    if PART2:
        if not PART1:
            raise ValueError
        LOG.setLevel(logging.WARNING)
        count = 10
        while True:
            count += 1
            next_vals = do_round(new_vals)
            if not (next_vals ^ new_vals):
                break
            new_vals = next_vals
            if count == 100:
                print(100)
            if count % 200 == 0:
                print(count)
        print(f"final {count=}")

LOG.info(f"done {__name__}")
