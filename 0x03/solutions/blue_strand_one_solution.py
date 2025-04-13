# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Blue Strand'

Topics
  - class
  - property
  - staticmethod
"""

import random


class Dice:
    """ simple dice class with history """
    total_rolls = 0

    def __init__(self, sides=6):
        self.sides = sides
        self._history = []

    def roll(self):
        """ creates a roll and stores it in history """
        result = random.randint(1, self.sides)
        Dice.total_rolls += 1
        self._history.append(result)
        return result

    @property
    def history(self):
        """ returns history """
        return list(self._history)  # prevent modification

    @staticmethod
    def roll_multiple(n, sides=6):
        """ rolls n times and returns a list """
        dice = Dice(sides)
        return [dice.roll() for _ in range(n)]

    def __repr__(self):
        return f"({self.__dict__})"

def roll_the_dice():
    """ test Dice class and properties """
    d20 = Dice(20)
    print(f" 1| {d20=}")

    saving_throw = d20.roll()
    attack_roll = d20.roll()
    print(f" 2| {saving_throw=}, {attack_roll=}, {d20.history=}")

    d12 = Dice()
    damage = d12.roll()
    print(f" 3| {d12=}, {damage=}, {d12.history=}")

    print(f" 4| {Dice.total_rolls=}")

    fire = Dice.roll_multiple(n=5, sides=6)
    print(f" 5| {fire=}")
    print(f" 6| {Dice.total_rolls=}")

if __name__ == '__main__':
    roll_the_dice()
