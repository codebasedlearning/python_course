# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses lists and list operations.

Teaching focus
  - The 'using_lists' function is discussed in detail, as its structure is
    a template for the others.
  - Non-modifying and modifying operations are the core of collections.
"""


def using_lists():
    """ list basics """
    print("\nusing_lists\n===========")

    data = [2, 3, 5, "seven"]                                   # lists, mutable, objects of different type
    # data: list[int | str] = [2, 3, 5, "seven"]                # with type hint
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")

    single = [1, ]                                              # =[1] both lists, cf. tuple
    print(f" 2| {single=}")


def non_modifying_list_ops():
    """ non-modifying list operations """
    print("\nnon_modifying_list_ops\n======================")

    data = [2, 3, 5, "seven"]
    print(f" 1| {data=}")
    print(f" 2| {data[1]=}")                                    # index access, 0-based, read
    print(f" 3| {data.index(3)=}")                              # find or exception
    print(f" 4| {(5 in data)=}, {(6 in data)=}")                # contains
    print(f" 5| {(11 not in data)=}")                           # contains not

    print(" 6| traverse: ", end='')
    for n in data:                                              # traverse
        print(f"{n=} ", end='')
    print()

    print(f" 7| slicing: {data[-2:]=}")                         # start=length-2, end=length(ecl.), comp. string


def modifying_list_ops():
    """ modifying list operations """
    print("\nmodifying_list_ops\n==================")

    data = [2, 3, 5]
    print(f" 1| {data=}")

    data[0] = 1                                                 # write
    print(f" 2| set [0]=1: {data}")

    data.append(7)                                              # add to the end
    print(f" 3| append 7: {data}")

    data.extend([11, 13, 17])                                   # add all
    print(f" 4| extend [11, 13, 17]: {data}")

    data.remove(13)                                             # remove object
    print(f" 5| remove 13: {data}")

    item = data.pop(2)                                          # remove at index, returns element
    print(f" 6| pop at 2: {data}, item={item}")

    data.reverse()                                              # in-place
    print(f" 7| reverse: {data}")

    data.sort()                                                 # in-place
    print(f" 8| sort: {data}")

    data.clear()                                                # surprise
    print(f" 9| clear: {data}")

    data = [1, 3, 5] + [2, 4, 6, 8]                             # op+
    print(f"10| +: {data}")

    del data[3]                                                 # like pop but without returning element
    print(f"11| del [3]: {data}")

    del data[1:4:2]                                             # remove index 1, 3
    print(f"12| del [1:4:2]: {data}")

    del data[:]                                                 # all indices, i.e. clear
    print(f"13| del [:]: {data}")


if __name__ == "__main__":
    using_lists()
    non_modifying_list_ops()
    modifying_list_ops()


###############################################################################


"""
Summary

Topics
  - lists
  - non-modifying operations
  - modifying operations

Lists
  - can contain data of different type
  - each element in a list is a reference to an object stored elsewhere in memory, not the object itself
  - modifying a mutable (!) object inside a list affects all references to that object
  - mutable
  - can be traversed
  - can be sliced
  - can be modified
  - can be copied

See also
  - https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
  - https://www.w3schools.com/python/python_lists_methods.asp
"""
