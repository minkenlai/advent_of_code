from .lib import *
import itertools


def sample():
    return open("aoc2022/inputs/day13-example.txt", "r")


def input():
    return open("aoc2022/inputs/day13.txt", "r")


def both_int(a, b):
    return isinstance(a, int) and isinstance(b, int)


def compare(a, b, prefix=""):
    if both_int(a, b):
        if a < b:
            print("RIGHT: left side is lesser")
            return True
        elif b > a:
            print("WRONG: left side is greater")
            return False
        return None

    for (x, y) in itertools.zip_longest(a, b):
        print(f"{prefix}Compare {repr(x)=} and {repr(y)=}")

        if both_int(x, y):
            if x < y:
                print("RIGHT: left side is lesser")
                return True
            elif x > y:
                print("WRONG: left side is greater")
                return False
            continue

        if x is None:
            print("RIGHT: left side is shorter")
            return True
        if y is None:
            print("WRONG: right side is shorter")
            return False

        if isinstance(x, int) and not isinstance(y, int):
            x = [x]
        if isinstance(y, int) and not isinstance(x, int):
            y = [y]
        if isinstance(y, list) and isinstance(x, list):
            res = compare(x, y, prefix + "  ")
            if res is None:
                continue
            if res:
                print("RIGHT: bubble up")
                return True
            else:
                print("WRONG: bubble up")
                return False
        else:
            raise ValueError
    return None


def part1(lines):
    a = None
    b = None
    i = 0
    sum = 0
    for l in lines:
        if not l:
            a = None
            b = None
            continue
        l = eval(str(l))
        if a is None:
            a = l
        elif b is None:
            b = l
        if a is not None and b is not None:
            i += 1
            print(f"=== pair {i}")
            print(a)
            print(b)
            res = compare(a, b)
            if res is None or res:
                print("right")
                sum += i
                print(f"{sum=}")
            else:
                print("wrong")
    return sum


def comparator(a, b):
    res = compare(a, b)
    if res is None:
        return 0
    return -1 if res else 1


PART1 = False
PART2 = True

if __name__ == "__main__":
    # lines = all_lines(sample())
    lines = all_lines(get_source())

    if PART1:
        result = part1(lines)
        print(f"{result=}")
    if PART2:
        vals = [
            [[2]],
            [[6]],
        ]
        for l in lines:
            if not l:
                continue
            vals.append(eval(l))
        import functools

        results = sorted(vals, key=functools.cmp_to_key(comparator))
        marker1 = 0
        marker2 = 0
        max = 0
        for i, val in enumerate(results):
            max = i
            if val == [[2]]:
                marker1 = i + 1
                continue
            if val == [[6]]:
                marker2 = i + 1
                continue
        print(f"=== {marker1=} {marker2=} {max=} ")

print(f"done {__name__}")
