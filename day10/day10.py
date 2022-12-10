# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 23:55:22 2022

@author: Connor

--- Day 10: Cathode-Ray Tube ---
You avoid the ropes, plunge into the river, and swim to shore.

The Elves yell something about meeting back up with them upriver, but the
river is too loud to tell exactly what they're saying. They finish crossing the
bridge and disappear from view.

Situations like this must be why the Elves prioritized getting the
communication system on your handheld device working. You pull it out of your
pack, but the amount of water slowly draining from a big crack in its screen
tells you it probably won't be of much immediate use.

Unless, that is, you can design a replacement for the device's video system! It
seems to be some kind of cathode-ray tube screen and simple CPU that are both
driven by a precise clock circuit. The clock circuit ticks at a constant rate;
each tick is called a cycle.

Start by figuring out the signal being sent by the CPU. The CPU has a single
register, X, which starts with the value 1. It supports only two instructions:

addx V takes two cycles to complete. After two cycles, the X register is
increased by the value V. (V can be negative.)

noop takes one cycle to complete. It has no other effect.

The CPU uses these instructions in a program (your puzzle input) to, somehow,
tell the screen what to draw.

Consider the following small program:

noop
addx 3
addx -5

Execution of this program proceeds as follows:

At the start of the first cycle, the noop instruction begins execution.
During the first cycle, X is 1. After the first cycle, the noop instruction
finishes execution, doing nothing.

At the start of the second cycle, the addx 3 instruction begins execution.
During the second cycle, X is still 1.

During the third cycle, X is still 1. After the third cycle, the addx 3
instruction finishes execution, setting X to 4.

At the start of the fourth cycle, the addx -5 instruction begins execution.
During the fourth cycle, X is still 4.
During the fifth cycle, X is still 4. After the fifth cycle, the addx -5
instruction finishes execution, setting X to -1.

Maybe you can learn something by looking at the value of the X register
throughout execution. For now, consider the signal strength
(the cycle number multiplied by the value of the X register) during the 20th
cycle and every 40 cycles after that
(that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles).
"""

import numpy as np
# from itertools import product

is_test = False
is_testb = False
fn = f"input10{'b' if is_testb and is_test else ''}.txt"
with open(fn if not is_test else f"test_{fn}", "r") as fh:
    data = [data.strip() for data in fh.readlines()]

useful_cycles = [20, 60, 100, 140, 180, 220]
cycle_count = 1
x = 1
strengths = []
for item in data:
    # print(f"Before cycle {cycle_count}: {x=}")
    if cycle_count in useful_cycles:
        strengths.append(cycle_count * x)
    if "addx" in item:
        cycle_count += 1
        # print(f"After cycle {cycle_count-1}: {x=}")
        # print(f"Before cycle {cycle_count}: {x=}")
        if cycle_count in useful_cycles:
            strengths.append(cycle_count * x)
        cycle_count += 1
        x += int(item.split()[1])
    else:
        cycle_count += 1
    # print(f"After cycle {cycle_count-1}: {x=}")

print(sum(strengths))

"""
--- Part Two ---
It seems like the X register controls the horizontal position of a sprite.
Specifically, the sprite is 3 pixels wide, and the X register sets the
horizontal position of the middle of that sprite. (In this system, there is no
such thing as "vertical position": if the sprite's horizontal position puts its
pixels where the CRT is currently drawing, then those pixels will be drawn.)

You count the pixels on the CRT: 40 wide and 6 high. This CRT screen draws the
top row of pixels left-to-right, then the row below that, and so on. The
left-most pixel in each row is in position 0, and the right-most pixel in each
row is in position 39.
"""
cycle_count = 1
x = 1
crt_grid = np.zeros((6,40))
row = 0
for item in data:
    col = (cycle_count-1) % 40

    crt_grid[row][col] = col in [x-1, x, x+1]
    if (cycle_count % 40) == 0:
        row += 1
    if "addx" in item:
        cycle_count += 1

        col = (cycle_count-1) % 40

        crt_grid[row][col] = col in [x-1, x, x+1]
        if (cycle_count % 40) == 0:
            row += 1
        cycle_count += 1
        x += int(item.split()[1])
    else:
        cycle_count += 1

def print_grid(crt_grid):
    r,c = crt_grid.shape
    for rr in range(r):
        for cc in range(c):
            if crt_grid[rr][cc]:
                print("#", end="")
            else:
                print(" ", end="")
        print("")

print_grid(crt_grid)
