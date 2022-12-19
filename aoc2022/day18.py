from .lib import *
import datetime
import functools
import itertools
import logging
import re

example = [
    2,
    2,
    2,
    1,
    2,
    2,
    3,
    2,
    2,
    2,
    1,
    2,
    2,
    3,
    2,
    2,
    2,
    1,
    2,
    2,
    3,
    2,
    2,
    4,
    2,
    2,
    6,
    1,
    2,
    5,
    3,
    2,
    5,
    2,
    1,
    5,
    2,
    3,
    5,
]


def adj(a, b):
    dist = sum(abs(a[i] - b[i]) for i in range(3))
    return dist == 1


droplets = set()


def load_example():
    numdrips = int(len(example) / 3)
    for i in range(numdrips):
        j = 3 * i
        droplets.add((example[j], example[j + 1], example[j + 2]))


def neighbors(p):
    x, y, z = p
    if x < max_x:
        yield (x + 1, y, z)
    if x > min_x:
        yield (x - 1, y, z)
    if y < max_y:
        yield (x, y + 1, z)
    if y > min_y:
        yield (x, y - 1, z)
    if z < max_z:
        yield (x, y, z + 1)
    if z > min_z:
        yield (x, y, z - 1)


def count_neighbors():
    shared_faces = 0
    for d in droplets:
        for p in neighbors(d):
            if p in droplets:
                shared_faces += 1
    return shared_faces


max_x = 0
min_x = 99
max_y = 0
min_y = 99
max_z = 0
min_z = 99


def load_input():
    global droplets
    droplets = set()
    for line in get_source():
        # x,y,z=line.split(", ")
        if not line:
            break
        x, y, z = [int(v) for v in line.strip().split(",")]
        droplets.add((x, y, z))
        # print((x,y,z))


load_input()

for d in droplets:
    x, y, z = d
    if x >= max_x:
        max_x = x + 1
    elif x <= min_x:
        min_x = x - 1
    if y >= max_y:
        max_y = y + 1
    elif y <= min_y:
        min_y = y - 1
    if z >= max_z:
        max_z = z + 1
    elif z <= min_z:
        min_z = z - 1

nn = count_neighbors()
faces = len(droplets) * 6 - nn
print(f"PART1: there are {nn} faces in between droplets, so external {faces=}")

# PART2

groups: list[
    set[tuple[int, int, int]]
] = []  # each group is a set of spaces that inter-connect
spaces = {}  # coord -> how many droplets around it


def count_spaces():
    shared_faces = 0
    non_shared_faces = 0
    for d in droplets:
        for n in neighbors(d):
            if n in droplets:
                shared_faces += 1
            else:
                non_shared_faces += 1
                spaces[n] = 1 if n not in spaces else spaces[n] + 1
    return shared_faces, non_shared_faces


def merge_groups():
    singles = 0
    new_spaces = {}
    for c in spaces:
        """
        if spaces[c] == 6:
            singles += 1
            LOG.debug(f"fully enclosed {c=}")
        else:
        """
        # find group membership if any, else start a group
        group: T.Optional[set[tuple[int, int, int]]] = None
        for g in groups:
            if c in g:
                group = g
                break
        if group is None:
            group = set()
            group.add(c)

        # merge group with all neighbor empty spaces
        LOG.debug(f"add/merge neighbors of {c=}")
        for n in neighbors(c):
            if n not in droplets:
                if n not in spaces:
                    new_spaces[n] = 0  # no neighbor droplets
                if n not in group:
                    # if neighbor is in another group, union with it
                    ngroup = None
                    for g in groups:
                        if n in g:
                            ngroup = g
                            break
                    if ngroup:
                        LOG.debug(f"found {n=} in {ngroup=} ==> join with {group=}")
                        group = set.union(group, ngroup)
                        groups.remove(ngroup)
                    else:
                        LOG.debug(f"not found {n=} ==> add it to {group=}")
                        group.add(n)
                        for n in group:
                            if not isinstance(n, tuple):
                                raise ValueError(f"{group=}")
        # in case group is new, add to groups
        if group and group not in groups:
            groups.append(group)
    if new_spaces:
        print(f"adding spaces {new_spaces=}")
        for n in new_spaces:
            spaces[n] = new_spaces[n]
    return singles


if not spaces:
    count_spaces()
print(f"{len(spaces)=}")

# singles = merge_groups()
print(f"{len(spaces)=} {len(groups)=}")


def print_groups():
    group_sizes = {}
    for g in groups:
        size = len(g)
        group_sizes[size] = 1 if size not in group_sizes else group_sizes[size] + 1
    print(f"{group_sizes=}")
    return group_sizes


group_sizes = print_groups()


exposed_groups = []


def mark_exposed():
    for g in groups:
        for n in g:
            x, y, z = n
            if (
                x == max_x
                or x == min_x
                or y == min_y
                or y == max_y
                or z == max_z
                or z == min_z
            ):
                exposed_groups.append(g)
                break


def count_pfaces():
    pfaces = 0
    for g in groups:
        if g not in exposed_groups:
            for c in g:
                pfaces += spaces[c]
    print(f"{pfaces=}")
    return pfaces


# pfaces = count_pfaces()


def expand_boundaries():
    global max_x, max_y, max_z, min_x, min_y, min_z
    max_x += 1
    max_y += 1
    max_z += 1
    min_x -= 1
    min_y -= 1
    min_z -= 1


"""Try a different approach, just search from bounding box inwards"""


def bounding_box():
    nodes = [
        (min_x, y, z) for y in range(min_y, max_y + 1) for z in range(min_z, max_z + 1)
    ]
    nodes.extend(
        [
            (max_x, y, z)
            for y in range(min_y, max_y + 1)
            for z in range(min_z, max_z + 1)
        ]
    )
    nodes.extend(
        [
            (x, min_y, z)
            for x in range(min_x, max_x + 1)
            for z in range(min_z, max_z + 1)
        ]
    )
    nodes.extend(
        [
            (x, max_y, z)
            for x in range(min_x, max_x + 1)
            for z in range(min_z, max_z + 1)
        ]
    )
    nodes.extend(
        [
            (x, y, min_z)
            for x in range(min_x, max_x + 1)
            for y in range(min_y, max_y + 1)
        ]
    )
    nodes.extend(
        [
            (x, y, max_z)
            for x in range(min_x, max_x + 1)
            for y in range(min_y, max_y + 1)
        ]
    )
    return nodes


nodes = bounding_box()
visited = set()
faces = 0


def do_round(nodes):
    global faces
    next_nodes = []
    for p in nodes:
        if p in visited:
            continue
            raise ValueError(f"already seen {p=}")
        visited.add(p)
        for n in neighbors(p):
            if n in droplets:
                faces += 1
            elif n not in visited:
                next_nodes.append(n)
    return next_nodes


while nodes:
    nodes = do_round(nodes)
    print(f"{faces=}")
