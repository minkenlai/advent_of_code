"""convenience library for Advent of Code"""
import importlib
import sys
import typing as T

from collections import deque


def get_source():
    if len(sys.argv) > 1:
        print(f"input file: {sys.argv[1]=}")
        return open(sys.argv[1], "r")
    return sys.stdin


def all_lines(source=sys.stdin):
    return [v.strip() for v in source]


def reload(mod):
    return importlib.reload(mod)


def ints(value: str, splitter: str = " ") -> list[int]:
    parts = value.strip().split(splitter)
    return [int(v) for v in parts if v]


def convert(value: str, mapping: dict[str, T.Any]):
    return mapping[value]


def grouped(lines, group_size=3):
    group = []
    i = 0
    for line in lines:
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


def has_repeat(buffer: T.Union[list, str]):
    s = set()
    for c in buffer:
        s.add(c)
    print(f"{s=} {buffer=}")
    return len(s) < len(buffer)


def ranges_disjoint(a: tuple[int, int], b: tuple[int, int]):
    return a[1] < b[0] or a[0] > b[1]


def ranges_overlap(a: tuple[int, int], b: tuple[int, int]):
    return not ranges_disjoint(a, b)


def merge_ranges(
    ranges: list[tuple[int, int]],
    new_range: T.Optional[tuple[int, int]],
    merge_adj=True,
) -> list[tuple[int, int]]:
    """ranges must be sorted in ascending order, the new_range will be inserted with any overlaps merged"""
    new_ranges = []
    merge_adj = 1 if merge_adj else 0
    for existing_range in ranges:
        if not new_range or existing_range[1] < new_range[0] - merge_adj:
            new_ranges.append(existing_range)
        elif new_range and existing_range[0] > new_range[1] + merge_adj:
            new_ranges.append(new_range)
            new_range = None
            new_ranges.append(existing_range)
        else:
            # print(f"merge {existing_range=} and {new_range=}")
            new_range = (
                min(existing_range[0], new_range[0]),
                max(existing_range[1], new_range[1]),
            )
            # print(f"got {new_range=}")
    if new_range is not None:
        new_ranges.append(new_range)
    # print(f"{new_ranges=}")
    return new_ranges


def sort_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """ranges may have overlaps and unordered, the result will be sorted and merged"""
    new_ranges = []
    for existing_range in ranges:
        new_ranges = merge_ranges(new_ranges, existing_range)
    return new_ranges


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
