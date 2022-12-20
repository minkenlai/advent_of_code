from .lib import *
import functools
import itertools
import logging
import re

pOre = re.compile("Each ore robot costs ([0-9]*) ore")
pCla = re.compile("Each clay robot costs ([0-9]*) ore")
pObs = re.compile("Each obsidian robot costs ([0-9]*) ore and ([0-9]*) clay")
pGeo = re.compile("Each geode robot costs ([0-9]*) ore and ([0-9]*) obsidian")


def parse(lines: list[str]):
    global ore, cla, obs, geo
    """Blueprint 1:
    Each ore robot costs 3 ore.
    Each clay robot costs 4 ore.
    Each obsidian robot costs 4 ore and 18 clay.
    Each geode robot costs 3 ore and 8 obsidian.
    """
    blueprints = []
    for line in lines:
        ore = pOre.findall(line)[0]
        cla = pCla.findall(line)[0]
        obs = pObs.findall(line)[0]
        geo = pGeo.findall(line)[0]
        ore = int(ore)
        cla = int(cla)
        obs = tuple(int(i) for i in obs)
        geo = tuple(int(i) for i in geo)
        print(f"{ore=} {cla=} {obs=} {geo=}")
        blueprints.append(BluePrint(ore, cla, obs, geo))
    return blueprints


class BluePrint:
    def __init__(self, ore, cla, obs, geo):
        self.ore = ore
        self.cla = cla
        self.obs = obs
        self.geo = geo

    def ore_bot(self, inventory, rate) -> int:
        if inventory.ore >= self.ore:
            inventory.ore -= self.ore
            LOG.info(f" >  spend {self.ore} ore to build one ore_bot")
            return 1
        return 0

    def tt_ore(self, inventory, rate) -> tuple[int, int, int, int]:
        return (max(0, int((self.ore - inventory.ore) / rate.ore)), 0, 0, 0)

    def cla_bot(self, inventory, rate) -> int:
        LOG.debug(f" . {inventory.cla=} {self.cla=}")
        if inventory.ore >= self.cla:
            inventory.ore -= self.cla
            LOG.info(f" >  spend {self.cla} ore to build one cla_bot")
            return 1
        return 0

    def tt_cla(self, inventory, rate) -> tuple[int, int, int, int]:
        return (max(0, int((self.cla - inventory.ore) / rate.ore)), 0, 0, 0)

    def obs_bot(self, inventory, rate):
        if inventory.ore >= self.obs[0] and inventory.cla >= self.obs[1]:
            inventory.ore -= self.obs[0]
            inventory.cla -= self.obs[1]
            LOG.info(
                f" >  spend {self.obs[0]} ore and {self.obs[1]} cla to build one obs_bot"
            )
            return 1
        return 0

    def tt_obs(self, inventory, rate) -> tuple[int, int, int, int]:
        ore, cla = self.obs
        turns_ore = max(0, int((ore - inventory.ore) / rate.ore))
        turns_cla = (
            -1 if rate.cla < 1 else max(0, int((cla - inventory.cla) / rate.cla))
        )
        return (turns_ore, turns_cla, 0, 0)

    def geo_bot(self, inventory, rate):
        if inventory.ore >= self.geo[0] and inventory.obs >= self.geo[1]:
            inventory.ore -= self.geo[0]
            inventory.obs -= self.geo[1]
            LOG.info(
                f" >  spend {self.geo[0]} ore and {self.geo[1]} obs to build one geo_bot"
            )
            return 1
        return 0

    def tt_geo(self, inventory, rate) -> tuple[int, int, int, int]:
        ore, obs = self.geo
        turns_ore = max(0, int((ore - inventory.ore) / rate.ore))
        turns_obs = (
            -1 if rate.obs < 1 else max(0, int((obs - inventory.obs) / rate.obs))
        )
        return (turns_ore, 0, turns_obs, 0)


class Inventory:
    def __init__(self, name="Inventory"):
        self.name = name
        self.ore = 0
        self.cla = 0
        self.obs = 0
        self.geo = 0

    def inc(self, rates: list[int]):
        ore, cla, obs, geo = rates
        LOG.debug(f" {self.name} inc: {ore=} {cla=} {obs=} {geo=}")
        self.ore += ore
        self.cla += cla
        self.obs += obs
        self.geo += geo
        LOG.debug("  " + self.__str__())

    @property
    def rates(self):
        return [self.ore, self.cla, self.obs, self.geo]

    def __str__(self):
        return f"{self.name}: {self.ore=} {self.cla=} {self.obs=} {self.geo=}"

    def __repr__(self):
        return f"{self.name}({self.ore=}, {self.cla=}, {self.obs=}, {self.geo=})"


def print_graph(graph):
    for l in graph:
        print(l)


EXAMPLE = True
PART1 = True
PART2 = True

if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())
    blueprints = parse(lines)
    # print_graph()

    if PART1:

        def run_blueprint(bp: BluePrint) -> Inventory:
            total_time = 24
            inv = Inventory()
            rates = Inventory("Rates")
            rates.inc([1, 0, 0, 0])
            for t in range(1, total_time + 1):
                LOG.info(f"== Minute {t} ==")
                new_bots = [0, 0, 0, 0]
                # always build geo bot if we can
                new_bots[3] = bp.geo_bot(inv, rates)
                turns_geo = bp.tt_geo(inv, rates)
                turns_obs = bp.tt_obs(inv, rates)
                # build obs bot if we can (check it doesn't slow down geo bot)
                if not sum(new_bots):
                    # check if geo is waiting on long pole
                    if turns_obs[1] >= 0 and turns_geo[2] > turns_geo[0]:
                        new_bots[2] = bp.obs_bot(inv, rates)
                # build cla bot if we can (check it doesn't slow down above)
                if not sum(new_bots) and bp.tt_cla(inv, rates)[0] >= 0:
                    # check if either obs or geo is waiting on long pole
                    if turns_obs[1] > turns_obs[0] or turns_geo[2] > turns_geo[0]:
                        new_bots[1] = bp.cla_bot(inv, rates)
                # build ore bot if we can (check it doesn't slow down above)
                if not sum(new_bots):
                    # check if either obs or geo is waiting on long pole
                    if turns_obs[1] > turns_obs[0] or turns_geo[2] > turns_geo[0]:
                        new_bots[0] = bp.ore_bot(inv, rates)
                inv.inc(rates.rates)
                rates.inc(new_bots)
                LOG.info(rates)

            return inv

        LOG.setLevel(logging.DEBUG)
        total = 0
        for i, bp in enumerate(blueprints):
            inventory = run_blueprint(bp)
            print(f"====== bp{i+1} finished with {inventory=}")
            quality = (i + 1) * inventory.geo
            total += quality
            LOG.info(f"bot{i+1} {quality=} {total=}")

        print(f"sum {total=}")

    if PART2:
        pass

LOG.info(f"done {__name__}")
