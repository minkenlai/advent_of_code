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
EXAMPLE2 = False
PART1 = True
PART2 = True

day_name = os.path.basename(os.path.dirname(__file__))
day_num = int(day_name[3:]) if day_name.startswith("day") else "unknown"
print(f"{day_name=} {day_num=}")


class Map:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def add(self, src, dest, length):
        self.lines.append([src, dest, length])

    def print(self):
        print(f"{self.name}")
        for l in lines:
            print(l)

    def map(self, src):
        for l in self.lines:
            if src >= l[0]:
                i = src - l[0]
                if i < l[2]:
                    return l[1] + i
        return src

    def map_ranges(self, src):
        # input is a list of ranges [[start, length], ...]
        # output should be a sorted list of ranges
        dst = []
        while len(src):
            sr = sorted(src)[0]
            src.remove(sr)
            range_start, range_len = sr
            range_end = range_start + range_len  # non-inclusive
            print(f"{range_start=} {range_end=}   {range_len=}")
            touched = False
            for l in self.lines:
                # look for overlap and turn that into a new range
                m_src, m_dst, m_len = l
                m_end = m_src + m_len  # non-inclusive
                print(f"{m_src=} {m_end=} -> {m_dst=}")
                if range_end <= m_src:
                    continue
                if range_start >= m_end:
                    continue
                if range_start < m_src:
                    src.append([range_start, m_src - range_start])
                    print(f"before={src[-1]}")
                if range_end > m_end:
                    src.append([m_end, range_end - m_end])
                    print(f"after={src[-1]}")
                move_start = max(range_start, m_src)
                move_end = min(range_end, m_end)
                dst.append([m_dst + move_start - m_src, move_end - move_start])
                print(f"moved={dst[-1]}")
                touched = True
                break
            if not touched:
                print(f"untouched={sr}")
                dst.append(sr)
        return self.merged_ranges(dst)

    def merged_ranges(self, range_list):
        # input is a list of ranges [[start, length], ...]
        range_list = sorted(range_list)
        print(f"{range_list=}")
        results = [range_list[0]]
        for r in range_list[1:]:
            prev = results[-1]
            prev_end = prev[0] + prev[1]
            if r[0] < prev_end:
                new_end = r[0] + r[1]
                if prev_end < new_end:
                    results[-1][1] = new_end - prev[0]
            else:
                results.append(r)
        print(f"{results=}")
        return results


def expand_seeds(seeds):
    for i in range(int(len(seeds) / 2)):
        start = seeds[2 * i]
        length = seeds[2 * i + 1]
        for j in range(length):
            yield start + j


def run(lines):
    section = -1
    seeds = []
    maps = []
    for l in lines:
        if len(l) == 0:
            section += 1
        elif section < 0:
            seeds = l.split()[1:]
            seeds = list(int(s) for s in seeds)
            if PART2 and EXAMPLE:
                # seeds = expand_seeds(seeds)
                pass
            if PART2:
                seed_ranges = []
                for i in range(0, len(seeds), 2):
                    seed_ranges.append([seeds[i], seeds[i + 1]])
        else:
            if "map" in l:
                maps.append(Map(l))
            else:
                src, dest, length = l.split()
                maps[section].add(int(dest), int(src), int(length))

    print(f"{seeds=}")
    lowest = None
    if PART1:
        for seed in seeds:
            val = seed
            for m in maps:
                # m.print()
                val = m.map(val)
                print(f"{m.name=} {val=}")
            if not lowest or val < lowest:
                lowest = val
            print(f"{lowest=}")
    if PART2:
        val = seed_ranges
        for m in maps:
            val = m.map_ranges(val)
        print(f"{val[0]=}")


def main():
    if EXAMPLE:
        lines = all_lines(open(curr_dir + "/example", "r"), strip=True)
    elif EXAMPLE2:
        lines = all_lines(open(curr_dir + "/example2", "r"), strip=True)
    else:
        lines = all_lines(open(curr_dir + "/input", "r"), strip=True)
    print(f"{len(lines)=}")

    run(lines)


if __name__ == "__main__":
    main()
