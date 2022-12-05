import sys
from .lib import *

RPS = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1,
    "Y": 2,
    "Z": 3,
}

map_to_mine = {
    "X": -1,
    "Y": 0,
    "Z": +1,
}


def points_of(val) -> int:
    return (val % 3) or 3


def score1(a, b):
    x = convert(a, RPS)
    y = convert(b, RPS)
    v = points_of(y)
    if (y - x) % 3 == 1:
        v += 6
    elif (y - x) % 3 == 0:
        v += 3
    print(f"{x=} {y=} {v=}")
    return v


def score2(a, b):
    x = convert(a, RPS)
    y = x + map_to_mine[b]
    v = points_of(y)
    if (y - x) % 3 == 1:
        v += 6
    elif (y - x) % 3 == 0:
        v += 3
    print(f"{x=} {y=} {v=}")
    return v


def run():
    sum1 = 0
    sum2 = 0
    for line in sys.stdin:
        a, b = line.strip().split(" ")
        print(f"{a=} {b=}")
        sum1 += score1(a, b)
        sum2 += score2(a, b)
        print(f"{sum1=} {sum2=}")


if __name__ == "__main__":
    assert convert("A", RPS) == 1
    assert convert("C", RPS) == 3
    assert convert("X", RPS) == 1
    assert convert("Z", RPS) == 3
    run()

print(f"done {__name__}")
