import os
import sys
import functools
import itertools
import logging
import re

curr_dir = os.path.dirname(__file__)
aoc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(aoc_dir)
print(f"{sys.path=}")

import aoc2023.lib
from aoc2023.lib import all_lines, sample, input, LOG

EXAMPLE = 1
PART1 = 1
PART2 = 1

day_name = os.path.basename(curr_dir)
day_num = day_name[3:] if day_name.startswith('day') else 'unknown'
print(f"{day_name=} {day_num=}")

class Rating:
    def __init__(self, line):
        self.vars = line[1:-1].split(',')
        self.data = {}
        sum = 0
        for e in self.vars:
            var_name, value = e.split('=')
            self.data[var_name] = int(value)
            sum += int(value)
        self.sum = sum

    def get(self, name) -> int:
        return self.data[name]

    def __str__(self):
        return repr(self.data)

class Rule:
    def __init__(self, s):
        parts = s.split(':')
        if len(parts) == 1:
            self.cond = None
            self.dest = parts[0]
        else:
            self.cond, self.dest = parts
            for op in ['<', '>']:
                if op in self.cond:
                    self.var_name, value = self.cond.split(op)
                    self.value = int(value)
                    self.op = op
                    break


    def eval(self, r):
        if not self.cond:
            return self.dest
        r_value = r.get(self.var_name)
        print(self)
        if '<' == self.op and r_value < self.value:
            return self.dest
        elif '>' == self.op and r_value > self.value:
            return self.dest
        else:
            raise Exception(f"bad rule: {self.cond=} {self.dest=}")

    def __str__(self):
        return f"{self.cond}:{self.dest} {self.var_name=} {self.op=} {self.value=}"

class Workflow:
    def __init__(self, line):
        self.name, line = line.split('{')
        self.rules = line[:-1].split(',')
        self.rules = list(Rule(r) for r in self.rules)

    def eval(self, r) -> str:
        dest = None
        for rule in self.rules:
            dest = rule.eval(r)
            if dest:
                return dest

    def __str__(self):
        return f"{self.name=} {repr(self.rules)=}"

def part1(lines):
    answer=0
    section=0
    workflows = {}
    ratings = []
    for l in lines:
        if not l:
            section = 1
            continue
        if section:
            ratings.append(Rating(l))
            print(ratings[-1])
        else:
            w = Workflow(l)
            workflows[w.name] = w
            print(w)

    for r in ratings:
        w = workflows['in']
        while True:
            v = w.eval(r)
            if v == 'A':
                print(f"{answer} + {r.sum} = ", end='')
                answer += r.sum
                print(answer)
                break
            elif v == 'R':
                print(v)
                break
            else:
                print(f" -> {v}", end='')
                w = workflows[v]
    return answer


def part2(lines):
    answer=0
    workflows = {}
    rule_root = Rule('A')
    for l in lines:
        if not l:
            break
        w = Workflow(l)
        workflows[w.name] = w
        print(w)
    return answer

def main():
    filename = "input"
    if EXAMPLE:
        filename = "example"
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(os.path.join(curr_dir, filename), "r"), strip=True)
    print(f"input loaded, {len(lines)=}")

    if PART1:
        answer = part1(lines)
        print(f"PART1 {answer=}")

    if PART2:
        answer = part2(lines)
        print(f"PART2 {answer=}")

if __name__ == "__main__":
    main()