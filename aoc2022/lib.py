import sys
import typing as T

def ints(value: str, splitter: str = " ") -> list[int]:
    parts = value.strip().split(splitter)
    return [int(v) for v in parts if v]


def convert(value: str, mapping: dict[str, T.Any]):
    return mapping[value]


def all_lines():
    return [v.strip() for v in sys.stdin]


def grouped(source, group_size=3):
    group = []
    i = 0
    for line in source:
        group.append(line.strip())
        i += 1
        if i % group_size == 0:
            yield group
            group = []


if __name__ == "__main__":
    assert ints("1 23 45") == [1, 23, 45]
    print(ints("1 23 45 6  78"))
    for line in all_lines():
        print(line)

print(f"done {__name__}")