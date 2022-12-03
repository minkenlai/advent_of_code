import sys
from .lib import *

def max_sum(source, top_n):
    sum = 0
    highest = []
    all = []
    lowest = 0
    for line in source:
        v = line.strip()
        if v:
            v = int(v)
            sum += v
            print(f"{sum=} after {v=}")
        else:
            all.append(sum)
            if (sum > lowest):
               highest.append(sum)
               highest.sort()
            if len(highest) > top_n:
                lowest = highest[0]
                highest = highest[1:]
            print(f"{highest=}")
            sum = 0
    sum = 0
    for v in highest:
        sum += v

    all.sort()
    top3 = all[-3:]
    print(f"{top3=}")
    return sum

def iter_ints(source):
    for line in source:
        if isinstance(line, str):
            v = line.strip()
        elif isinstance(line, int):
            v = int
        else:
            raise Exception(f"unexpected type {line.__class__}")
        if v:
            if isinstance(v, str):
                v = int(v)
            yield v
        else:
            return


if __name__ == "__main__":
    print(f"sum of top 3 are: {max_sum(sys.stdin, 3)}")

print(f"done {__name__}")