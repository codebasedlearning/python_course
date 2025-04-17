# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses a special enum case with flags.
"""

from enum import Flag, auto


class ChModFlag(Flag):                      # models file modes from 'chmod' command
    """ enum with flags """
    X = auto()
    W = auto()
    R = auto()
    ALL = R | W | X                         # combine flags
    U_shift = 6                             # owner
    G_shift = 3                             # group
    O_shift = 0                             # other


def show_enums_with_flags():
    """ test our class """
    print("\nshow_enums_with_flags\n=====================")

    print(" 1| Flags:")
    for flag in ChModFlag:
        print(f"      Flag: {flag}, name:{flag.name}, value:{flag.value}")

    mode = ((ChModFlag.W | ChModFlag.R).value << ChModFlag.U_shift.value) \
        + (ChModFlag.R.value << ChModFlag.G_shift.value) \
        + (ChModFlag.R.value << ChModFlag.O_shift.value)
    print(f" 2| chmod u+rw g+r o+r = {oct(mode)}")


if __name__ == "__main__":
    show_enums_with_flags()


###############################################################################


"""
Summary
  - In this special case you can also combine flags.
  
See also
    https://docs.python.org/3/howto/enum.html
    https://docs.python.org/3/library/enum.html
"""
