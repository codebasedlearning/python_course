# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses collection types and their most used operations.

Teaching focus
  - collection types, i.e. lists, dictionaries
  - preview: tuples, sets, frozensets
  - non-modifying operations
  - modifying operations
  - shallow copies and deep copies
  - variable unpacking, extended Iterable Unpacking

Lists
  - can contain data of different type
  - each element in a list is a reference to an object stored elsewhere in memory,
    not the object itself
  - modifying a mutable (!) object inside a list affects all references to that
    object
  - mutable
  - can be traversed, sliced, modified, copied
  - tuple operations are similar to those of an immutable list.
  - https://www.w3schools.com/python/python_lists_methods.asp

Dictionaries
  - Dictionaries are an essential part of Python. Not only as
    associative containers, but also in connection with objects, classes,
    and the (yet unknown) '__dict__'.
  - Mixed key types are allowed (not recommended), both are hashed internally.
  - Keys are unique, values can be repeated.
  - Can be traversed, sliced, modified, copied.
  - https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
  - https://www.w3schools.com/python/python_dictionaries.asp

Tuples, Sets, Frozen Sets
  - See `study_more_collections.py` for more details.

Copy
  - A shallow copy creates a new object but does not copy the objects within it.
    Instead, it only copies references to those objects.
  - If the elements are mutable, changes to them will be reflected across both
    the original and the copy.
  - A deep copy creates a new object and recursively copies all objects contained
    within it. This means the new object is completely independent of the original,
    even if the objects inside are mutable.
  - https://docs.python.org/3/library/copy.html
  - https://docs.python.org/3/reference/datamodel.html

Unpacking
  - In Python, 'unpacking' or 'variable unpacking' is the most commonly used
    and official term for this concept. Other names are 'Multiple Variable Assignment',
    'Destructuring Assignment', 'Decomposition'.
  - First use of the '*'-Operator, aka 'Extended Iterable Unpacking'.
  - https://docs.python.org/3/reference/simple_stmts.html#assignment-statements
