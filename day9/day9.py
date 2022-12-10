# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 19:08:29 2022

@author: Connor

--- Day 9: Rope Bridge ---
This rope bridge creaks as you walk along it. You aren't sure how old it is, or
whether it can even support your weight.

It seems to support the Elves just fine, though. The bridge spans a gorge which
was carved out by the massive river far below you.

You step carefully; as you do, the ropes stretch and twist. You decide to
distract yourself by modeling rope physics; maybe you can even figure out
where not to step.

Consider a rope with a knot at each end; these knots mark the head and the tail
of the rope. If the head moves far enough away from the tail, the tail is
pulled toward the head.

Due to nebulous reasoning involving Planck lengths, you should be able to model
the positions of the knots on a two-dimensional grid. Then, by following a
hypothetical series of motions (your puzzle input) for the head, you can
determine how the tail will move.

Due to the aforementioned Planck lengths, the rope must be quite short; in
fact, the head (H) and tail (T) must always be touching (diagonally adjacent
and even overlapping both count as touching):

....
.TH.
....

....
.H..
..T.
....

...
.H. (H covers T)
...

If the head is ever two steps directly up, down, left, or right from the tail,
the tail must also move one step in that direction so it remains close enough:

.....    .....    .....
.TH.. -> .T.H. -> ..TH.
.....    .....    .....

...    ...    ...
.T.    .T.    ...
.H. -> ... -> .T.
...    .H.    .H.
...    ...    ...

Otherwise, if the head and tail aren't touching and aren't in the same row or
column, the tail always moves one step diagonally to keep up:

.....    .....    .....
.....    ..H..    ..H..
..H.. -> ..... -> ..T..
.T...    .T...    .....
.....    .....    .....

.....    .....    .....
.....    .....    .....
..H.. -> ...H. -> ..TH.
.T...    .T...    .....
.....    .....    .....

You just need to work out where the tail goes as the head follows a series of
motions. Assume the head and the tail both start at the same position,
overlapping.
"""

import numpy as np
# from itertools import product

is_test = False
fn = "input9.txt"
with open(fn if not is_test else f"test_{fn}", "r") as fh:
    data = [(data.strip().split()[0], int(data.strip().split()[1])) for data in fh.readlines()]

class Rope:
    def __init__(self, head_xy=(0,0), tail_xy=(0,0)):
        self.hx, self.hy = head_xy
        self.tx, self.ty = tail_xy

    def move_right(self):
        self.hx += 1

    def move_left(self):
        self.hx -= 1

    def move_up(self):
        self.hy += 1

    def move_down(self):
        self.hy -= 1

    def h_to_t_dist(self):
        return int(np.floor(np.sqrt((self.hx-self.tx)**2 + (self.hy-self.ty)**2)))

    def move_tail(self):
        delta_x = self.hx - self.tx
        delta_y = self.hy - self.ty
        self.tx += np.sign(delta_x)
        self.ty += np.sign(delta_y)

    def get_tail(self):
        return self.tx, self.ty

visits = {(0,0): True}

rope = Rope()
for direction, cnt in data:
    for cc in range(cnt):
        if direction == "U":
            rope.move_up()
        elif direction == "R":
            rope.move_right()
        elif direction == "D":
            rope.move_down()
        elif direction == "L":
            rope.move_left()
        else:
            pass
        if rope.h_to_t_dist() > 1:
            rope.move_tail()
            visits[rope.get_tail()] = True

print(sum(visits.values()))


"""
A rope snaps! Suddenly, the river is getting a lot closer than you remember.
The bridge is still there, but some of the ropes that broke are now whipping
toward you as you fall through the air!

The ropes are moving too quickly to grab; you only have a few seconds to choose
how to arch your body to avoid being hit. Fortunately, your simulation can be
extended to support longer ropes.

Rather than two knots, you now must simulate a rope consisting of ten knots.
One knot is still the head of the rope and moves according to the series of
motions. Each knot further down the rope follows the knot in front of it using
the same rules as before.
"""
# Gotta improve my old class, but can use the same structure roughly...
class Rope:
    def __init__(self, start=(0,0), length=10):
        self.knots = np.ones((length,2))
        self.knots[:,0] = start[0]
        self.knots[:,1] = start[1]

    def move_right(self):
        self.knots[0,0] += 1

    def move_left(self):
        self.knots[0,0] -= 1

    def move_up(self):
        self.knots[0,1] += 1

    def move_down(self):
        self.knots[0,1] -= 1

    def move_segments(self):
        for ii, knot in enumerate(self.knots[1:]):
            delta_x = self.knots[ii,0] - knot[0]
            delta_y = self.knots[ii,1] - knot[1]
            if int(np.floor(np.sqrt(delta_x**2 + delta_y**2))) > 1:
                knot[0] += np.sign(delta_x)
                knot[1] += np.sign(delta_y)

    def get_tail(self):
        return int(self.knots[-1][0]), int(self.knots[-1][1])

visits2 = {(0,0): True}

rope = Rope(length=10)
for direction, cnt in data:
    for cc in range(cnt):
        if direction == "U":
            rope.move_up()
        elif direction == "R":
            rope.move_right()
        elif direction == "D":
            rope.move_down()
        elif direction == "L":
            rope.move_left()
        else:
            pass
        rope.move_segments()
        visits2[rope.get_tail()] = True

print(sum(visits2.values()))
