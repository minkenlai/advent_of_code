import os
import sys
import functools
import itertools
import logging
import re

curr_dir = os.path.dirname(__file__)
aoc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(aoc_dir)
print(f"{sys.path=}")

import aoc2023.lib
from aoc2023.lib import all_lines, sample, input, LOG

EXAMPLE = 0
PART1 = 1
PART2 = 1

day_name = os.path.basename(__file__)
day_num = re.search(r"\d+", day_name).group()
print(f"{day_name=} {day_num=}")

def differences(l1, l2):
    diff = 0
    for i,c in enumerate(l1):
        if c != l2[i]:
            if diff > 0:
                return 2
            else:
                diff = 1
    return diff
            

def validate_mirror(lines_so_far, more_lines) -> bool:
    smudge_ok=PART2
    print(f"checking for mirror for {len(lines_so_far)=}")
    diff = 0
    for i, l in enumerate(reversed(lines_so_far)):
        if i >= len(more_lines) or not more_lines[i]:
            print("end of more_lines")
            return not smudge_ok or diff == 1
        print(f"comparing {l=} and {more_lines[i]=}")
        diff += differences(l, more_lines[i])
        if not diff or (smudge_ok and diff == 1):
            continue
        else:
            return False
    print("******************* mirror found")
    return not smudge_ok or diff == 1

if __name__ == "__main__":
    filename = '/input'
    if EXAMPLE:
        filename = '/example'
        if EXAMPLE > 1:
            filename = filename + EXAMPLE
    lines = all_lines(open(curr_dir + filename, 'r'), strip=True)
    print(f"input loaded, {len(lines)=}")

    not_finished = True
    mirror=None
    hlines = []
    vlines = None
    blocks_completed = 0
    sum = 0
    for i,l in enumerate(lines):
        if mirror and l:
            # already found mirror in this block, just skip lines until blank
            continue
        if not l:
            print("===== block:")
            for hl in hlines:
                print(hl)
            blocks_completed += 1
            if not mirror:
                print("===== rotated block:")
                for vl in vlines:
                    print(vl)
                # we've reached end of block and no horizontal mirror was found
                for j, vl in enumerate(vlines):
                    if j and validate_mirror(vlines[:j], vlines[j:]):
                        mirror=j
                        sum += mirror
                        print(f"found vertical {mirror=} updated {sum=}")
                        break
            if not mirror:
                raise Exception(f"ERROR: no mirror found {hlines=} {vlines=}")
            mirror=None
            hlines=[]
            vlines=None
            continue
            
        # add to rotated lines 
        if not vlines:
            vlines = []
            for vl in range(len(l)):
                vlines.append([])
        for j, vl in enumerate(vlines):
            vl.append(l[j])
         
        if hlines and validate_mirror(hlines, lines[i:]):
            for hl in hlines:
                print(hl)
            for l in lines[i:i+len(hlines)]:
                print(l)
            mirror = len(hlines)
            vlines = None
            sum += mirror * 100
            print(f"found horizontal {mirror=} updated {sum=}")
        else:
            hlines.append(l)
    print(f"After {blocks_completed=} the total {sum=}")
            
    