"""

import copy

from utils import print_function_header

"""
Topic: Collections
"""

@print_function_header
def using_lists():
    """ list basics. """

    numbers = [1,1,2,3,5,8,13]              # List, mutable.
    print(f" 1| {numbers=}, {len(numbers)=}, {type(numbers)=}")

    data: list[int | str] = [2,3,5,"seven"] # List with type hint, here objects of different type.
    print(f" 2| {data=}")

    single = [1, ]                          # =[1] cf. tuple.
    print(f" 3| {single=}")

@print_function_header
def non_modifying_list_ops():
    """ Non-modifying list operations. """

    data = [2,3,5,"seven"]
    print(f" 1| {data=}")
    print(f" 2| {data[1]=}")                # Index access, 0-based, read.
    print(f" 3| {data.index(5)=}")          # Find value 5 or throw.
    print(f" 4| {(5 in data)=}")            # Contains?
    print(f" 5| {(11 not in data)=}")       # Contains not?
    print(f" 6| slicing: {data[-2:]=}")     # start=length-2, end=length(excl.), cf. string.

    print(" 7| traverse: ", end='')
    for n in data:                          # Traverse.
        print(f"{n=} ", end='')
    print()

@print_function_header
def modifying_list_ops():
    """ Modifying list operations. """

    data = [2, 3, 5]
    print(f" 1| {data=}")

    data[0] = 1                             # Write access, 0-based.
    print(f" 2| set data[0]=1: {data}")

    data.append(7)                          # Add to the end.
    print(f" 3| append 7: {data}")

    data.extend([11, 13, 17])               # Add all.
    print(f" 4| extend [11, 13, 17]: {data}")

    data.remove(13)                         # Remove element.
    print(f" 5| remove 13: {data}")

    item = data.pop(2)                      # Remove at index, return element.
    print(f" 6| pop at 2: {data}, item={item}")

    data.reverse()                          # In-place.
    print(f" 7| reverse: {data}")

    data.sort()                             # In-place.
    print(f" 8| sort: {data}")

    data.clear()                            # In-place.
    print(f" 9| clear: {data}")

    data = [1, 3, 5] + [2, 4, 6, 8]         # op+
    print(f"10| +: {data}")

    del data[3]                             # Like pop but without returning element.
    print(f"11| del [3]: {data}")

    del data[1:4:2]                         # Remove index from 1 until 4 (excl.), step 2, i.e. index 1 and 3.
    print(f"12| del [1:4:2]: {data}")

    del data[:]                             # All indices, i.e. clear.
    print(f"13| del [:]: {data}")

@print_function_header
def using_dicts():
    """ dict basics. """

    data = {1: "one", 2: "two", 3: "three", "four": 4}
    # data: dict[str, str] = ...            # dictionary (key-value), mutable, here with type hints.
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")

@print_function_header
def non_modifying_dict_ops():
    """ Non-modifying dictionary operations. """

    data = {1: "one", 2: "two", 3: "three", "four": 4}
    print(f" 1| {data=}")
    print(f" 2| {data[1]=}")                # Access, key-based.
    print(f" 3| {data.get(33, '-')=}")      # Access with default (or None)
    print(f" 4| {(4 in data)=}")            # Contains?
    print(f" 5| {(11 not in data)=}")       # Contains not?

    print(f" 6| {data.keys()=}")            # All keys.
    print(f" 7| {data.values()=}")          # All values.
    print(f" 8| {data.items()=}")           # All key-value pairs.
    print(" 9| traverse: ", end='')

    for k, v in data.items():               # Traverse items, assign item to k(key),v(value).
        print(f"[{k}]={v} ", end='')
    print()

@print_function_header
def modifying_dict_ops():
    """ Modifying dictionary operations. """

    data = {1: "one", 2: "two", 3: "three", "four": 4}
    print(f" 1| {data=}")

    data[1] = "1"                           # Write new value.
    print(f" 2| set [1]='1': {data=}")

    data.update({5: "five", 6: "six"})      # Add all, extend, but also overwrites existing keys.
    print(f" 3| update 5 and 6: {data=}")

    item = data.pop(3)
    print(f" 4| pop 3: {item=}, {data=}")   # Remove element with key 3, item is value.

    del data[5]                             # Remove element with key 5.
    print(f" 5| del [5]: {data=}")

    # No slicing or sorting here.

    data.clear()
    print(f" 6| clear: {data=}")

@print_function_header
def collections_preview():
    """ Preview: more collections. """

    rg = range(5)                           # Range, immutable.
    print(f" 1| {rg=}, {len(rg)=}, {type(rg)=}")
    print(f" 2| {rg.start=}, {rg.stop=}, {rg.step=}")

    data = {1, 1, 2, 3, 5, 8, 13}           # Set, mutable # noqa: B033
    print(f" 3| {data=}, {len(data)=}, {type(data)=}")

    fset = frozenset({2, 3, 5, "seven"})    # Frozen set, immutable.
    print(f" 4| {fset=}, {len(fset)=}, {type(fset)=}")

    tup = (2, 3, 5, "seven")               # Tuple, immutable.
    print(f" 5| {tup=}, {len(tup)=}, {type(tup)=}")


"""
Topic: Shallow and deep copy
"""

@print_function_header
def shallow_and_deep():
    """ Shallow and deep copy of lists. """

    data = [2, 3, 5]                        # Work on one list.
    data_ref = data
    print(f" 1| ref:  {data=}, {data_ref=}, {(data == data_ref)=}, {(id(data)==id(data_ref))=}, {(data is data_ref)=}")

    data[2] = 7
    print(f" 2| 5->7: {data=}, {data_ref=}, {(data == data_ref)=}")

    data_cpy = list(data)                   # Creates a copy, or: data.copy(), or: data[:]
    print(f" 3| cpy:  {data=}, {data_cpy=}, {(data == data_cpy)=}, {(id(data)==id(data_cpy))=}, {(data is data_cpy)=}")

    data[2] = 9
    print(f" 4| 7->9: {data=}, {data_cpy=}, {(data == data_cpy)=}")

    x23 = ['X', [23]]                       # Better for type-safety: x23: tuple[str, list[int]] = ("X", [23])
    x23_cpy = list(x23)                     # Creates a copy but element [1] refers to a list.
    print(f" 5| cpy?: {x23=}, {x23_cpy=}, {(x23 == x23_cpy)=}, {(id(x23)==id(x23_cpy))=}, {(x23 is x23_cpy)=}")

    # Affects both lists (an error for mypy as it infers something like: x23: list[object])
    x23[1][0] = 42                          # type: ignore[index]
    print(f" 6| ->42: {x23=}, {x23_cpy=}, {(x23 == x23_cpy)=}")

    y12 = ['Y', [12]]
    y12_deep = copy.deepcopy(y12)
    print(f" 7| deep: {y12=}, {y12_deep=}, {(y12 == y12_deep)=}, {(id(y12)==id(y12_deep))=}, {(y12 is y12_deep)=}")
    # Does not affect the deep copy (same error for mypy here)
    y12[1][0] = 24                          # type: ignore[index]
    print(f" 8| ->24: {y12=}, {y12_deep=}, {(y12 == y12_deep)=}")


"""
Topic: Unpacking
"""

@print_function_header
def variable_unpacking():
    """ Variable unpacking (multiple variable assignment). """

    x, y = 1, 2                             # Component by component, destructuring assignment.
    print(f" 1| x,y=1,2: {x=}, {y=}")

    x, y = y, x                             # No need for a temp.
    print(f" 2| swap x,y: {x=}, {y=}")

    def load_data():
        return True, [1,2,3]
    error, data = load_data()               # Standard use case.
    print(f" 3| error,data: {error=}, {data=}")

    triple = [1, 2, 3]
    a, _, c = triple                        # '_' means 'unused', it is discarded; _ _ is also possible.
    print(f" 4| a,_,c={triple} -> {a=}, {c=}")

    values = [1, 2, 3, 4, 5]
    x1, x2, *xn = values                    # '*' means 'rest'.
    print(f" 5| x1,x2,*xn={values} -> {x1=}, {x2=}, {xn=}")

    dct = {1: "one", 2: "two"}
    print(" 6| for k,v in dict:", end='')
    for k, v in dct.items():                # Standard use case.
        print(f" {{k={k}, v={v}}}", end='')
    print()


if __name__ == "__main__":
    # Collections
    using_lists()
    non_modifying_list_ops()
    modifying_list_ops()
    using_dicts()
    non_modifying_dict_ops()
    modifying_dict_ops()
    collections_preview()
    # Copies
    shallow_and_deep()
    # Unpacking
    variable_unpacking()
