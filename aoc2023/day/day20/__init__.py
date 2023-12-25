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

EXAMPLE = 2
PART1 = 1
PART2 = 1

day_name = os.path.basename(curr_dir)
day_num = day_name[3:] if day_name.startswith('day') else 'unknown'
print(f"{day_name=} {day_num=}")

pulse_modules = {}
from collections import deque
pulse_queue = deque()
all_names = []


class PulseModule:
    def __init__(self, name=None, destinations=None):
        self.name = name
        self.destinations = destinations if destinations else []
        self.high = 0

    def register(self):
        for name in self.destinations:
            if name not in pulse_modules:
                LOG.error(f"Looking for {name} but not finding it in {repr(pulse_modules)}")
            pulse_modules[name].add_sender(self.name)

    def add_sender(self, name):
        # base class does nothing
        pass

    def receive(self, name, pulse):
        self.send(pulse)

    def send(self, pulse):
        #print(f"                                 queue: {self.name} -{pulse}-> {self.destinations}")
        for m in self.destinations:
            pulse_queue.append((self.name, pulse, m))

    def __repr__(self):
        return f"PulseModule({self.name} -> {self.destinations})"

class FakeModule(PulseModule):
    def send(self, pulse):
        # don't queue any outgoing pulse
        pass

class FlipFlop(PulseModule):
    def __init__(self, name, destinations=[]):
        super().__init__(name, destinations)

    def receive(self, name, pulse):
        if pulse:
            # do nothing for high pulse
            pass
        else:
            self.flip()
            self.send(self.high)

    def add_sender(self, name):
        # flip-flop doesn't care about senders
        pass

    def flip(self):
        self.high = 0 if self.high else 1

    def snapshot(self):
        return '1' if self.high else '0'

class Conjunction(PulseModule):
    def __init__(self, name, destinations=[]):
        super().__init__(name, destinations)
        self.senders={}

    def add_sender(self, name):
        self.senders[name] = 0

    def receive(self, name, pulse):
        self.senders[name] = pulse
        self.send(0 if self.all_high() else 1)

    def all_high(self):
        for sv in self.senders.values():
            if not sv:
                return 0
        return 1

    def all_low(self):
        for sv in self.senders.values():
            if sv:
                return 0
        return 1

    def snapshot(self):
        state = []
        for name in all_names:
            if name in self.senders:
                state.append('1' if self.senders[name] else '0')
        return ''.join(state)

def snapshot(pulse_modules):
    state=[]
    for name in all_names:
        state.append(name + ':' + pulse_modules[name].snapshot())
    return ''.join(state)

def load_data(lines, example):
    global pulse_modules, all_names
    pulse_modules={}
    if example:
        pulse_modules['output'] = FakeModule('output', [])
    else:
        pulse_modules['rx'] = FakeModule('rx', [])
    for l in lines:
        name, destinations = l.split(' -> ')
        destinations = destinations.split(', ')
        if name == 'broadcaster':
            pulse_modules[name] = PulseModule(name, destinations)
            continue
        name = name[1:]
        all_names.append(name)
        if l[0] == '%':
            pulse_modules[name] = FlipFlop(name, destinations)
        elif l[0] == '&':
            pulse_modules[name] = Conjunction(name, destinations)
        else:
            raise Exception(l)

    for n, m in pulse_modules.items():
        print(f"{n}: {m.name} -> {m.destinations}")
    for m in pulse_modules.values():
        print(f"register {m.name} as sender to {repr(m.destinations)}")
        m.register()

def part1(lines, example=0, iterations=1000):
    global pulse_modules, all_names, pulse_queue
    load_data(lines, example)

    total_counts = [0, 0]
    for i in range(iterations):
        count = [0,0]
        pulse_queue.append(('button', 0, 'broadcaster'))
        while pulse_queue:
            sender, pulse, dest = pulse_queue.popleft()
            if dest in pulse_modules:
                print(f"do {sender} -{pulse}-> {dest}")
                pulse_modules[dest].receive(sender, pulse)
                count[pulse] += 1
            else:
                LOG.warn(f"{dest=} not found in {repr(pulse_modules)}")
        total_counts[0] += count[0]
        total_counts[1] += count[1]
        print(f"after {i+1} presses, {total_counts=}")
    return total_counts

def part2(lines, example, iterations):
    global pulse_modules, all_names, total_counts, reached
    load_data(lines, example)

    total_counts = [0, 0]
    if example:
        reached = {'inv':0, 'con':0}
    else:
        reached = {'th':0, 'sv':0, 'gh':0, 'ch':0}
    for i in range(iterations):
        count = [0,0]
        pulse_queue.append(('button', 0, 'broadcaster'))
        while pulse_queue:
            sender, pulse, dest = pulse_queue.popleft()
            if dest in pulse_modules:
                print(f"do {sender} -{pulse}-> {dest}")
                pulse_modules[dest].receive(sender, pulse)
                count[pulse] += 1
        total_counts[0] += count[0]
        total_counts[1] += count[1]

        found_all = True
        for name in reached.keys():
            if reached[name] == 0:
                if pulse_modules[name].all_low():
                    print(f"{name} got all_low at {i=}")
                    reached[name] = i
                if reached[name] == 0:
                    found_all = False
        print(f"after {i+1} presses, {total_counts=} {reached=}")
        if found_all:
            break

    return total_counts

def main(example=EXAMPLE, p1=PART1, p2=PART2, iterations=1000):
    filename = "input"
    if example:
        filename = "example"
        if example > 1:
            filename = filename + str(example)
    lines = all_lines(open(os.path.join(curr_dir, filename), "r"), strip=True)
    print(f"input loaded, {len(lines)=}")

    if p1:
        answer = part1(lines, example, iterations)
        print(f"part1 {answer=}")
    if p2:
        answer = part2(lines, example, iterations)
        print(f"part2 {answer=}")

if __name__ == "__main__":
    main()