import io
import sys


def max_sum(source, top_n):
    sum = 0
    highest = []
    lowest = 0
    for line in sys.stdin:
        v = line.strip()
        if v:
            v = int(v)
            sum += v
            print(f"{sum=} after {v=}")
        else:
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
    return sum


if __name__ == "__main__":
    print(f"sum of top 3 are: {max_sum(sys.stdin, 3)}")

print(f"done {__name__}")