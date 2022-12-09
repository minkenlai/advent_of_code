import sys
from .lib import *


def value_of(x) -> int:
    return x


def score(a, b) -> int:
    return a + b


def run(source):
    sum = 0
    for line in source:
        a, b = line.strip().split(" ")
        print(f"{a=} {b=}")
        sum += score(a, b)
        print(f"{sum=}")


def load_stacks() -> list[list[str]]:
    stacks = [list()]
    for line in open(
        "/Users/mlai/dev/minkenlai/aoc/aoc2022/inputs/day5-start.txt", "r"
    ):
        stacks.append(line.strip().split(","))
    print(stacks)
    return stacks


def move(stacks, count, src, des):
    print(f"move {count=} from {src=} to {des=}")
    i = 0
    items = []
    while i < count:
        items.append(stacks[src][-1])
        stacks[src] = stacks[src][:-1]
        i += 1
    i = count - 1
    while i >= 0:
        stacks[des].append(items[i])
        i -= 1
    print(f"{src=} {stacks[src]=}")
    print(f"{des=} {stacks[des]=}")


def pop_end(ls):
    last = ls[-1]
    del ls[-1]
    return last


def original(source=sys.stdin):
    input = """
    [C]             [L]         [T]
    [V] [R] [M]     [T]         [B]
    [F] [G] [H] [Q] [Q]         [H]
    [W] [L] [P] [V] [M] [V]     [F]
    [P] [C] [W] [S] [Z] [B] [S] [P]
[G] [R] [M] [B] [F] [J] [S] [Z] [D]
[J] [L] [P] [F] [C] [H] [F] [J] [C]
[Z] [Q] [F] [L] [G] [W] [H] [F] [M]
 1   2   3   4   5   6   7   8   9

"""
    print(input)


if __name__ == "__main__":
    # original()
    stacks = load_stacks()

    # run(sys.stdin)
    for line in get_source():
        _, count, _, src, _, des = line.strip().split(" ")
        move(stacks, int(count), int(src), int(des))
    for stack in stacks:
        print(stack)

print(f"done {__name__}")
