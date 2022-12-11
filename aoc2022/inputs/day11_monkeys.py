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
        items=[50, 70, 89, 75, 66, 66],
        op=(lambda old: old * 5),
        div_by=2,
        left=2,
        right=1,
    )
)
MONKEYS.append(
    Monkey(
        items=[85],
        op=lambda old: old * old,
        div_by=7,
        left=3,
        right=6,
    )
)
MONKEYS.append(
    Monkey(
        items=[66, 51, 71, 76, 58, 55, 58, 60],
        op=lambda old: old + 1,
        div_by=13,
        left=1,
        right=3,
    )
)
MONKEYS.append(
    Monkey(
        items=[79, 52, 55, 51],
        op=lambda old: old + 6,
        div_by=3,
        left=6,
        right=4,
    )
)
MONKEYS.append(
    Monkey(
        items=[69, 92],
        op=lambda old: old * 17,
        div_by=19,
        left=7,
        right=5,
    )
)
MONKEYS.append(
    Monkey(
        items=[71, 76, 73, 98, 67, 79, 99],
        op=lambda old: old + 8,
        div_by=5,
        left=0,
        right=2,
    )
)
MONKEYS.append(
    Monkey(
        items=[82, 76, 69, 69, 57],
        op=lambda old: old + 7,
        div_by=11,
        left=7,
        right=4,
    )
)
MONKEYS.append(
    Monkey(
        items=[65, 79, 86],
        op=lambda old: old + 5,
        div_by=17,
        left=5,
        right=0,
    )
)
