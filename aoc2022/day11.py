from .lib import *
from inputs.day11_monkeys import *

# from inputs.day11_example import *

PART1 = False
PART2 = True
rounds = 0

DIVISORS = [m.div_by for m in MONKEYS]


class Item:
    def __init__(self, val):
        self.vals = [val % m.div_by for m in MONKEYS]
        print(f"Item({val}) has {self.vals=}")

    def __str__(self):
        return self.vals.__str__()


for m in MONKEYS:
    m.items = [Item(val) for val in m.items]
    print(m.items)


def run():
    global rounds
    rounds += 1
    for i, m in enumerate(MONKEYS):
        # print(f"Processing MONKEY[{i}] {m.div_by=}")
        for j, item in enumerate(m.items):
            if PART1:
                item.vals = [int(m.op(val) / 3) for val in item.vals]
            elif PART2:
                item.vals = [m.op(val) for val in item.vals]
                for k, d in enumerate(DIVISORS):
                    item.vals[k] = item.vals[k] % d
                # print(f"Monkey {i} item {j} {item.vals=}")
            else:
                raise ValueError
            # print(f"Monkey {i} has {item.vals[i]=} and {m.div_by=}")
            if item.vals[i] % m.div_by == 0:
                target = m.left
            else:
                target = m.right
            MONKEYS[target].items.append(item)
            m.count += 1
            # print(f"{i=}: {item.vals=} {target=} {len(MONKEYS[target].items)=}")
        m.items = []


def printcounts():
    print(f"after {rounds=} =====")
    for i, m in enumerate(MONKEYS):
        print(f"MONKEY[{i}] inspected {m.count}")


if __name__ == "__main__":
    for i in range(10000):
        run()
        if 0 == rounds % 1000:
            printcounts()
    # printcounts()

print(f"done {__name__}")
