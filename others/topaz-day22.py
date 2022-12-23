#!/usr/bin/env python3

from collections import defaultdict, Counter
from functools import lru_cache
import itertools
import math
import string
import sys
import timeit
import unittest

class Tests(unittest.TestCase):
	def setUp(self):
		self.testinput = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
		self.test = parse_input(self.testinput.split("\n"))
		self.test2 = parse_input2(self.testinput.split("\n"), True)

	def test_part1(self):
		self.assertEqual(part1(self.test), 6032)
		pass

	def test_part2(self):
		self.assertEqual(part2(self.test2), 5031)
		pass

def parse_input(i):
	map = []
	path = ""
	atpath = False
	maxlen = 0
	for line in i:
		if len(line.strip()) == 0:
			atpath = True
		elif atpath:
			path = line.strip()
		else:
			map.append(list(line.strip("\n")))
			maxlen = max(len(line), maxlen)
		pass
	for l in map:
		if len(l) < maxlen:
			while len(l) < maxlen:
				l.append(" ")
	return map, path

def part1(i):
	grid, instr = i[0], i[1]
	instrs = []
	ci = ""
	for c in instr:
		if c in ['L', 'R']:
			if ci != "":
				instrs.append(int(ci))
				ci = ""
			instrs.append(c)
		else:
			ci += c
	if ci != "":
		instrs.append(int(ci))
		ci = ""
	for i, c in enumerate(grid[0]):
		if c != " ":
			pos = (0, i)
			break
	dir = "right"
	for inst in instrs:
		pos, dir = apply_instr(pos, dir, grid, inst)
	dir_val = 0
	if dir == "right":
		dir_val = 0
	elif dir == "left":
		dir_val = 2
	elif dir == "up":
		dir_val = 1
	else:
		dir_val = 3
	return (1000 * (pos[0] + 1)) + (4 * (pos[1] + 1)) + dir_val

def get_dir(dir, posn, grid):
	curr_y = posn[0]
	curr_x = posn[1]
	if dir == "up":
		if curr_y == 0:
			pass
		else:
			if grid[curr_y - 1][curr_x] != " ":
				return (curr_y - 1, curr_x)
		for y in range(len(grid) - 1, -1, -1):
			if grid[y][curr_x] != " ":
				return (y, curr_x)
		assert False
	elif dir == "down":
		if curr_y == len(grid) - 1:
			pass
		else:
			if grid[curr_y + 1][curr_x] != " ":
				return (curr_y + 1, curr_x)
		for y in range(0, len(grid)):
			if grid[y][curr_x] != " ":
				return (y, curr_x)
		assert False
	elif dir == "left":
		if curr_x == 0:
			pass
		else:
			if grid[curr_y][curr_x - 1] != " ":
				return (curr_y, curr_x - 1)
		for x in range(len(grid[0]) - 1, -1, -1):
			if grid[curr_y][x] != " ":
				return (curr_y, x)
		assert False
	elif dir == "right":
		if curr_x == len(grid[0]) - 1:
			pass
		else:
			if grid[curr_y][curr_x + 1] != " ":
				return (curr_y, curr_x + 1)
		for x in range(0, len(grid[0])):
			if grid[curr_y][x] != " ":
				return (curr_y, x)
		assert False
	assert False

def apply_instr(pos, dir, grid, instr):
	if instr == "L":
		if dir == "right":
			return pos, "up"
		elif dir == "left":
			return pos, "down"
		elif dir == "up":
			return pos, "left"
		elif dir == "down":
			return pos, "right"
		else:
			assert False
	elif instr == "R":
		if dir == "right":
			return pos, "down"
		elif dir == "left":
			return pos, "up"
		elif dir == "up":
			return pos, "right"
		elif dir == "down":
			return pos, "left"
		else:
			assert False
	else:
		for i in range(instr):
			new_pos = get_dir(dir, pos, grid)
			if grid[new_pos[0]][new_pos[1]] == "#":
				return pos, dir
			else:
				pos = new_pos
		return pos, dir

def part2(i):
	faces, instr = i[0], i[1]
	instrs = []
	ci = ""
	for c in instr:
		if c in ['L', 'R']:
			if ci != "":
				instrs.append(int(ci))
				ci = ""
			instrs.append(c)
		else:
			ci += c
	if ci != "":
		instrs.append(int(ci))
		ci = ""
	pos = (49, 0)
	curr_face = 2
	dir = "right"
	t = 0
	for inst in instrs:
		t += 1
		pos, dir, curr_face = apply_instr2(pos, dir, faces, curr_face, inst)
	a = len(faces[1]) - (pos[0])
	b = pos[1] + 1
	if curr_face == 5:
		return 1000 * (100 + a) + (4 * (pos[1] + 1)) + dir_value(dir)


