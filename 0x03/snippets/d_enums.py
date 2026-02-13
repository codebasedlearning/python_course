# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses enums and enum flags.

Teaching focus
  - define and work with various enums
  - combining flags with Flag enum

Class constants
  - In principle, you can define constants as class variables. The class
    is then a kind of namespace. Iterating over all constants is not
    that easy. This is better done with an 'enum'.

Enum
  - The class 'Enum' brings some convenience in dealing with the constants.
    Without the @unique decorator, an equal value would be possible.

Flag
  - In this special case you can also combine flags, e.g. for bitwise
    operations like file permissions.

See also
  - https://docs.python.org/3/howto/enum.html
  - https://docs.python.org/3/library/enum.html
"""

from enum import Enum, Flag, auto, unique

from utils import print_function_header

"""
Topic: Enums
"""


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
    Password = "<PASSWORD>"                 # placeholder, never store real credentials in code

@print_function_header
def work_with_enums():
    """ show different enum examples """

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


@print_function_header
def show_internals():
    """ note the dicts """

    print(f" 1| DrinkConsts: {DrinkConsts.__dict__}")
    print(f" 2| Drinks: {Drink.__dict__}")


"""
Topic: Enum flags
"""


class ChModFlag(Flag):                      # models file modes from 'chmod' command
    """ enum with flags """
    X = auto()
    W = auto()
    R = auto()
    ALL = R | W | X                         # combine flags
    U_shift = 6                             # owner
    G_shift = 3                             # group
    O_shift = 0                             # other


@print_function_header
def show_enums_with_flags():
    """ test our class """

    print(" 1| Flags:")
    for flag in ChModFlag:
        print(f"      Flag: {flag}, name:{flag.name}, value:{flag.value}")

    mode = ((ChModFlag.W | ChModFlag.R).value << ChModFlag.U_shift.value) \
        + (ChModFlag.R.value << ChModFlag.G_shift.value) \
        + (ChModFlag.R.value << ChModFlag.O_shift.value)
    print(f" 2| chmod u+rw g+r o+r = {oct(mode)}")


if __name__ == "__main__":
    # Enums
    work_with_enums()
    show_internals()

    # Enum flags
    show_enums_with_flags()
