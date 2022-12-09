import sys
from .lib import *

def sample():
    return [
        "30373",
        "25512",
        "65332",
        "33549",
        "35390",
    ]

def follow(head, tail) -> list[tuple[int, int]]:
    #print(f"{tail=}")
    x, y = tail[0]
    w, z = head
    if y==z and abs(x - w) > 1:
        if x < w:
            x = w-1
        elif x > w:
            x = w+1
    elif x==w and abs(y - z) > 1:
        if y < z:
            y = z-1
        elif y > z:
            y = z+1
    elif abs(y - z) + abs(x - w) > 2:
        print(f" . {x=} {y=} {w=} {z=}")
        if x < w:
            x = w-1 if w - x > 1 else w
        elif x > w:
            x = w+1 if x - w > 1 else w
        if y < z:
            y = z-1 if z - y > 1 else z
        elif y > z:
            y = z+1 if y - z > 1 else z
        print(f" .. {x=} {y=} {w=} {z=}")

    new_tail = [(x, y)]
    if len(tail) == 1:
        return new_tail
    new_tail.extend(follow((x, y), tail[1:]))
    return new_tail

_total = 0

def move(head: tuple[int, int], tail: list[tuple[int, int]], d:str, c:int, visited: set):
    global _total
    for i in range(c):
        ph, pt = head, tail
        _total += 1
        if d=="U":
            head = (head[0]+1, head[1])
        elif d=="D":
            head = (head[0]-1, head[1])
        if d=="L":
            head = (head[0], head[1]-1)
        elif d=="R":
            head = (head[0], head[1]+1)
        tail = follow(head, tail)
        visited.add(tail[-1])
    return head, tail

def run(lines):
    visited=set()
    head: tuple[int, int] = (0, 0)
    tail: list[tuple[int, int]] = [(0, 0) for _ in range(9)]
    for l in lines:
        d, c = l.split(" ")
        c = int(c)
        ph, pt = head, tail
        head, tail = move(head, tail, d, c, visited)
        print(f" {d=} {c=} : {ph=} {pt=} -> {head=} {tail=}")
    print(f"===== final {_total=} {len(visited)=}")


if __name__ == "__main__":
    run(all_lines(get_source()))

print(f"done {__name__}")