def apply_instr2(pos, dir, faces, curr_face, instr):
	y_max = len(faces[1]) - 1
	if instr == "L":
		if dir == "right":
			return pos, "up", curr_face
		elif dir == "left":
			return pos, "down", curr_face
		elif dir == "up":
			return pos, "left", curr_face
		elif dir == "down":
			return pos, "right", curr_face
		else:
			assert False
	elif instr == "R":
		if dir == "right":
			return pos, "down", curr_face
		elif dir == "left":
			return pos, "up", curr_face
		elif dir == "up":
			return pos, "right", curr_face
		elif dir == "down":
			return pos, "left", curr_face
		else:
			assert False
	else:
		for i in range(instr):
			new_pos, new_faceid, new_dir = right_face_from_pos(pos, dir, faces[curr_face], curr_face)
			if faces[new_faceid][y_max - new_pos[0]][new_pos[1]] == "#":
				return pos, dir, curr_face
			else:
				pos = new_pos
				dir = new_dir
				curr_face = new_faceid
		return pos, dir, curr_face


def test_getface(pos):
	y, x = pos[0], pos[1]
	if y <= 3:
		return (y, x), 1
	elif y >= 4 and y <= 7:
		if x >= 4 and x <= 7:
			return (y - 4, x - 4), 2
		elif x >= 8:
			return (y - 4, x - 8), 3
		else:
			return (y - 4, x), 6
	else:
		if x >= 4 and x <= 7:
			return (y - 8, x - 4), 4
		else:
			return (y - 8, x), 5

def pos_on_face(face, pos):
	return face[pos[0]][pos[1]]

def dir_value(dir):
	if dir == "right":
		return 0
	elif dir == "down":
		return 1
	elif dir == "left":
		return 2
	elif dir == "up":
		return 3
	else:
		assert False

# same side-perspective: invert y/x about center point, x/y becomes new edge value
# opposite side-perspective: same y/x, x/y becomes new edge-value
# perpendicular side-perspective:
# up -> left: y inv x, x 0
# up -> right y x, x max
# down -> left y x, x 0
# down -> right x inv x, x max
# to reverse:n

