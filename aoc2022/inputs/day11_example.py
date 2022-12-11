class Monkey:
    def __init__(self, items, op, div_by, left, right):
        self.items = items
        self.op = op
        self.div_by = div_by
        self.left = left
        self.right = right
        self.count = 0


MONKEYS: list[Monkey] = []

MONKEYS.append(
    Monkey(
        items=[79, 98],
        op=lambda old: old * 19,
        div_by=23,
        left=2,
        right=3,
    )
)
MONKEYS.append(
    Monkey(
        items=[54, 65, 75, 74],
        op=lambda old: old + 6,
        div_by=19,
        left=2,
        right=0,
    )
)
MONKEYS.append(
    Monkey(
        items=[79, 60, 97],
        op=lambda old: old * old,
        div_by=13,
        left=1,
        right=3,
    )
)
MONKEYS.append(
    Monkey(
        items=[74],
        op=lambda old: old + 3,
        div_by=17,
        left=0,
        right=1,
    )
)
