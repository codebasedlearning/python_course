# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses tuples and tuple operations.

Teaching focus
  - This topic is part of the self-study during the exercises or at home.
  - The tuple operations are similar to those of an immutable list.
"""


def using_tuples():
    """ tuple basics """
    print("\nusing_tuples\n=============")

    data = (2, 3, 5, "seven")                                   # tuples, immutable
    # data: tuple[int, int, int, str] = (2, 3, 5, "seven")      # with type hint
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")

    single = (1, )                                              # needed, as '(1)' is '1' and not a tuple, cf. list
    print(f" 2| {single=}")


def non_modifying_tuple_ops():
    """ non-modifying tuple operations """
    print("\nnon_modifying_tuple_ops\n=======================")

    data = (2, 3, 5, "seven")
    print(f" 1| {data=}")
    print(f" 2| {data[1]=}")                                    # index access, 0-based, read
    print(f" 3| {data.index(3)=}")                              # find or exception
    print(f" 4| {(5 in data)=}, {(6 in data)=}")                # contains
    print(f" 5| {(11 not in data)=}")                           # contains not

    def load_data():
        return True, 23                                         # return type is a tuple,
    result = load_data()                                        # check with debug
    # error, data = load_data()                                 # usually this way
    print(f" 6| {result=}")

    print(" 7| traverse: ", end='')
    for n in data:  # traverse
        print(f"{n=} ", end='')
    print()

    print(f" 8| slicing: {data[-2:]=}")                         # start=length-2, end=length(ecl.), comp. string


if __name__ == "__main__":
    using_tuples()
    non_modifying_tuple_ops()


###############################################################################


"""
Summary

Topics
  - tuples
  - non-modifying operations

Tuple
  - Can contain data of different type.
  - Immutable.
  - Suitable data types for grouping multiple values where neither the 
    content nor the number changes, for example in the case of return values.

See also
  - https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
  - https://www.w3schools.com/python/python_tuples.asp
"""
