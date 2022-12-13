# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 10:15:49 2022

@author: Connor

--- Day 11: Monkey in the Middle ---
As you finally start making your way upriver, you realize your pack is much
lighter than you remember. Just then, one of the items from your pack goes
flying overhead. Monkeys are playing Keep Away with your missing things!

To get your stuff back, you need to be able to predict where the monkeys will
throw your items. After some careful observation, you realize the monkeys
operate based on how worried you are about each item.
"""

import numpy as np
import operator

is_test = False
is_testb = False
fn = f"input11{'b' if is_testb and is_test else ''}.txt"
with open(fn if not is_test else f"test_{fn}", "r") as fh:
    data = [data.strip() for data in fh.readlines()]

class Monkey:
    def __init__(self, notes):
        self.__count = 0
        for note in notes:
            if "Starting items" in note:
                items = note.split(": ")[1]
                self.items = [int(item) for item in items.split(", ")]
            elif "Operation" in note:
                if "+" in note:
                    self.op = operator.add
                    op_char = "+"
                elif "*" in note:
                    self.op = operator.mul
                    op_char = "*"
                elif "-" in note:
                    op_char = "-"
                    self.op = operator.sub
                elif "/" in note:
                    op_char = "/"
                    self.op = operator.div
                else:
                    pass
                if note.split(f"{op_char} ")[1].isnumeric():
                    self.var = int(note.split(f"{op_char} ")[1])
                else:
                    self.var = note.split(f"{op_char} ")[1]
            elif "Test" in note:
                self.div_test = int(note.split("by ")[1])
            elif "true" in note:
                self.pass_throw = int(note[-1])
            elif "false" in note:
                self.fail_throw = int(note[-1])
            else:
                pass
    def __repr__(self):
        return f"{self.items}"

    def turn(self, monkeys):
        for item in self.items:
            # print(f"1. {item=}")
            item = self.inspect(item)
            # print(f"2. {item=}")
            item = self.bored(item)
            # print(f"3. {item=}")
            if self.test(item):
                monkeys[self.pass_throw].give_item(item)
            else:
                monkeys[self.fail_throw].give_item(item)

        self.items.clear()

    def inspect(self, item):
        self.__count += 1
        if self.var == "old":
            item = self.op(item, item)
        else:
            item = self.op(item, self.var)
        return item

    def bored(self, item):
        item = item // 3
        return item

    def test(self, item):
        return item % self.div_test == 0

    def give_item(self, item):
        self.items.append(item)

    def get_count(self):
        return self.__count

# Monkey Factory :)
# monkeys = []
# for item in data:
#     if "Monkey" in item:
#         new_notes = list()
#     elif item:
#         new_notes.append(item)
#     else:
#         monkeys.append(Monkey(new_notes))
# monkeys.append(Monkey(new_notes))

# num_rounds = 20
# for rnd in range(num_rounds):
#     for monkey in monkeys:
#         monkey.turn(monkeys)

# counts = sorted([monkey.get_count() for monkey in monkeys])
# print(f"Monkey Business = {counts[-1] * counts[-2]}")

"""
--- Part Two ---
You're worried you might not ever get your items back. So worried, in fact,
that your relief that a monkey's inspection didn't damage an item no longer
causes your worry level to be divided by three.

Unfortunately, that relief was all that was keeping your worry levels from
reaching ridiculous levels. You'll need to find another way to keep your worry
levels manageable.

At this rate, you might be putting up with these monkeys for a very long
time - possibly 10000 rounds!
"""

# Try to the math work with just modulos, but I am not seeing how to do so
# without making the "big number" when its tossed, since other monkey isn't
# going to have the same div_test...
OVERALL_DIVISOR = 1

class NewMonkey:
    def __init__(self, notes):
        self.__count = 0
        for note in notes:
            if "Starting items" in note:
                items = note.split(": ")[1]
                # self.items = [Item(int(item)) for item in items.split(", ")]
                self.items = [int(item) for item in items.split(", ")]
            elif "Operation" in note:
                if "+" in note:
                    self.op = operator.add
                    op_char = "+"
                elif "*" in note:
                    self.op = operator.mul
                    op_char = "*"
                elif "-" in note:
                    op_char = "-"
                    self.op = operator.sub
                elif "/" in note:
                    op_char = "/"
                    self.op = operator.div
                else:
                    pass
                if note.split(f"{op_char} ")[1].isnumeric():
                    self.var = int(note.split(f"{op_char} ")[1])
                else:
                    self.var = note.split(f"{op_char} ")[1]
            elif "Test" in note:
                self.div_test = int(note.split("by ")[1])
            elif "true" in note:
                self.pass_throw = int(note[-1])
            elif "false" in note:
                self.fail_throw = int(note[-1])
            else:
                pass

    def __repr__(self):
        return f"{self.items}"

    def turn(self, monkeys):
        for item in self.items:
            # print(f"1. {item=}")
            item = self.inspect(item)
            # print(f"2. {item=}")
            if self.test(item) == 0:
                monkeys[self.pass_throw].give_item(item)
            else:
                monkeys[self.fail_throw].give_item(item)

        self.items.clear()

    def inspect(self, item):
        self.__count += 1
        if self.var == "old":
            out = self.op(item, item)
        else:
            out = self.op(item, self.var)
        return out

    def test(self, item, use_overall=False):
        if use_overall:
            return item % OVERALL_DIVISOR
        else:
            return item % self.div_test

    def give_item(self, item):
        self.items.append(self.test(item, True))

    def get_count(self):
        return self.__count


# Monkey Factory :)
monkeys = []
for item in data:
    if "Monkey" in item:
        new_notes = list()
    elif item:
        new_notes.append(item)
    else:
        monkeys.append(NewMonkey(new_notes))
monkeys.append(NewMonkey(new_notes))

for monkey in monkeys:
    OVERALL_DIVISOR *= monkey.div_test

num_rounds = 10000
for rnd in range(num_rounds):
    for monkey in monkeys:
        monkey.turn(monkeys)
    print(f"Done with round {rnd+1}...")

counts = sorted([monkey.get_count() for monkey in monkeys])
print(f"Monkey Business = {counts[-1] * counts[-2]}")
