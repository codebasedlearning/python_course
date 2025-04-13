# (C) 2023 A.Voß, a.voss@fh-aachen.de, python@codebasedlearning.dev

""" This example shows a first use (!) of 'enums'. """

from enum import Enum, Flag, auto, unique


class DrinkConsts:                                                  # (A) class constants
    TEA = 11
    COFFEA = 22


@unique
class Drink(Enum):                                                  # (B) Enum, unique, extends
    TEA = 11
    COFFEA = 22


def show_drinks():
    print(f"01| DrinkConsts: Tea={DrinkConsts.TEA}, Coffea={DrinkConsts.COFFEA}\n")
    print(f"02| Drinks:")
    for drink in Drink:
        print(f"      Drink: {drink}, name:{drink.name}, value:{drink.value}")

    dv22 = Drink(22)
    dn22 = Drink.COFFEA
    print(f"03| access by value: {dv22}, and name: {dn22}")
    print()


class ColorId(Enum):
    RED = auto()                                                    # auto means, start with 1
    GREEN = auto()
    BLUE = auto()


ColorFunc = Enum('Color2', ['RED2', 'GREEN2', 'BLUE2'])             # functional syntax


def show_colors():
    print(f"04| ColorId:")
    for colorId in ColorId:
        print(f"      Color: {colorId}, name:{colorId.name}, value:{colorId.value}")
    print(f"05| ColorFunc:")
    for color in ColorFunc:
        print(f"      Color: {color}, name:{color.connection_string}, value:{color.value}")
    print()


class ChModFlag(Flag):                                              # models file modes from 'chmod' command
    X = auto()
    W = auto()
    R = auto()
    ALL = R | W | X                                                 # combine flags
    U_shift = 6                                                     # owner
    G_shift = 3                                                     # group
    O_shift = 0                                                     # other


def show_flags():
    print(f"06| Flags:")
    for flag in ChModFlag:
        print(f"      Flag: {flag}, name:{flag.name}, value:{flag.value}")

    mode = ((ChModFlag.W | ChModFlag.R).value << ChModFlag.U_shift.value) \
        + (ChModFlag.R.value << ChModFlag.G_shift.value) \
        + (ChModFlag.R.value << ChModFlag.O_shift.value)
    print(f"07| chmod u+rw g+r o+r = {oct(mode)}")


def print_all():
    show_drinks()
    show_colors()
    show_flags()


if __name__ == "__main__":
    print_all()

"""
# (A) class constants
In principle, you can define constants as class variables. The class is then a kind of namespace.
Iterating over all constants is not that easy. This is better done with an 'enum'.

(B) Enum
The class 'Enum' brings some convenience in dealing with the constants. 
Without the @unique decorator, an equal value would also be possible.

More on Enums can be found here:
    https://docs.python.org/3/howto/enum.html
    https://docs.python.org/3/library/enum.html
"""
