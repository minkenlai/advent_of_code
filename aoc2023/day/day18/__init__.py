import os
import sys
import functools
import itertools
import logging
import numpy as np
import re

curr_dir = os.path.dirname(__file__)
aoc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(aoc_dir)
print(f"{sys.path=}")

import aoc2023.lib
from aoc2023.lib import all_lines, sample, input, LOG

EXAMPLE = 1
PART1 = 0
PART2 = 1

print(
    f"{__file__=} {__name__=} {os.path.basename(__file__)=} {os.path.dirname(__file__)=}"
)
day_name = os.path.basename(__file__)
day_num = None
if not day_name.startswith("day"):
    day_name = os.path.dirname(__file__).split("\\")[-1]
    print(f"last part of dirname: {day_name=}")
if not day_name.startswith("day"):
    day_name = __name__.split(".")[-1]
    print(f"last part of module name: {day_name=}")

if day_name.startswith("day"):
    day_num = int(day_name[3:])
print(f"{day_name=} {day_num=}")


def print_table():
    for r in range(min_r, max_r + 1, 1):
        for c in range(min_c, max_c + 1, 1):
            key = f"{r}_{c}"
            if key in ground:
                print("#", end="")
            else:
                print(".", end="")
        print()


class Color:
    def __init__(self, color):
        self.rgb = color

    def __str__(self):
        return self.rgb

    def __repr__(self):
        return str(self)


class Corner:
    def __init__(self, c):
        self.c = c


step = {
    "R": np.array([0, 1]),
    "L": np.array([0, -1]),
    "D": np.array([1, 0]),
    "U": np.array([-1, 0]),
}
ground = {}
corners = set()
min_r, max_r = 0, 0
min_c, max_c = 0, 0


def current_key(a):
    return f"{a[0]}_{a[1]}"


def dig_trenches():
    global lines, ground, corners, min_c, max_c, min_r, max_r
    current = np.array([0, 0])
    key = current_key(current)
    ground = {key: "()"}  # coord => color
    corners.add(key)
    for l in lines:
        direction, length, color = l.split()
        length = int(length)
        color = Color(color)
        inc = step[direction]
        print(f"{direction=} {length=} {color=}")
        for i in range(length):
            current += inc
            key = f"{current[0]}_{current[1]}"
            print(f"{key=} {color=}")
            ground[key] = color
            min_r = min(min_r, current[0])
            max_r = max(max_r, current[0])
            min_c = min(min_c, current[1])
            max_c = max(max_c, current[1])
        corners.add(key)


def parse_part2(lines):
    dir_map = {"0": ">", "1": "v", "2": "<", "3": "^"}
    current = np.array([0, 0])
    corners = [[0, 0, "#", "#"]]  # row, col, incoming_dir, outgoing_dir
    trench_length = 0
    for l in lines:
        i = l.index("#")
        h = l[i + 1 : i + 6]
        dist = int(h, 16)
        trench_length += dist
        direction = dir_map[l[i + 6]]
        print(f"{dist=} {direction=}")
        if corners:
            corners[-1][3] = direction
        if direction == ">":
            current[1] += dist
        elif direction == "<":
            current[1] -= dist
        elif direction == "v":
            current[0] += dist
        elif direction == "^":
            current[0] -= dist
        else:
            raise Exception(f"unexpected {direction=}")
        corners.append([current[0], current[1], direction, "#"])
    # copy the final outgoing_dir to the head node's incoming_dir
    corners[0][2] = corners.pop(-1)[2]
    print(f"first {corners[0]=} // last {corners[-1]=}")
    print(f"{trench_length=}")
    return corners, trench_length


def polygon_area(x, y):
    n = len(x)
    if n != len(y) or n < 3:
        raise ValueError(
            "Invalid input: The polygon must have at least 3 vertices with matching coordinates."
        )
    area = 0.5 * abs(
        sum(x[i] * y[(i + 1) % n] - x[(i + 1) % n] * y[i] for i in range(n))
    )
    return area


def poly_example():
    # Example usage:
    x_coords = [0, 4, 7, 5]
    y_coords = [0, 0, 3, 4]
    area = polygon_area(x_coords, y_coords)
    print(f"The area of the polygon is: {area}")


def polygon_area_np(x, y):
    # Ensure the arrays are NumPy arrays
    x = np.array(x)
    y = np.array(y)
    n = len(x)
    if n != len(y) or n < 3:
        raise ValueError(
            "Invalid input: The polygon must have at least 3 vertices with matching coordinates."
        )
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return area


def check_lagoon():
    global ground, corners, min_c, max_c, min_r, max_r
    count_ground = 0
    count_hole = 0
    for r in range(min_r, max_r + 1, 1):
        crossed = 0
        for c in range(min_c, max_c + 1, 1):
            key = f"{r}_{c}"
            if key in ground:
                count_hole += 1
                print("#", end="")
                if key not in corners:
                    crossed += 1

            elif in_hole:
                count_hole += 1
                print("#", end="")
            else:
                count_ground += 1
                print(".", end="")
        print()
    print(f"{count_ground=} {count_hole=}")


def flood(ground, r, c) -> int:
    # return number of flooded nodes
    stack = [(r, c)]
    count = 0
    while stack:
        r, c = stack.pop(-1)
        for ir, ic in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr = r + ir
            nc = c + ic
            key = f"{nr}_{nc}"
            if key not in ground:
                ground[key] = "#"
                stack.append((nr, nc))
                count += 1
    return count


def do_part1():
    dig_trenches()
    print(f"{min_r=} {max_r=} {min_c=} {max_c=} {len(ground)=}")

    print_table()
    for i in range(min_c, max_c):
        if f"{min_r}_{i}" in ground:
            start_corner = (min_r, i)
            break

    print(f"{start_corner=}")
    flood_count = flood(ground, start_corner[0] + 1, start_corner[1] + 1)
    print(f"{flood_count=} {flood_count+len(ground)=}")

    print_table()


#    check_lagoon()


def do_part2(lines):
    corners, trench_length = parse_part2(lines)
    x_coords = np.array(list(e[0] for e in corners), dtype=np.int64)
    y_coords = np.array(list(e[1] for e in corners), dtype=np.int64)
    area = polygon_area_np(x_coords, y_coords)
    answer = area + trench_length / 2 + 1
    print(f"{area=} {trench_length=} {answer=}")


def main():
    filename = "input"
    if EXAMPLE:
        filename = "example"
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    curr_dir = os.path.dirname(__file__)
    lines = all_lines(open(os.path.join(curr_dir, filename), "r"), strip=True)
    print(f"input loaded, {len(lines)=}")

    if PART2:
        do_part2(lines)


if __name__ == "__main__":
    main()
