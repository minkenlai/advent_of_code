import sys
import typing as T

from collections import deque


def ints(value: str, splitter: str = " ") -> list[int]:
    parts = value.strip().split(splitter)
    return [int(v) for v in parts if v]


def convert(value: str, mapping: dict[str, T.Any]):
    return mapping[value]


def all_lines(source=sys.stdin):
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


def transpose(lines: T.Union[list[str], list[list]], cols: int = 0) -> list[deque]:
    cols = cols if cols else len(lines[0])
    new_lines = [deque() for i in range(0, cols)]
    for line in lines:
        for i in range(0, cols):
            new_lines[i].append(line[i])
    return new_lines


def rotate(
    lines: T.Union[list[str], list[list]], cols: int = 0, clockwise: bool = False
) -> list[deque]:
    cols = cols if cols else len(lines[0])
    new_lines = [deque() for i in range(0, cols)]
    for line in lines:
        for i in range(0, cols):
            if clockwise:
                new_lines[i].appendleft(line[i])
            else:
                new_lines[cols - 1 - i].append(line[i])
    return new_lines


def has_repeat(buffer):
    s = set()
    for c in buffer:
        s.add(c)
    print(f"{s=} {buffer=}")
    return len(s) < len(buffer)


if __name__ == "__main__":
    assert ints("1 23 45") == [1, 23, 45]
    print(ints("1 23 45 6  78"))
    lines = all_lines()
    for line in lines:
        print(line)

    print("transpose")
    transposed_lines = transpose(lines)
    for line in transposed_lines:
        print(line)

    print("anti-clockwise")
    new_lines = rotate(lines, clockwise=False)
    for i, line in enumerate(new_lines):
        print(line)
        # same as transposed then lines reversed
        assert line == transposed_lines[len(new_lines) - 1 - i]

    print("clockwise")
    new_lines = rotate(lines, clockwise=True)
    for i, line in enumerate(new_lines):
        print(line)
        # same as transposed then lines reversed-within
        line.reverse()
        assert line == transposed_lines[i]

    # try with number lists
    num_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    new_lists = transpose(num_lists)
    for i, line in enumerate(new_lists):
        print(line)
    new_lists = rotate(num_lists, clockwise=True)
    for i, line in enumerate(new_lists):
        print(line)


print(f"done {__name__}")
