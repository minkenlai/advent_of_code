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


if __name__ == "__main__":
    run(all_lines(get_source()))

print(f"done {__name__}")
