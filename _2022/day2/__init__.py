import sys

def score(a, b):
    if a == "A":
        x = 1
    elif a == "B":
        x = 2
    elif a == "C":
        x = 3
    else:
        raise ValueError
    if b == "X":
        y = x - 1
        if y == 0:
            y = 3
    elif b == "Y":
        y = x
    elif b == "Z":
        y = x + 1
        if y == 4:
            y = 1
    else:
        raise ValueError
    v = y
    if (y - x) % 3 == 1:
        v += 6
    elif (y - x) % 3 == 2:
        v += 0
    else:
        v += 3
    print(f"{x=} {y=} {v=}")
    return v

def run():
    sum = 0
    for line in sys.stdin:
        a, b = line.strip().split(" ")
        print(f"{a=} {b=}")
        sum += score(a, b)
        print(f"{sum=}")

if __name__ == "__main__":
    run()

print(f"done {__name__}")