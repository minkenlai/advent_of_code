import sys
from .lib import *


CHECK = [20, 60, 100, 140, 180, 220]

X = 1
CRT: list[str] = []
sum: int = 0
current_line: str = ""
DEBUG = False


def sample() -> list[str]:
    return all_lines(open("aoc2022/inputs/day10-example.txt", "r"))


def debug(str):
    if DEBUG:
        print(str)


def part1(tick: int):
    global sum
    tick += 1
    if tick in CHECK:
        sum += tick * X
    debug(f"{tick=} {X=} {sum=}")
    return tick


def part2(tick: int):
    global current_line, CRT

    def sprite(pos: int) -> str:
        return "#" if pos % 40 in [X - 1, X, X + 1] else "."

    current_line += sprite(tick)
    tick += 1
    if tick % 40 == 0:
        CRT.append(current_line)
        current_line = ""
    debug(f"{tick=} {X=} {current_line=}")
    return tick


def run(source: list[str], do_tick):
    global X, CRT
    tick = 0
    for line in source:
        if line.startswith("noop"):
            tick = do_tick(tick)
            continue
        a, b = line.strip().split(" ")
        if a == "addx":
            tick = do_tick(tick)
            tick = do_tick(tick)
            X += int(b)
        else:
            raise ValueError
        debug(f"{tick=} {X=} {b=} {current_line=}")
    for l in CRT:
        print(l)


if __name__ == "__main__":
    lines = all_lines(get_source())
    run(lines, part1)
    print(f"{sum=}")
    X = 1
    run(lines, part2)

print(f"done {__name__}")
