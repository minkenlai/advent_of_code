import sys
from .lib import *


def value_of(x) -> int:
    return x


def score(a, b) -> int:
    x, y = a.split("-")
    w, z = b.split("-")
    if (int(x) <= int(w) and int(z) <= int(y)) or (
        int(w) <= int(x) and int(y) <= int(z)
    ):
        return 1
    return 0


def any_b_in_a(a, b) -> int:
    x, y = a.split("-")
    w, z = b.split("-")
    if int(x) <= int(w) and int(w) <= int(y):
        return 1
    if int(x) <= int(z) and int(z) <= int(y):
        return 1
    return 0


def no_overlap(a, b) -> int:
    x, y = list(map(int, a.split("-")))
    w, z = list(map(int, b.split("-")))
    if y < w or z < x:
        return 1
    return 0


def run(source):
    sum = 0
    distinct = 0
    total = 0
    for line in source:
        a, b = line.strip().split(",")
        print(f"{a=} {b=}")
        if any_b_in_a(a, b) or any_b_in_a(b, a):
            sum += 1
        if no_overlap(a, b):
            distinct += 1
        total += 1
        print(f"{sum=} {distinct=} {total=}")


if __name__ == "__main__":

    run(sys.stdin)

print(f"done {__name__}")
