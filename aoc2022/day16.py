from .lib import *
import functools
import itertools
import logging
import re

logging.basicConfig()
day = "day16"
LOG = logging.getLogger("aoc_" + day)
LOG.setLevel(logging.INFO)

EXAMPLE = False
PART1 = False
PART2 = True


def sample():
    global target_row, part2_max
    target_row = 10
    part2_max = 20
    return open(f"aoc2022/inputs/{day}-example.txt", "r")


def input():
    global target_row, part2_max
    target_row = 2000000
    part2_max = 4000000
    return open(f"aoc2022/inputs/{day}.txt", "r")


def dist(x, y, u, v):
    return abs(x - u) + abs(y - v)


class Valve:
    def __init__(self, name, neighbors, rate):
        self.name = name
        self.neighbors = neighbors
        self.rate = rate
        self.dists = {}
        for d in neighbors:
            self.dists[d] = 1
        self.dest_pots = {}

    def add(self, v: "Valve"):
        if v.name not in self.dists:
            print(f"{self.name} doesn't know {v.name} yet")
            return
        base_dist = self.dists[v.name]
        has_changed = False
        for d in v.dists:
            via_dist = base_dist + v.dists[d]
            if d not in self.dists:
                self.dists[d] = via_dist
                has_changed = True
            else:
                if self.dists[d] > via_dist:
                    self.dists[d] = via_dist
                    has_changed = True
        return has_changed


def parse(lines: list[str]):
    global beacons, sensors, max_x, max_y, min_x, min_y, max_d, max_max_x, min_min_x
    p = re.compile(
        "^Valve (..) has flow rate=([0-9]*); tunnel[s]? lead[s]? to valve[s]? (.*)$"
    )
    rates = {}
    valves = {}
    for l in lines:
        m = p.fullmatch(l)
        if not m:
            raise ValueError("no match: " + l)
        valve = m[1]
        rate = int(m[2])
        dests = m[3].split(", ")
        print(f"{valve=} has {rate=} and leads to {dests=}")
        valves[valve] = Valve(valve, dests, rate)
        rates[valve] = rate
    return valves, rates


def potential_value(name, remaining, visited=[]) -> dict[str, tuple[int, int]]:
    """At current valve, calculate the value of traveling to and turning on each valve"""
    global valves
    pot = {}
    total = 0
    valve = valves[name]
    for k, v in valves.items():
        if k in visited:
            continue
        remaining_time = remaining - valve.dists[k] - 1
        potval = v.rate * remaining_time
        if potval > 0:
            pot[k] = (potval, remaining_time)
            total += potval
    print(f"At {valve.name} potential {total=} and {pot=}")
    return pot


if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())
    valves, rates = parse(lines)

    rate_vals = list(rates.values())
    srv = sorted(rate_vals)
    print(f"{srv=}")
    valve_keys = list(valves)
    svk = sorted(valve_keys)
    print(f"{svk=}")
    top = sorted(rates.items(), key=lambda i: i[1], reverse=True)
    print(f"{top=}")
    for i in range(15):
        count = 0
        for k, v in valves.items():
            for n in v.neighbors:
                nv = valves[n]
                count += 1 if v.add(nv) else 0
        print(f"{i=} changed {count=}")
        if count == 0:
            break

    for k, r in top:
        sorted_vals = sorted(
            potential_value(k, 30).items(), key=lambda x: x[1][0], reverse=True
        )
        print(f"{k=} {r=} {sorted_vals=}")

    if PART1:

        def dfs1(current="AA", time=30, visited=["AA"]) -> tuple[str, int]:
            global valves
            print(f"{visited} ===> dfs: {current=}, {time=}")
            pot_vals = potential_value(current, time, visited)
            max_val = 0
            max_name = ""
            for name, pv in pot_vals.items():
                score, remaining = pv
                # with candidate NAME, we've added SCORE and have REMAINING time to go
                # so go down to next level and get back the best.
                next_name, new_val = dfs1(name, remaining, visited + [name])
                print(
                    f"{visited} ===> if we choose {name=}, its best is {next_name=} which gives {new_val=} ==="
                )
                if score + new_val > max_val:
                    max_val = score + new_val
                    max_name = current + next_name
            return (max_name, max_val)

        mn, mv = dfs1()
        print(f"{mn=} {mv=}")

    if PART2:

        def dfs2(
            current=("AA", 26), subs=("AA", 26), visited=["AA"]
        ) -> tuple[str, int]:
            """return the best destination after current and how much it adds to total"""
            global valves

            pot_vals = potential_value(current[0], current[1], visited)
            if not pot_vals:
                return ("", 0)

            max_val = 0
            max_name = ""
            for name, pv in pot_vals.items():
                score, remaining = pv
                # with candidate NAME, we've added SCORE and have REMAINING time to go
                # so try possible next ones and keep the best.
                best_name, best_val = (
                    dfs2((name, remaining), subs, visited + [name])
                    if remaining > subs[1]
                    else dfs2(subs, (name, remaining), visited + [name])
                )
                print(
                    f"{visited} ===> if we choose {name=}, its best is {best_name=} which gives {best_val=} ==="
                )
                if score + best_val > max_val:
                    max_val = score + best_val
                    max_name = current[0] + best_name
            return (max_name, max_val)

        mn, mv = dfs2()
        print(f"{mn=} {mv=}")

print(f"done {__name__}")
