# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses dictionaries and dictionary operations.

Teaching focus
  - Although the complexity and method names are different, the operations
    are essentially very similar to those from the list.
"""


def using_dicts():
    """ dict basics """
    print("\nusing_dicts\n===========")

    data = {1: "one", 2: "two", 3: "three", "four": 4}          # dictionary (key-value), mutable
    # data: dict[str, str] = {1: "one", 2: "two", 3: "three", "four": 4}
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")


def non_modifying_dict_ops():
    """ non-modifying dictionary operations """
    print("\nnon_modifying_dict_ops\n======================")

    data = {1: "one", 2: "two", 3: "three", "four": 4}
    print(f" 1| {data=}")
    print(f" 2| {data[1]=}")                                    # access, key-based
    print(f" 3| {data.get(33, '-')=}")                          # access with default (or None)
    print(f" 4| {(4 in data)=}")                                # contains
    print(f" 5| {(11 not in data)=}")                           # contains not

    print(" 6| traverse: ", end='')
    for k, v in data.items():                                   # traverse items, assign item to k(key),v(value)
        print(f"[{k}]={v} ", end='')
    print()

    print(f" 7| {data.keys()=}")                                # all keys
    print(f" 8| {data.values()=}")                              # all values
    print(f" 9| {data.items()=}")                               # all pairs


def modifying_dict_ops():
    """ modifying dictionary operations """
    print("\nmodifying_dict_ops\n==================")

    data = {1: "one", 2: "two", 3: "three", "four": 4}
    print(f" 1| {data=}")

    data[1] = "1"                                               # write new value
    print(f" 2| set [1]='1': {data=}")

    data.update({5: "five", 6: "six"})                          # add all, extend
    print(f" 3| update 5 and 6: {data=}")

    item = data.pop(3)
    print(f" 4| pop 3: {item=}, {data=}")                       # remove object with key 3, item is value

    del data[5]                                                 # remove object with key 5
    print(f" 5| del [5]: {data=}")

    # no slicing or sorting here

    data.clear()
    print(f" 6| clear: {data=}")


if __name__ == "__main__":
    using_dicts()
    non_modifying_dict_ops()
    modifying_dict_ops()


###############################################################################


"""
Summary

Topics
  - dictionaries
  - non-modifying operations
  - modifying operations

Dictionaries
  - Dictionaries are an essential part of Python. Not only as associative containers, 
    but also in connection with objects, classes, and the (yet unknown) '__dict__'.

See also
  - https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
  - https://www.w3schools.com/python/python_dictionaries.asp
"""
