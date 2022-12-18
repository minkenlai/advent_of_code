from .lib import *
import datetime
import functools
import itertools
import logging
import re


WIDTH = 7
ROCKS = [
    [15],
    [
        2,
        7,
        2,
    ],
    [
        1,
        1,
        7,
    ],
    [
        1,
        1,
        1,
        1,
    ],
    [
        3,
        3,
    ],
]


class Rock:
    def __init__(self, lines):
        self.lines = lines
        self.width = max(v.bit_length() for v in lines)
        self.height = len(lines)
        self.pos = 2
        self.depth = -2

    def valid_pos(self, c):
        return c >= 0 and c + self.width <= WIDTH

    def go(self, dir):
        c = self.pos + dir
        if self.valid_pos(c):
            self.pos = c

    def at_pos(self):
        """generate lines, bottom-up, at position"""
        for i in range(-1, -self.height - 1, -1):
            yield self.lines[i] << (7 - self.width - self.pos)


just_looped_jets = 1
last_loop_rock = 0


def rock_gen():
    global just_looped_jets, last_loop_rock
    while True:
        for r in ROCKS:
            if just_looped_jets:
                just_looped_jets = 0
                LOG.info(f"next rock is {r=}")
                if not last_loop_rock:
                    last_loop_rock = r
                elif last_loop_rock != r:
                    LOG.info("DIFFERENT rock after jets loop")
                else:
                    LOG.info("SAME rock after jets loop")
                last_loop_rock = r
            yield Rock(r)


def jet_gen(line: str):
    global just_looped_jets, last_loop_count, first_loop_count
    last_loop_at = 0
    first_loop_count = 0
    last_loop_count = 0
    while True:
        for c in line:
            yield -1 if c == "<" else 1
        LOG.info(f"looping jets at {count=} height={purged_count+len(settled_lines)-1}")
        just_looped_jets = purged_count + len(settled_lines) - 1
        loop_count = count - last_loop_at
        LOG.info(f"{last_loop_count=} now {loop_count=}")
        if not first_loop_count:
            first_loop_count = loop_count
        if not last_loop_count:
            last_loop_count = loop_count
        elif last_loop_count != loop_count:
            LOG.info(f"DIFFERENT {loop_count=}")
            last_loop_count = loop_count
        else:
            LOG.info(f"SAME {loop_count=}")
        last_loop_at = count
        if LOG.isEnabledFor(logging.INFO):
            for i in range(-1, -11, -1):
                print(f"  {settled_lines[i]:07b}")


def would_overlap(settled_lines, rock, depth=1):
    """whether rock at rock.pos would run into settled_lines at given depth"""
    # at depth 1, compare rock.lines[-1] with settles_lines[-1]
    # at depth 2, compare rock.lines[-1] with settles_lines[-2] and rl=-2 with sl=-1
    if depth < 1:
        raise ValueError
    for d in range(0, depth):
        if d >= len(rock.lines):
            continue
        rl = rock.lines[-1 - d] << (7 - rock.width - rock.pos)
        sl = settled_lines[d - depth]
        if rl | sl != rl ^ sl:
            LOG.debug(f"{rock.pos=} {bin(rl)=} {bin(sl)=} overlap")
            return True
        LOG.debug(f"{rock.pos=} {d=} {bin(rl)=} {bin(sl)=} do not overlap")
    return False


def settle(settled_lines, rock, depth):
    if LOG.isEnabledFor(logging.DEBUG):
        print_settled_lines()
        LOG.debug(f"settle {rock.lines=} at {depth=}")
    for rl, sl in zip(range(-1, -depth - 1, -1), range(-depth, 0)):
        LOG.debug(f"{rock.lines=} {rl=} {sl=}")
        if rock.height + rl < 0:
            continue
        rl = rock.lines[rl] << (7 - rock.width - rock.pos)
        LOG.debug(f"rock line {rl:07b}")
        LOG.debug(f"sett line {settled_lines[sl]:07b}")
        settled_lines[sl] |= rl
        LOG.debug(f"merg line {settled_lines[sl]:07b}")
    for rl in range(-depth, -len(rock.lines), -1):
        rl = rock.lines[rl - 1]
        settled_lines.append(rl << (7 - rock.width - rock.pos))
    return settled_lines


