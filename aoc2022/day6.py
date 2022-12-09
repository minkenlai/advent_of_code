import sys
from .lib import *


def value_of(x) -> int:
    return x


def score(a, b) -> int:
    return a + b


def run(lines):
    print(len(lines))
    print(len(lines[0]))
    sum = 0
    buffer = deque()
    i = 0
    for c in lines[0]:
        i += 1
        buffer.append(c)
        if len(buffer) < 14:
            continue
        if len(buffer) > 14:
            buffer.popleft()
        print(f"{buffer=}")
        if not has_repeat(buffer):
            print(f"found {buffer=} at {i=}")
            return i


if __name__ == "__main__":
    # run(["bvwbjplbgvbhsrlpgdmjqwftvncz"])
    run(all_lines(get_source()))

print(f"done {__name__}")
