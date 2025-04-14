# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses enums.

Teaching focus
  - define and work with various enums
"""

from enum import Enum, auto, unique


class DrinkConsts:
    """ class constants; pro/con? """
    TEA = 11
    COFFEA = 22

@unique
class Drink(Enum):
    """ unique enum values, i.e. no duplicates """
    TEA = 11
    COFFEA = 22
    # WATER = 22                            # throws if already known

class ColorId(Enum):
    """ auto-incrementing, unique values, starting with 1 """
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    WHITE = 255
    EXTRA_WHITE = auto()                    # increments from 255

class Defaults(Enum):                       # pylint complains about not being UPPERCASE
    """ different types """
    URL = "https://www.google.com"
    Port = 8080
    User = "<USER>"
    Password = "<PASSWORD>"

def work_with_enums():
    """ show different enum examples """
    print("\nwork_with_enums\n===============")

    print(f" 1| just class consts: {DrinkConsts.TEA=}, {DrinkConsts.COFFEA=}")

    tea = Drink.TEA
    print(f" 2| use as enum: {tea=}")

    coconut22 = Drink(22)                   # throws if unknown
    coffea = Drink.COFFEA
    print(f" 3| access by value: {coconut22=}, or name: {coffea=}\n")

    print(" 4| enumerate Drinks:")
    for drink in Drink:
        print(f"      drink={drink}, {drink=}, {drink.name=}, {drink.value=}")

    print(" 5| enumerate ColorIds:")
    for colorId in ColorId:
        print(f"      {colorId=}")

    print(" 6| enumerate Defaults:")
    for item in Defaults:
        print(f"      {item=}")


def show_internals():
    """ note the dicts """
    print("\nshow_internals\n=============")

    print(f" 1| DrinkConsts: {DrinkConsts.__dict__}")
    print(f" 2| Drinks: {Drink.__dict__}")


if __name__ == "__main__":
    work_with_enums()
    show_internals()


###############################################################################


"""
Summary

Topics
  - enums, unique, auto

class constants
  - In principle, you can define constants as class variables. The class 
    is then a kind of namespace. Iterating over all constants is not 
    that easy. This is better done with an 'enum'.

Enum
  - The class 'Enum' brings some convenience in dealing with the constants. 
    Without the @unique decorator, an equal value would be possible.

See also
  - https://docs.python.org/3/howto/enum.html
  - https://docs.python.org/3/library/enum.html
"""