def one_rock():
    global max_depth, count
    r = rock_iter.__next__()
    r.go(jet_iter.__next__())
    r.go(jet_iter.__next__())
    r.go(jet_iter.__next__())
    # while able to move down
    depth = 0
    while True:
        d = jet_iter.__next__()
        pos = r.pos
        r.go(d)
        if depth > 0 and would_overlap(settled_lines, r, depth):
            r.pos = pos
        if would_overlap(settled_lines, r, depth + 1):
            settle(settled_lines, r, depth)
            break
        depth += 1
        if depth > max_depth:
            max_depth = depth
            print(f"{max_depth=} {len(settled_lines)=} {depth=}")
    count += 1
    # lateral movement
    # downward movement


def print_settled_lines():
    for r in range(0, len(settled_lines)):
        print(f"{settled_lines[-1-r]:07b}")


purged_count = 0


def purge_settled_lines(keep=1000):
    global settled_lines, purged_count
    current_lines = len(settled_lines)
    if current_lines < keep:
        return settled_lines
    new_settled_lines = []
    for i in range(-keep, 0):
        new_settled_lines.append(settled_lines[i])
    assert len(new_settled_lines) == 1000
    settled_lines = new_settled_lines
    purged_count += current_lines - keep
    LOG.info(
        f"=== purged {current_lines - keep} from settled_lines, bringing total to {purged_count}, keeping {keep}"
    )


EXAMPLE = 0
PART1 = 1
PART2 = 1
LOG.setLevel(logging.INFO)

TEST_JETS = False

if __name__ == "__main__":
    if EXAMPLE:
        lines = all_lines(sample())
    else:
        lines = all_lines(input())

    LOG.info(f"{lines=}")
    jet_iter = jet_gen(lines[0])
    if TEST_JETS:
        for i in range(len(lines[0]) + 5):
            print(f"{i} {jet_iter.__next__()}")

    TEST_OVERLAP = True
    if TEST_OVERLAP:
        assert not would_overlap([1 << 5], Rock([7]))
        assert would_overlap([1 << 4], Rock([7]))
        assert not would_overlap([1 << 4, 1 << 5], Rock([7]))
        assert would_overlap([1 << 4, 1 << 5], Rock([7]), 2)
    TEST_SETTLE = 1
    if TEST_SETTLE:
        pass

    def reset():
        global count, max_depth, settled_lines, rock_iter, jet_iter
        count = 0
        max_depth = 0
        settled_lines = [0b1111111]
        rock_iter = rock_gen()
        jet_iter = jet_gen(lines[0])

    count = 0
    max_depth = 0
    settled_lines = [0b1111111]
    reset()

    # LOG.setLevel(logging.DEBUG)
    if PART1 or PART2:
        rocks = 2022
        # for each rock up to max
        while count < rocks:
            one_rock()
            if count % 1000 == 0:
                purge_settled_lines()
        print(f"after rock {count}, {purged_count=} {len(settled_lines)=}")

    if PART2:
        # look for loops.. most likely when the input file resets and the next rock is same
        rocks = 10000
        first_loop_count = 0
        last_loop_count = 0
        checkpoint = 1000
        check_mag = 1000
        while count < rocks:
            one_rock()
            if count % 1000 == 0:
                purge_settled_lines()
            if count >= checkpoint:
                print(
                    f"after rock {count}, {purged_count=} {len(settled_lines)=} {datetime.datetime.now().isoformat()}"
                )
                checkpoint += check_mag
                if checkpoint == check_mag * 10:
                    check_mag *= 10
        print(
            f"after rock {count}, {purged_count=} {len(settled_lines)=} total height {purged_count+len(settled_lines)-1}"
        )

        # saw in the above, loops were stable
        rocks = 1000000000000
        reset()
        complete_loops = int((rocks - first_loop_count) / last_loop_count)
        after_loop_count = (rocks - first_loop_count) % last_loop_count
        rocks = first_loop_count + last_loop_count
        while count < rocks:
            one_rock()

    # print_settled_lines()
LOG.info(f"done {__name__}")
