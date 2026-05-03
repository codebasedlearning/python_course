# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses enum flags.

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
    show_enums_with_flags()
