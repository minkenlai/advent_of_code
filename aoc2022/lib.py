import sys
import typing as T

from collections import deque

def ints(value: str, splitter: str = " ") -> list[int]:
    parts = value.strip().split(splitter)
    return [int(v) for v in parts if v]


def convert(value: str, mapping: dict[str, T.Any]):
    return mapping[value]


def all_lines():
    return [v.strip() for v in sys.stdin]


def grouped(source, group_size=3):
    group = []
    i = 0
    for line in source:
        group.append(line.strip())
        i += 1
        if i % group_size == 0:
            yield group
            group = []

def transpose(lines: list[str], cols: int = 0) -> list[deque]:
    cols = cols if cols else len(lines[0])
    new_lines=[deque() for i in range(0, cols)]
    for line in lines:
        for i in range(0, cols):
            new_lines[i].append(line[i])
    return new_lines

def rotate(lines: list[str], cols: int = 0, clockwise: bool=False) -> list[deque]:
    cols = cols if cols else len(lines[0])
    new_lines=[deque() for i in range(0, cols)]
    for line in lines:
        for i in range(0, cols):
            if clockwise:
                new_lines[i].appendleft(line[i])
            else:
                new_lines[cols-1-i].append(line[i])
    return new_lines


if __name__ == "__main__":
    assert ints("1 23 45") == [1, 23, 45]
    print(ints("1 23 45 6  78"))
    lines = all_lines()
    for line in lines:
        print(line)

    print("transpose")
    new_lines = transform_grid(lines, transpose=True)
    for line in new_lines:
        print(line)

    print("clockwise")
    new_lines = transform_grid(lines, clockwise=True)
    for line in new_lines:
        print(line)

    print("anti-clockwise")
    new_lines = transform_grid(lines, clockwise=False)
    for line in new_lines:
        print(line)

print(f"done {__name__}")