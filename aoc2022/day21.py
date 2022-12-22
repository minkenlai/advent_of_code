from .lib import *
import functools
import itertools
import logging
import re

EXAMPLE = 0
PART1 = 0
PART2 = 1


class Monkey:
    def __init__(self, name, value, deps: list[str], op):
        self.name = name
        self.monkeys = []
        if value:
            self.value = value
            self.deps = None
            self.op = None
        else:
            self.value = None
            self.deps = deps
            self.op = op

    @property
    def val(self) -> T.Optional[int]:
        if self.name == "humn":
            return None
        if self.value:
            return self.value
        assert self.deps
        if not (self.deps[0] in monkeys and self.deps[1] in monkeys):
            return None
        if not (a := monkeys[self.deps[0]].val):
            return None
        if not (b := monkeys[self.deps[1]].val):
            return None
        if self.op == "+":
            self.value = a + b
        elif self.op == "-":
            self.value = a - b
        elif self.op == "*":
            self.value = a * b
        elif self.op == "/":
            self.value = int(a / b)
        else:
            raise ValueError
        LOG.info(f"{self.name} has {self.val}")
        return self.value

    def mk(self) -> T.Optional[tuple["Monkey", "Monkey"]]:
        if not self.deps or not self.deps[0] in monkeys or not self.deps[1] in monkeys:
            return None
        return (monkeys[self.deps[0]], monkeys[self.deps[1]])

    def __repr__(self):
        return f"Monkey({self.name}, {self.value}, {self.deps}, {self.op})"

    def solve(self, val: int) -> int:
        LOG.debug(self)
        if self.name == "humn":
            print(f"humn: {val=}")
            return val
        if self.val:
            return self.val
        r = self.mk()
        ma, mb = r if r else (None, None)
        if not (ma and mb):
            LOG.error(f"{self.name} does not know {self.deps}: {ma=} {mb=}")
            raise ValueError
        va = ma.val
        vb = mb.val
        if not va and not vb:
            LOG.error(f"{self.name} cannot determine values for either {self.deps}")
            raise ValueError
        if self.name == "root":
            if vb and isinstance(vb, int):
                LOG.info(f"right side is {vb}")
                return ma.solve(vb)
            elif va and isinstance(va, int):
                LOG.info(f"left side is {va}")
                return mb.solve(va)
            else:
                raise ValueError
        if not self.op:
            assert val
            return val
        LOG.info(
            f"We want to make {self.name}={val} using {va=} {ma=} {self.op=} {vb=} {mb=}"
        )
        v = va if va else vb
        m = mb if va else ma
        assert v and m
        if self.op == "+":
            # v + ? = val
            LOG.info(f"{v=} + {m.name}.val = {val} ({self.name})")
            return m.solve(val - v)
        if self.op == "*":
            # v * ? = val
            LOG.info(f"{v=} * {m.name}.val = {val} ({self.name})")
            return m.solve(int(val / v))
        if self.op == "-":
            if va:
                # v - ? = val
                LOG.info(f"{v=} - {m.name}.val = {val} ({self.name})")
                return m.solve(v - val)
            else:
                # ? - v = val
                LOG.info(f"{m.name}.val - {v=} = {val} ({self.name})")
                return m.solve(v + val)
        if self.op == "/":
            if va:
                # v / ? = val
                LOG.info(f"{v=} / {m.name}.val = {val} ({self.name})")
                return m.solve(int(v / val))
            else:
                # ? / v = val
                LOG.info(f"{m.name}.val / {v=} = {val} ({self.name})")
                return m.solve(v * val)


name_pattern = re.compile("[1-z]{4}")
op_pattern = re.compile("[-+*/]")
num_pattern = re.compile("[0-9]+")


def part1(lines: list[str]):
    global monkeys, answer
    answer = None
    monkeys = {}
    for l in lines:
        m = name_pattern.findall(l)
        if len(m) == 1:
            name = m[0]
            v = int(num_pattern.findall(l)[0])
            depa, depb, op = None, None, None
        else:
            name, depa, depb = m
            op = op_pattern.findall(l)[0]
            v = None
        monkeys[name] = Monkey(name, v, [depa, depb], op)
        if not answer and "root" in monkeys:
            val = monkeys["root"].val
            if val:
                answer = val
                print(f"root: {answer}")
    return monkeys


def part2(lines: list[str]):
    global monkeys
    root = None
    monkeys = {}
    for l in lines:
        m = name_pattern.findall(l)
        if len(m) == 1:
            name = m[0]
            v = int(num_pattern.findall(l)[0])
            depa, depb, op = None, None, None
        else:
            name, depa, depb = m
            op = op_pattern.findall(l)[0]
            v = None
        monkeys[name] = Monkey(name, v, [depa, depb], op)
    LOG.info(f"parsed {len(monkeys)} monkeys")
    root = monkeys["root"]
    return root.solve(None)


def print_graph(graph):
    for l in graph:
        print(l)


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())

    if PART1:
        print("do part 1")
        monkeys = part1(lines)

    if PART2:
        LOG.setLevel(logging.DEBUG)
        print("do part 2")
        print(part2(lines))

LOG.info(f"done {__name__}")