def right_face_from_pos(pos, dir, curr_face, curr_id):
	# Right, Left, Up, Down
	dct = {1: [4, 2, 6, 3], 2: [1, 5, 6, 3], 3: [4, 2, 1, 5], 4: [5, 1, 6, 3], 5: [2, 4, 6, 3], 6: [2, 4, 1, 5]}
	test_sides = {6: {"up": 1, "left": 4, "right": 2, "down": 5}, 3: {"up": 1, "right": 4, "left": 2, "down": 5}}
	real_sides = {6: {"up": 5, "left": 2, "right": 4, "down": 1}, 3: {"up": 5, "right": 2, "left": 5, "down": 1}}
	t = len(curr_face) < 10
	y, x = pos[0], pos[1]
	if dir == "left" and x > 0:
		np = (y, x - 1)
		return np, curr_id, dir
	elif dir == "right" and x < len(curr_face) - 1:
		np = (y, x + 1)
		return np, curr_id, dir
	elif dir == "down" and y > 0:
		np = (y - 1, x)
		return np, curr_id, dir
	elif dir == "up" and y < len(curr_face) - 1:
		np = (y + 1, x)
		return np, curr_id, dir

	new_face = curr_id
	x_max = len(curr_face) - 1
	y_max = x_max
	x_min = 0
	y_min = 0
	y_inv = y_max - y
	x_inv = x_max - x

	if dir == "left":
		new_pos = (y, x - 1)
	elif dir == "right":
		new_pos = (y, x + 1)
	elif dir == "down":
		new_pos = (y - 1, x)
	elif dir == "up":
		new_pos = (y + 1, x)

	new_dir = dir

	# lazy, assume t is false if not mentioned
	if curr_id == 1:
		if dir == "left":
			new_face = 2
			if x == 0:
				new_pos = (y, x_max)
		elif dir == "right":
			new_face = 4
			if x == x_max:
				new_pos = (y_inv, x_max)
				new_dir = "left"
		elif dir == "down":
			new_face = 3
			if y == 0:
				new_pos = (x_inv, x_max)
				new_dir = "left"
		elif dir == "up":
			new_face = 6
			if y == y_max:
				new_pos = (y_min, x)
	elif curr_id == 2:
		if dir == "left":
			if x == 0:
				new_face = 5
				new_pos = (y_inv, x_min)
				new_dir = "right"
		elif dir == "right":
			if x == x_max:
				new_face = 1
				new_pos = (y, x_min)
		elif dir == "down":
			if y == 0:
				new_face = 3
				new_pos = (y_max, x)
		elif dir == "up":
			if y == y_max:
				new_face = 6
				new_pos = (x_inv, x_min)
				new_dir = "right"
	elif curr_id == 3:
		if dir == "left":
			if x == 0:
				new_face = 5
				new_pos = (y_max, y_inv)
				new_dir = "down"
		elif dir == "right":
			if x == x_max:
				new_face = 1
				new_pos = (y_min, y_inv)
				new_dir = "up"
		elif dir == "down":
			if y == 0:
				new_face = 4
				new_pos = (y_max, x)
		elif dir == "up":
			if y == y_max:
				new_face = 2
				new_pos = (y_min, x)
	elif curr_id == 4:
		if dir == "left":
			if x == 0:
				new_face = 5
				new_pos = (y, x_max)
		elif dir == "right":
			if x == x_max:
				new_face = 1
				new_pos = (y_inv, x_max)
				new_dir = "left"
		elif dir == "down":
			if y == 0:
				new_face = 6
				new_pos = (x_inv, x_max)
				new_dir = "left"
		elif dir == "up":
			if y == y_max:
				new_face = 3
				new_pos = (y_min, x)
	elif curr_id == 5:
		if dir == "left":
			if x == 0:
				new_face = 2
				new_pos = (y_inv, x_min)
				new_dir = "right"
		elif dir == "right":
			if x == x_max:
				new_face = 4
				new_pos = (y, x_min)
		elif dir == "down":
			if y == 0:
				new_face = 6
				new_pos = (y_max, x)
		elif dir == "up":
			if y == y_max:
				new_face = 3
				new_pos = (x_inv, x_min)
				new_dir = "right"
	elif curr_id == 6:
		if dir == "left":
			if x == 0:
				new_face = 2
				new_pos = (y_max, y_inv)
				new_dir = "down"
		elif dir == "right":
			if x == x_max:
				new_face = 4
				new_pos = (y_min, y_inv)
				new_dir = "up"
		elif dir == "down":
			if y == 0:
				new_face = 1
				new_pos = (y_max, x)
		elif dir == "up":
			if y == y_max:
				new_face = 5
				new_pos = (y_min, x)
	return new_pos, new_face, new_dir






def real_getface(pos):
	y, x = pos[0], pos[1]
	if y <= 49:
		if x <= 49:
			return (y, x), 2
		else:
			return (y, x - 50), 1
	elif y >= 50 and y <= 99:
		return (y - 50, x), 3
	elif y >= 100 and y <= 149:
		if x <= 49:
			return (y - 100, x), 5
		else:
			return (y - 100, x - 50), 4
	else:
		return (y - 150, x), 6

def parse_input2(i, istest):
	faces = [None]
	size = 4 if istest else 50
	for _ in range(6):
		f = []
		for _ in range(size):
			r = []
			for _ in range(size):
				r.append(" ")
			f.append(r)
		faces.append(f)
	f_height = 3 if istest else 4
	y = 0
	for line in i:
		x = 0
		if y == (f_height * size):
			y += 1
			continue
		elif y == (f_height * size) + 1:
			path = line.strip()
			return faces, path
		for c in line.strip("\n"):
			if c == " ":
				continue
			if istest:
				face_pos, face_id = test_getface((y, x))
			else:
				face_pos, face_id = real_getface((y, x))
			faces[face_id][face_pos[0]][face_pos[1]] = c
			x += 1
		x = 0
		y += 1
	y = 0

def main():
	t0 = timeit.default_timer()
	with open(sys.argv[1], "r") as f:
		i = parse_input(f.readlines())
	print(part1(i))
	t1 = timeit.default_timer()
	with open(sys.argv[1], "r") as f:
		i = parse_input2(f.readlines(), False)
	print(part2(i))
	t2 = timeit.default_timer()
	if len(sys.argv) > 2:
		print(f"Part 1: {t1 - t0} seconds")
		print(f"Part 2: {t2 - t1} seconds")

if __name__ == '__main__':
	if len(sys.argv) < 2:
		unittest.main()
	else:
		main()
