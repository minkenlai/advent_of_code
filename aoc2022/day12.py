from .lib import *

ORD_A = ord("a")
START = (-1, -1)
END = (-1, -1)


def to_elev(ch: str) -> int:
    return ord(ch) - ORD_A


def get_elev(lines):
    global START, END
    rows = len(lines)
    cols = len(lines[0])
    elev = [[] for _ in range(rows)]
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == "S":
                val = to_elev("a")
                START = (r, c)
            elif ch == "E":
                val = to_elev("z")
                END = (r, c)
            else:
                val = to_elev(ch)
            elev[r].append(val)
        # print(elev[r])
    for row in elev:
        print(row)
    print(f"{START=} {END=}")
    return elev


def get_neighbors(co: tuple[int, int]) -> list[tuple[int, int]]:
    vals = []
    if co[0] > 0:
        vals.append((co[0] - 1, co[1]))
    if co[1] > 0:
        vals.append((co[0], co[1] - 1))
    if co[0] < MAX_R:
        vals.append((co[0] + 1, co[1]))
    if co[1] < MAX_C:
        vals.append((co[0], co[1] + 1))
    return vals


MAX_R = 0
MAX_C = 0
ELEV = []
STEPS = []


def el(co):
    return ELEV[co[0]][co[1]]


def st(co):
    return STEPS[co[0]][co[1]]


found_lowest = None


def do_round(q):
    global found_lowest
    nq = []
    for n in q:
        print(f"{n=} {el(n)=} {st(n)=}")
        for nn in get_neighbors(n):
            if el(n) <= el(nn) + 1:  # nn can reach n
                if st(nn) < 0 or st(nn) > st(n) + 1:  # nn is further than n
                    STEPS[nn[0]][nn[1]] = st(n) + 1
                    nq.append(nn)
                    print(f" . {nn=} {el(nn)=} {st(nn)=}")
                    if nn == START:
                        print(
                            f"======= FOUND START ====== {n=} {st(n)=} {nn=} {st(nn)=}"
                        )
                        return []
                if el(nn) == 0:
                    if not found_lowest:
                        print(
                            f"======= FOUND LOWEST ====== {n=} {st(n)=} {nn=} {st(nn)=}"
                        )
                        found_lowest = nn
                    else:
                        print(
                            f"=== FOUND other lowest === {n=} {st(n)=} {nn=} {st(nn)=}"
                        )
                    # return []
    return nq


def print_steps():
    for row in STEPS:
        print(row)


def run(lines):
    global MAX_R, MAX_C, ELEV, STEPS
    ELEV = get_elev(lines)
    MAX_R = len(ELEV) - 1
    MAX_C = len(ELEV[0]) - 1
    STEPS = [[-1 for _ in range(len(ELEV[0]))] for _ in range(len(ELEV))]
    STEPS[START[0]][START[1]] = -1
    STEPS[END[0]][END[1]] = 0
    for row in STEPS:
        print(row)
    q = [END]
    q = do_round(q)
    round = 0
    while q:
        q = do_round(q)
        round += 1
    # print_steps()
    return q


if __name__ == "__main__":
    q = run(all_lines(get_source()))
    print(f"First lowest found at {st(found_lowest)=}")
    print(f"Found START at {st(START)=}")

print(f"done {__name__}")
