import sys
from .lib import *


def value_of(x) -> int:
    return x


def score(v) -> int:
    return ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ").index(v) + 1


def run(source):
    sum = 0
    for line in source:
        l = line.strip()
        h = int(len(l) / 2)
        a = l[0:h]
        b = l[h:]
        print(f"{a=} {b=}")
        f = []
        for c in a:
            if c in b and c not in f:
                sum += score(c)
                print(f"  {c=} {sum=}")
                f.append(c)


def run2(source):
    sum = 0
    for a, b, c in grouped(source):
        print(f"{a=} {b=} {c=}")
        for v in a:
            if v in b and v in c:
                sum += score(v)
                print(f"  {v=} {sum=}")
                break
    return sum


if __name__ == "__main__":
    assert score("a") == 1
    assert score("Z") == 52
    lines = all_lines(get_source())
    run(lines)
    run2(lines)

print(f"done {__name__}")
