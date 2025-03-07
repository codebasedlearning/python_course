# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses shallow and deep copies.

Teaching focus
  - It is very important to understand what it means to make copies and what
    shallow copies and deep copies actually are.
"""

import copy


def shallow_and_deep():
    """ shallow and deep copy of lists """
    print("\nshallow_and_deep\n================")

    data = [2, 3, 5]                                            # works on one object
    data_ref = data
    print(f" 1| ref:  {data=}, {data_ref=}, {(data == data_ref)=}, {(id(data)==id(data_ref))=}, {(data is data_ref)=}")

    data[2] = 7
    print(f" 2| 5->7: {data=}, {data_ref=}, {(data == data_ref)=}")

    data_cpy = list(data)                                       # creates a copy
    print(f" 3| cpy:  {data=}, {data_cpy=}, {(data == data_cpy)=}, {(id(data)==id(data_cpy))=}, {(data is data_cpy)=}")

    data[2] = 9
    print(f" 4| 7->9: {data=}, {data_cpy=}, {(data == data_cpy)=}")

    x23 = ['X', [23]]
    x23_cpy = list(x23)                                         # creates a copy but element [1] refers to a list
    print(f" 5| cpy?: {x23=}, {x23_cpy=}, {(x23 == x23_cpy)=}, {(id(x23)==id(x23_cpy))=}, {(x23 is x23_cpy)=}")

    x23[1][0] = 42                                              # affects both lists; btw. this is an error for mypy
    print(f" 6| ->42: {x23=}, {x23_cpy=}, {(x23 == x23_cpy)=}")

    y12 = ['Y', [12]]
    y12_deep = copy.deepcopy(y12)
    print(f" 7| deep: {y12=}, {y12_deep=}, {(y12 == y12_deep)=}, {(id(y12)==id(y12_deep))=}, {(y12 is y12_deep)=}")
    y12[1][0] = 24                                            # affects both lists; same error for mypy here
    print(f" 8| ->24: {y12=}, {y12_deep=}, {(y12 == y12_deep)=}")


if __name__ == "__main__":
    shallow_and_deep()


###############################################################################


"""
Summary

Topics
  - shallow and deep copy

Copy
  - A shallow copy creates a new object but does not copy the objects within it. 
    Instead, it only copies references to those objects.
  - If the elements are mutable, changes to them will be reflected across both 
    the original and the copy.
  - A deep copy creates a new object and recursively copies all objects contained 
    within it. This means the new object is completely independent of the original, 
    even if the objects inside are mutable.

See also
  - https://docs.python.org/3/library/copy.html
  - https://docs.python.org/3/reference/datamodel.html
"""
