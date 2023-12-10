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

# char mapped to [Up,Down,Left,Right]
pipes = {
    '|' : [1,1,0,0],
    '-' : [0,0,1,1],
    'L' : [1,0,0,1],
    'J' : [1,0,1,0],
    '7' : [0,1,1,0],
    'F' : [0,1,0,1],
    '.' : [0,0,0,0],
    'S' : [1,1,1,1],
}
up=0
down=1
left=2
right=3

if __name__ == "__main__":
    filename = '/input'
    if EXAMPLE:
        filename = '/example'
        if EXAMPLE > 1:
            filename = filename + str(EXAMPLE)
    lines = all_lines(open(curr_dir + filename, 'r'), strip=True)
    print(f"input loaded, {len(lines)=}")

    # build map, each coordinate [i][j] has [U,D,L,R]
    m = []
    visited = []  # initialize to all 0s
    x = None
    y = None
    for i, l in enumerate(lines):
        r = []
        for j, c in enumerate(l):
            r.append(pipes[c])
            if c == 'S':
                x, y = i, j
        m.append(r)
        visited.append([0]*len(r))

    def open_ways(m, x, y):
        result=[]
        if x > 0 and m[x-1][y][down]:
            result.append(1)
        else:
            result.append(0)
        if x + 1 < len(m) and m[x+1][y][up]:
            result.append(1)
        else:
            result.append(0)
        if y > 0 and m[x][y-1][right]:
            result.append(1)
        else:
            result.append(0)
        if y + 1 < len(m[x]) and m[x][y+1][left]:
            result.append(1)
        else:
            result.append(0)
        print(f"{x=} {y=} {result=}")
        return result
                
    result = open_ways(m, x, y)
    m[x][y] = result
    visited[x][y] = 1
    cw = None
    anti = None
    if result[up]:
        cw = [x-1,y] 
        prev = [up]
    if result[down]:
        if not cw:
            cw = [x+1,y]
            prev = [down]
        else:
            anti = [x+1,y] 
            prev.append(down)
    if result[left]:
        if not cw:
            cw = [x,y-1]
            prev = [left]
        else:
            anti = [x,y-1]
            prev.append(left)
    if result[right]:
        assert cw
        anti = [x,y+1]
        prev.append(right)
    print(f"from {x=} {y=} {result=} we're going {prev=} to {cw=} and {anti=}")
    visited[cw[0]][cw[1]] = 1
    visited[anti[0]][anti[1]] = 1

    def next_dir(prev_dir, x, y):
        current = m[x][y]
        if current[up] and prev_dir != down:
            return up, x-1, y
        if current[down] and prev_dir != up:
            return down, x+1, y
        if current[left] and prev_dir != right:
            return left, x, y-1
        if current[right] and prev_dir != left:
            return right, x, y+1


    count = 0
    while cw != anti:
        count += 1
        cw_dir, cw_x, cw_y = next_dir(prev[0], cw[0], cw[1])
        anti_dir, anti_x, anti_y = next_dir(prev[1], anti[0], anti[1])
        prev = [cw_dir, anti_dir]
        cw = [cw_x, cw_y]
        anti = [anti_x, anti_y]
        visited[cw_x][cw_y] = 1
        visited[anti_x][anti_y] = 1
        print(f"{count=} {prev=} {cw=} {anti=}")
        
    # PART2: for each unvisited spot, go toward nearest wall and
    # if it's IN or OUT, mark same
    # if it's crossing pipes, count how many crossed.
    # diagonal opposite corners also count as 1.
    # BETTER:
    # Going from outside in, using dynamic programming algo:
    # If crossed odd number of pipes, it's inside.
    # Just going top-down should work too.
    outside='O'
    inside='I'
    count = 0
    for i, vl in enumerate(visited):
        pipe_stack = []
        side_status = False
        last_corner = None
        for j, c in enumerate(vl):
            if c:
                # are we crossing a pipe?
                p = m[i][j]
                if p == [1,1,0,0]:
                    side_status = not side_status
                elif p == [0,0,1,1]:
                    pass
                elif not last_corner:
                    last_corner = p
                else:
                    is_across = True
                    for (a, b) in zip(last_corner, p):
                        is_across &= a ^ b
                    print(f"{last_corner=} {p=} {is_across=}")
                    if is_across:
                        side_status = not side_status
                    last_corner = None
                if side_status:
                    vl[j] = 'i'
                else:
                    vl[j] = 'o'
            elif i > 0 and visited[i-1][j] in [outside, inside]:
                vl[j] = visited[i-1][j]
            elif j > 0 and vl[j-1] in [outside, inside]:
                vl[j] = vl[j-1]
            elif side_status:
                vl[j] = inside
            else:
                vl[j] = outside

            if vl[j] == inside:
                count += 1
        print(f"{i=} {vl} {count=}")