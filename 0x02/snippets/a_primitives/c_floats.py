# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses floats.

Teaching focus
  - It is structured like the int-snippet, i.e. first some conversions and
    basic operations, then some special stuff.
  - 'nan', 'inf'
  - Pylint
"""

# pylint: disable=(comparison-with-itself)
import math


def using_floats():
    """ float basics """
    print("\nusing_floats\n============")

    d = 2.5                                                     # 'd' references a floating point number
    # d: float = 2.5                                            # with type hint
    print(f" 1| {d=}, {type(d)=}")

    # cast to float
    print(f" 2| {float(23)=}, {float("3.1415")=}, {float(True)=}")


def special_floats_and_ops():
    """ special floats nan and inf  """
    print("\nspecial_floats_and_ops\n======================")

    nan = float('nan')
    print(f" 1| {nan=}, {math.isnan(nan)=}")                    # nan = not-a-number

    inf = float('inf')                                          # same for "-inf"
    print(f" 2| {inf=}, {math.isinf(inf)=}")

    # be careful here
    d = 2.5
    print(f" 3| {d=}, {(d == d)=}, {(nan == nan)=}, {(inf == inf)=}, {(d < inf)=}")
    print(f" 4| {(d+nan)=}, {(d+inf)=}, {(inf-inf)=}, {(1/inf)=}")


if __name__ == "__main__":
    using_floats()
    special_floats_and_ops()


###############################################################################


"""
Summary

Topics
  - floats
  - nan, inf

Floats
  - Almost all Python variants implement 'float' according to IEEE-754 "double precision",
    i.e. as a standard 'double'.
  - Constants like 'inf' can sometimes be used to initialize variables in algorithms.
  - Be aware that operations with 'nan' or 'inf' may result in strange or unexpected behavior.
    Any operation with 'nan' results in 'nan'. For 'inf' it depends.

See also
  - https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
"""
