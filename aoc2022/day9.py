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

def follow(head, tail) -> tuple[int, int]:
    x, y = tail
    w, z = head
    if abs(y - z) + abs(x - w) > 2:
        print(f" . {x=} {y=} {w=} {z=}")
        if x < w:
            x += 1
        elif x > w:
            x -= 1
        if y < z:
            y += 1
        elif y > z:
            y -= 1
        print(f" .. {x=} {y=} {w=} {z=}")
    elif abs(x - w) > 1:
        x = int((x + w)/2)
    elif abs(y - z) > 1:
        y = int((y + z)/2)
    return (x, y)

_total = 0

def move(head: tuple[int, int], tail: tuple[int, int], d:str, c:int, visited: set):
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
        print(f" {ph=} {pt=} -> {head=} {tail=}")
        visited.add(tail)
    return head, tail

def run(lines):
    visited=set()
    head: tuple[int, int] = (0, 0)
    tail: tuple[int, int] = (0, 0)
    for l in lines:
        d, c = l.split(" ")
        c = int(c)
        head, tail = move(head, tail, d, c, visited)
    print(f"===== final {_total=} {len(visited)=}")


if __name__ == "__main__":
    run(all_lines(get_source()))

print(f"done {__name__}")
