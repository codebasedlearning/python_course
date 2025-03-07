# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses sets and set operations.

Teaching focus
  - This topic is part of the self-study during the exercises or at home.
  - The set operations are similar to those of a list or dictionary.
  - Hashable keys are needed for dictionaries. Therefor we need an immutable set -> frozenset.
"""


def using_sets():
    """ set basics """
    print("\nusing_sets\n===========")

    data = {1, "two", 3, "four"}                                 # sets, mutable, unordered, objects of different type
    # data: set[int | str] = {1, "two", 3, "four"}
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")


def non_modifying_set_ops():
    """ non-modifying set operations """
    print("\nnon_modifying_set_ops\n=====================")

    data = {2, 3, 5, "seven"}
    print(f" 1| {data=}")
    print(f" 2| {(5 in data)=}, {(6 in data)=}")                # contains
    print(f" 3| {(11 not in data)=}")                           # contains not

    print(" 4| traverse: ", end='')
    for n in data:                                              # traverse
        print(f"{n=} ", end='')
    print()
    print(" 5| enumerate: ", end='')
    for i, n in enumerate(data):                                # traverse with index
        print(f"{i=},{n=} ", end='')
    print()


def modifying_set_ops():
    """ modifying set operations """
    print("\nmodifying_set_ops\n=================")

    data = {2, 3, 5}
    print(f" 1| {data=}")

    data.add(3)
    data.add(7)                                                 # add an element but only once
    print(f" 2| add 3?, add 7: {data=}")

    data.update({11, 13, 17})                                   # add multiple elements
    print(f" 3| update [11,13,17]: {data=}")

    data.discard(13)                                            # remove an element safely (no error if not found)
    print(f" 4| discard 13: {data=}")

    data.remove(11)                                             # remove an element (raises error if not found)
    print(f" 5| remove 11: {data=}")

    item = data.pop()                                           # remove an arbitrary element, useful e.g. in
    print(f" 6| pop arbitrary: {data=}, {item=}")               # an iterative process

    data.clear()                                                # remove all
    print(f" 7| clear: {data=}")

    # first typical set ops - more in the next function

    data = {1, 3, 5} | {2, 4, 6, 7}                             # union of two sets
    print(f" 8| union {{1,3,5}} with {{2,4,6,7}}: {data=}")

    # data = data - {3, 5}
    data -= {3, 5}                                              # subtract (no error if not found)
    print(f" 9| difference with {{3,5}}: {data=}")


def typical_set_ops():
    """ typical set operations """
    print("\ntypical_set_ops\n===============")

    data1 = {1, 1, 2, 3, 5, 8, 13}                              # pylint: disable=duplicate-value
    data2 = {8, 13, 21}
    data3 = {3, 5, 8}

    print(f" 1| sets: {data1=}, {data2=}, {data3=}")
    print(f" 2| union12 |: {data1 | data2}")                    # data1.union(data2)
    print(f" 3| intersection12 &: {data1 & data2}")             # data1.intersection(data2)
    print(f" 4| difference12 -: {data1 - data2}")               # data1.difference(data2)
    print(f" 5| symmetric_difference12 ^: {data1 ^ data2}")     # data1.symmetric_difference(data2)
    print(f" 6| issubset31 <=: {data3 <= data1}")               # data3.issubset(data1)
    print(f" 7| issuperset13 >=: {data1 >= data3}")             # data1.issuperset(data3)
    print(f" 8| isdisjoint12: {data1.isdisjoint(data2)}")


def why_frozensets():
    """ why frozensets are useful """
    print("\nwhy_frozensets\n==============")

    data = frozenset({2, 3, 5, "seven"})
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")
    print(f" 2| {(5 in data)=}, {(6 in data)=}, etc.")          # same as set

    # Example: Graph Edges in an Undirected Graph. A 'frozenset' represents
    # an edge in an undirected graph since the order of vertices doesn't matter.
    graph_edges = {
        frozenset({1, 2}): 5,                                   # Edge between 1 and 2 with weight 5
        frozenset({2, 3}): 10,                                  # Edge between 2 and 3 with weight 10
        frozenset({1, 3}): 7,                                   # Edge between 1 and 3 with weight 7
    }
    weight = graph_edges[frozenset({2, 1})]                     # same as {1, 2}
    print(f" 3| {weight=}")


if __name__ == "__main__":
    using_sets()
    non_modifying_set_ops()
    modifying_set_ops()
    typical_set_ops()
    why_frozensets()


###############################################################################


"""
Summary

Topics
  - sets
  - typical set operations
  - frozensets
  - enumerate

Set
  - Sets do not support indexing or slicing, so many list-style operations 
    (e.g., `data[0]`, `del data[index]`, `reverse`, `sort`) are not available.
  - Sets cannot be used as dictionary key, frozensets can.

Fun Fact
  - A first version of this set-snippet was created from AI Assistant with: 
    "Can you create code similar to the one below, (code with 'list' was given) 
    but now using sets instead of lists?"
    AI: "Sure, here's a similar code but this time using sets: ..."  :-)

See also
  - https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset
"""
