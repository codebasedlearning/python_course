# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses ranges and range operations.

Teaching focus
  - This topic is part of the self-study during the exercises or at home.
  - The range operations are similar to those of a tuple.
  - Often used for iteration.
"""


def using_ranges():
    """ range basics """
    print("\nusing_ranges\n============")

    data = range(5)                                             # ranges, immutable
    # data: range = range(5)                                    # with type hint
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")
    print(f" 2| {data.start=}, {data.stop=}, {data.step=}")

    middle = range(-2, 3)
    print(f" 3| {middle=}, {len(middle)=}")
    print(f" 4| {middle.start=}, {middle.stop=}, {middle.step=}")

    odds = range(3,11,2)
    print(f" 5| {odds=}, {len(odds)=}")
    print(f" 6| {odds.start=}, {odds.stop=}, {odds.step=}")


def non_modifying_range_ops():
    """ non-modifying range operations """
    print("\nnon_modifying_range_ops\n=======================")

    data = range(3,11,2)                                        # 3,5,7,9 excl. 11
    print(f" 1| {data=}")
    print(f" 2| {data[2]=}")                                    # index access, 0-based, read
    print(f" 3| {data.index(5)=}")                              # find or exception
    print(f" 4| {(5 in data)=}, {(6 in data)=}")                # contains
    print(f" 5| {(11 not in data)=}")                           # contains not

    rg147 = range(1, 10, 3)                                     # 1,4,7 excl. 10
    print(f" 6| traverse {rg147=}:      ")
    print("      ", end='')
    for n in rg147:                                             # traverse
        print(f"[it]={n} ", end='')
    print()
    print("      ", end='')
    for i, n in enumerate(rg147):                               # traverse with index
        print(f"i,[i]={i},{n} ", end='')
    print()


if __name__ == "__main__":
    using_ranges()
    non_modifying_range_ops()


###############################################################################


"""
Summary

Topics
  - ranges
  - non-modifying operations

Range
  - Excludes the last element.
  - Often used for iteration.
  - No operators such as union.

See also
  - https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
  - https://www.w3schools.com/python/ref_func_range.asp
"""
