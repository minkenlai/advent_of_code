import sys
from .lib import *


def value_of(x) -> int:
    return x


def score(trees, a, b) -> int:
    h = trees[a][b]
    v = 1
    print(f"=== {a=} {b=}")

    r = a - 1
    c = b
    t = 1
    while r >= 0 and trees[r][c] < h:
        r -= 1
        t += 1 if r >= 0 else 0
    v *= t
    print(f"up {t=} {v=}")

    r = a + 1
    c = b
    t = 1
    cols = len(trees[0])
    while r < cols and trees[r][c] < h:
        r += 1
        t += 1 if r < cols else 0
    v *= t
    print(f"down {t=} {v=}")

    r = a
    c = b - 1
    t = 1
    cols = len(trees)
    while c >= 0 and trees[r][c] < h:
        c -= 1
        t += 1 if c >= 0 else 0
    v *= t
    print(f"left {t=} {v=}")

    r = a
    c = b + 1
    t = 1
    while c < cols and trees[r][c] < h:
        c += 1
        t += 1 if c < cols else 0
    v *= t
    print(f"right {t=} {v=}")

    return v


def sample():
    return [
        "30373",
        "25512",
        "65332",
        "33549",
        "35390",
    ]


def process_rows(trees, rows, cols, vis):
    for r in range(1, rows - 1):
        tallest = trees[r][0]
        count = 0
        for c in range(1, cols - 1):
            if trees[r][c] > tallest:
                vis[r][c] = 1
                tallest = trees[r][c]
                count += 1
        print(f"{r=} {count=}")
        print(vis[r])
    vis = rotate(vis)
    print("vis after rotate")
    for l in vis:
        print(l)
    trees = rotate(trees)
    print("trees after rotate")
    for l in trees:
        print(l)


def count_visible(source: list[str]):
    rows = len(source)
    cols = len(source[0])
    vis = [[] for _ in range(cols)]
    trees = [[] for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            vis[r].append(0)
            trees[r].append(int(source[r][c]))
        print(trees[r])
    for r in range(rows):
        vis[r][0] = 1
        vis[r][cols - 1] = 1
    for c in range(cols):
        vis[0][c] = 1
        vis[rows - 1][c] = 1
    sum = 0
    for l in vis:
        for v in l:
            sum += v
        print(l)
    print(f"starting with vis {sum}")

    process_rows(trees, rows, cols, vis)
    process_rows(trees, rows, cols, vis)
    process_rows(trees, rows, cols, vis)
    process_rows(trees, rows, cols, vis)

    sum = 0
    for l in vis:
        for v in l:
            sum += v
    print(f"{sum=}")
    return sum


def run(lines):
    rows = len(lines)
    cols = len(lines[0])
    trees = [[] for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            trees[r].append(int(lines[r][c]))
        # print(trees[r])

    hi = 1
    hi_r = 0
    hi_c = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            v = score(trees, r, c)
            if hi < v:
                hi = v
                hi_r = r
                hi_c = c
                print(f"new high {hi=} {r=} {c=}")

    print(f"===== final {hi=} {hi_r=} {hi_c=}")


if __name__ == "__main__":
    run(all_lines(get_source()))

print(f"done {__name__}")
