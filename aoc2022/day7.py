import sys
from .lib import *


def value_of(x) -> int:
    return x


def score(a, b) -> int:
    return a + b


class File:
    total_size: int = 0

    def __init__(self, name: str, size: int):
        self.name = name
        self.total_size = size

    def __repr__(self) -> str:
        return f" file {self.name=} {self.total_size=}"


all_dirs: list = []


class Dir:
    def __init__(self, name: str, parent: "Dir" = None):
        if not name:
            raise ValueError("no name provided")
        self.children: dict[str, T.Union["Dir", File]] = dict()
        self.name = name
        self.parent = parent
        all_dirs.append(self)
        pass

    @property
    def total_size(self) -> int:
        sum: int = 0
        print(f"summing total size for dir {self.name=} {self.children=}")
        for n in list(self.children):
            print(f"  {n=} {self.children[n]=}")
            sum += self.children[n].total_size
        return sum

    @property
    def fullname(self) -> str:
        if self.name == "/":
            return ""
        return (self.parent.fullname if self.parent else "") + "/" + self.name

    def __repr__(self) -> str:
        return f"Dir {self.fullname=} {self.children=}"

    def __str__(self) -> str:
        return self.__repr__()


def run(source: list[str]):
    sum = 0
    root = Dir("/")
    root.parent = root
    current_dir: Dir = root
    for line in source:
        line = line.strip()
        print(f"==={line=}")
        if not line:
            continue
        if line.startswith("$ cd "):
            des = line[5:]
            if des == "/":
                current_dir = root
                print(f"now in {current_dir.fullname=}")
                continue
            if des == "..":
                if current_dir == root:
                    print("=====ALREADY IN ROOT")
                    continue
                current_dir = current_dir.parent
                print(f"now in {current_dir.fullname=}")
                continue
            current_dir = T.cast(Dir, current_dir.children[des])
            print(f"now in {current_dir.fullname=}")
            continue
        if line.startswith("$ ls"):
            listing = True
            continue
        if line.startswith("dir "):
            name = line[4:]
            current_dir.children[name] = Dir(name, current_dir)
            print(f"added dir {name=}:  {current_dir=}")
            continue
        size, name = line.strip().split(" ")
        print(f"{size=} {name=}")
        if name in current_dir.children:
            raise ValueError(
                f"{current_dir.fullname=} already has {name}: {current_dir.children[name]}"
            )
        current_dir.children[name] = File(name, int(size))
        print(f"{current_dir.name=} {current_dir.children=}")

    all_dirs.sort(key=lambda d: d.total_size)
    sum = 0
    sizes = dict()
    root_size = 0
    for d in all_dirs:
        print(d)
        s = d.total_size
        sizes[s] = d
        if d == root:
            root_size = s
        sum += s
    print(f"{sum=}")
    free_space = 70000000 - root_size
    need_space = 30000000 - free_space
    print(f"{root_size=} {free_space=} {need_space=}")
    by_size = sorted(list(sizes))
    for s in by_size:
        print(s, sizes[s].fullname)


if __name__ == "__main__":
    run(all_lines(get_source()))

print(f"done {__name__}")
