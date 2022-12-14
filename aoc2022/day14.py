from .lib import *
import functools
import itertools

PART1 = False
PART2 = True

def sample():
    return open("aoc2022/inputs/day14-example.txt", "r")

def input():
    return open("aoc2022/inputs/day14.txt", "r")

def parse(lines: list[str]):
    global min_x, max_x, max_y
    min_x = 999
    max_x = 0
    max_y = 0
    graph = []
    for l in lines:
        coords = l.split(" -> ")
        l = []
        for c in coords:
            x, y = (int(v) for v in c.split(","))
            min_x = x if x < min_x else min_x
            max_x = x if x > max_x else max_x
            max_y = y if y > max_y else max_y
            l.append((x, y))
        print(l)
        graph.append(l)
    return graph

def justify(graph):
    print(f"justified after finding {min_x=} {max_x=} {max_y=}")
    justified = []
    for l in graph:
        print(l)
        l = [(x-min_x, y) for (x, y) in l]
        print(l)
        justified.append(l)
    return justified

def plot(graph):
    h = {}
    for l in graph:
        p = None
        for n in l:
            if p is None:
                h[n] = "#"
                p = n
                continue
            x, y = p
            u, v = n
            print(f"line from {p=} to {n=}")
            print(f"{x=} {y=} {u=} {v=}")
            while x != u or y != v:
                if x < u:
                    x += 1
                elif x > u:
                    x -= 1
                elif y < v:
                    y += 1
                elif y > v:
                    y -= 1
                h[(x, y)] = "#"
                print(f"{x=} {y=}")
            h[n] = "#"
            p = n
        #print(f"{len(h)=}")
    return h

def left_of(c):
    return (c[0]-1, c[1])

def right_of(c):
    return (c[0]+1, c[1])

def settle(start):
    global result
    c = start
    if c[1] > max_y or c[0] < min_x or c[0] > max_x:
        return None
    while c not in result:
        c = (c[0], c[1] + 1)
    if left_of(c) not in result:
        return settle(left_of(c))
    if right_of(c) not in result:
        return settle(right_of(c))
    if c[1] > max_y:
        return None
    c = (c[0], c[1] - 1)
    result[c] = "o"
    return c

def print_graph():
    for y in range(max_y+1):
        l = ""
        for x in range(min_x, max_x+1):
            if (x, y) in result:
                l += result[(x, y)]
            else:
                l += "."
        print(l)

if __name__ == "__main__":
    lines = all_lines(sample())
    lines = all_lines(get_source())
    graph = parse(lines)

    result = plot(graph)
    print(f"{result=}")

    if PART1:
        start = (500, 0)
        count = 0
        while True:
            count += 1
            r = settle(start)
            print(f"{r=}")
            #print_graph()
            if not r:
                break
            if r == start:
                print(f"{count=}")
                break
        print_graph()
        print(f"{count=}")


    if PART2:
        start = (500, 0)
        min_x -= 500
        max_x += 500
        max_y += 2
        for i in range(min_x, max_x + 1):
            result[(i, max_y)] = "#"

        count = 0
        while True:
            count += 1
            r = settle(start)
            print(f"{r=}")
            #print_graph()
            if not r:
                break
            if r == start:
                print(f"{count=}")
                break
        print_graph()
        print(f"{count=}")

print(f"done {__name__}")
