# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses Flag enums and bitwise combination of flag values.

Teaching focus
  - combining flags with the Flag enum
  - bitwise operations (|, &, <<) on flag values
  - a chmod-style example: r/w/x bits shifted into owner/group/other slots

Flag
  - Flag is a special Enum subclass: members can be combined with bitwise
    operators (|, &, ^, ~) to form composite values.
  - Useful for permission masks, feature toggles, and any 'set of options'
    that you want to pack into a single value.

See also
  - https://docs.python.org/3/howto/enum.html
  - https://docs.python.org/3/library/enum.html#enum.Flag
  - d_enums.py — for the regular Enum and @unique / auto basics.
"""

from enum import Flag, auto

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
