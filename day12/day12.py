# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 12:00:09 2022

@author: Connor

--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're
following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input).
The heightmap shows the local area from above broken into a grid; the elevation
of each square of the grid is given by a single lowercase letter, where a is
the lowest elevation, b is the next-lowest, and so on up to the highest
elevation, z.

Also included on the heightmap are marks for your current position (S) and the
location that should get the best signal (E). Your current position (S) has
elevation a, and the location that should get the best signal (E) has
elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as
possible. During each step, you can move exactly one square up, down, left, or
right. To avoid needing to get out your climbing gear, the elevation of the
destination square can be at most one higher than the elevation of your current
square; that is, if your current elevation is m, you could step to elevation n,
but not to elevation o. (This also means that the elevation of the destination
square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle. You
could start by moving down or right, but eventually you'll need to head toward
the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square
moving up (^), down (v), left (<), or right (>). The location that should get
the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the
location that should get the best signal?
"""
# Implement A star
# parse grid s.t. start location is known, and all the heights are known as
# ints, not chars
import numpy as np
import operator

is_test = False
is_testb = False
fn = f"input12{'b' if is_testb and is_test else ''}.txt"
with open(fn if not is_test else f"test_{fn}", "r") as fh:
    data = [data.strip() for data in fh.readlines()]

def get_height(char: str):
    if char.islower():
        return ord(char)-ord("a")
    elif char == "S":
        return 0
    elif char == "E":
        return 25

num_rows, num_cols = len(data), len(data[0])
grid = np.zeros((num_rows, num_cols))
for r, item in enumerate(data):
    for c, char in enumerate(item):
        if char == "S":
            start = (r,c)
        if char == "E":
            end = (r,c)
        grid[r,c] = get_height(char)


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, value, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.value = value

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(maze[start[0],start[1]], None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(maze[end[0],end[1]], None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    print("starting...")

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # print(f"Looking at {current_node.position}")

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(1, 0), (0, 1), (-1, 0), (0, -1)]: # Adjacent squares, not (-1, -1), (-1, 1), (1, -1), (1, 1)

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within valid range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain (skip if delta is bigger than 1)
            if maze[node_position[0]][node_position[1]] - current_node.value > 1:
                continue

            # Make sure its not the same as current parent, if it is, skip it
            if current_node.parent is not None:
                if node_position == current_node.parent.position:
                    continue

            # Make sure new node is not in

            # Create new node
            new_node = Node(maze[node_position[0],node_position[1]], current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            # for closed_child in closed_list:
            #     if child == closed_child:
            #         continue\
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list:
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

            # Add the child to the open list
            open_list.append(child)



path = astar(grid, start, end)
print(path)

#%% Oh god what is happening
import matplotlib.pyplot as plt
x = np.arange(0, grid.shape[1], 1)
y = np.arange(0, grid.shape[0], 1)
h = plt.contourf(x,y,grid, levels=25)
xp = [pt[1] for pt in path]
yp = [pt[0] for pt in path]
plt.plot(xp,yp)
plt.gca().invert_yaxis()
plt.show()

plt.figure()
h = plt.contourf(x,y,grid==1, levels=2)
xp = [pt[1] for pt in path]
yp = [pt[0] for pt in path]
plt.plot(xp,yp)
plt.gca().invert_yaxis()
plt.show()

# Hohkay, so this code gets REAL close to the correct answer.
# BUT IT ISN'T EXACTLY RIGHT
# It gets a path of len(401) (400 steps)
# however, its greedier than I want it to be, and instead of fixing I visually
# inspected to see how many points it was greedy, which was 3 points where it
# made 2 unneccessary turns, which means that the real answer should be
# 400-6=394 (which it was!)

# For Part 2, I noticed that the ONLY way onto the grid from an A height cell,
# was the left side. As such, I found the only place it could realistically
# start visually. And got the answer to be 6 more steps less, at 388 steps.
