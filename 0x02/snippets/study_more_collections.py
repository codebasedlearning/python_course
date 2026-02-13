# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses ranges, sets, tuples, defaultdicts, and more collections.

Teaching focus
  - The range operations are similar to those of a tuple.
  - The set operations are similar to those of a list or dictionary.
  - Hashable keys are needed for dictionaries. Therefore we need an immutable set -> frozenset.

Summary

Ranges
  - Excludes the last element.
  - Often used for iteration.
  - No operators such as union.

Sets
  - Sets do not support indexing or slicing, so many list-style operations
    (e.g., `data[0]`, `del data[index]`, `reverse`, `sort`) are not available.
  - Sets cannot be used as dictionary key, frozensets can.

Tuples
  - Can contain data of different type.
  - Immutable.
  - Suitable data types for grouping multiple values where neither the
    content nor the number changes, for example in the case of return values.

Defaultdict
  - A `defaultdict` is a subclass of Python's built-in `dict` that provides
    a convenient way to handle missing keys by automatically supplying
    a default value for those keys.
  - Normally, if you try to access a key in a regular dictionary that doesn't
    exist, Python raises a `KeyError`. With a `defaultdict`, however,
    it automatically creates a default value for the missing key using
    a function (called a `default_factory`) that you specify when creating
    the `defaultdict`.

Counter
  - A dict subclass for counting hashable objects.
  - Supports arithmetic, most_common(), and initialization from iterables.

deque
  - Double-ended queue with O(1) append/pop on both ends.
  - Thread-safe, supports maxlen for bounded buffers.

ChainMap
  - Groups multiple dicts into a single lookup.
  - Writes go to the first dict only — useful for layered config.

See also
  - https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
  - https://www.w3schools.com/python/ref_func_range.asp
  - https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset
  - https://www.w3schools.com/python/python_tuples.asp
  - https://docs.python.org/3/library/collections.html#collections.defaultdict
  - https://docs.python.org/3/library/collections.html#collections.Counter
  - https://docs.python.org/3/library/collections.html#collections.deque
  - https://docs.python.org/3/library/collections.html#collections.ChainMap
"""

from collections import ChainMap, Counter, defaultdict, deque
from typing import Any

from utils import print_function_header


@print_function_header
def using_ranges():
    """ range basics """

    data = range(5)                         # ranges, immutable
    # data: range = range(5)                                    # with type hint
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")
    print(f" 2| {data.start=}, {data.stop=}, {data.step=}")

    middle = range(-2, 3)
    print(f" 3| {middle=}, {len(middle)=}")
    print(f" 4| {middle.start=}, {middle.stop=}, {middle.step=}")

    odds = range(3,11,2)
    print(f" 5| {odds=}, {len(odds)=}")
    print(f" 6| {odds.start=}, {odds.stop=}, {odds.step=}")


@print_function_header
def non_modifying_range_ops():
    """ non-modifying range operations """

    data = range(3,11,2)                    # 3,5,7,9 excl. 11
    print(f" 1| {data=}")
    print(f" 2| {data[2]=}")                # index access, 0-based, read
    print(f" 3| {data.index(5)=}")          # find or exception
    print(f" 4| {(5 in data)=}, {(6 in data)=}")                # contains
    print(f" 5| {(11 not in data)=}")       # contains not

    rg147 = range(1, 10, 3)                 # 1,4,7 excl. 10
    print(f" 6| traverse {rg147=}:      ")
    print("      ", end='')
    for n in rg147:                         # traverse
        print(f"[it]={n} ", end='')
    print()
    print("      ", end='')
    for i, n in enumerate(rg147):           # traverse with index
        print(f"i,[i]={i},{n} ", end='')
    print()

@print_function_header
def using_sets():
    """ set basics """

    data = {1, "two", 3, "four"}            # sets, mutable, unordered, objects of different type
    # data: set[int | str] = {1, "two", 3, "four"}
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")


@print_function_header
def non_modifying_set_ops():
    """ non-modifying set operations """

    data = {2, 3, 5, "seven"}
    print(f" 1| {data=}")
    print(f" 2| {(5 in data)=}, {(6 in data)=}")                # contains
    print(f" 3| {(11 not in data)=}")       # contains not

    print(" 4| traverse: ", end='')
    for n in data:                          # traverse
        print(f"{n=} ", end='')
    print()
    print(" 5| enumerate: ", end='')
    for i, n in enumerate(data):            # traverse with index
        print(f"{i=},{n=} ", end='')
    print()


@print_function_header
def modifying_set_ops():
    """ modifying set operations """

    data = {2, 3, 5}
    print(f" 1| {data=}")

    data.add(3)
    data.add(7)                             # add an element but only once
    print(f" 2| add 3?, add 7: {data=}")

    data.update({11, 13, 17})               # add multiple elements
    print(f" 3| update [11,13,17]: {data=}")

    data.discard(13)                        # remove an element safely (no error if not found)
    print(f" 4| discard 13: {data=}")

    data.remove(11)                         # remove an element (raises error if not found)
    print(f" 5| remove 11: {data=}")

    item = data.pop()                       # remove an arbitrary element, useful e.g. in
    print(f" 6| pop arbitrary: {data=}, {item=}")               # an iterative process

    data.clear()                            # remove all
    print(f" 7| clear: {data=}")

    # first typical set ops - more in the next function

    data = {1, 3, 5} | {2, 4, 6, 7}         # union of two sets
    print(f" 8| union {{1,3,5}} with {{2,4,6,7}}: {data=}")

    # data = data - {3, 5}
    data -= {3, 5}                          # subtract (no error if not found)
    print(f" 9| difference with {{3,5}}: {data=}")


@print_function_header
def typical_set_ops():
    """ typical set operations """

    data1 = {1, 1, 2, 3, 5, 8, 13}          # noqa: B033
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


@print_function_header
def why_frozensets():
    """ why frozensets are useful """

    data = frozenset({2, 3, 5, "seven"})
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")
    print(f" 2| {(5 in data)=}, {(6 in data)=}, etc.")          # same as set

    # Example: Graph Edges in an Undirected Graph. A 'frozenset' represents
    # an edge in an undirected graph since the order of vertices doesn't matter.
    graph_edges = {
        frozenset({1, 2}): 5,               # Edge between 1 and 2 with weight 5
        frozenset({2, 3}): 10,              # Edge between 2 and 3 with weight 10
        frozenset({1, 3}): 7,               # Edge between 1 and 3 with weight 7
    }
    weight = graph_edges[frozenset({2, 1})]                     # same as {1, 2}
    print(f" 3| {weight=}")


@print_function_header
def using_tuples():
    """ tuple basics """

    data = (2, 3, 5, "seven")               # tuples, immutable
    # data: tuple[int, int, int, str] = (2, 3, 5, "seven")      # with type hint
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")

    single = (1, )                          # needed, as '(1)' is '1' and not a tuple, cf. list
    print(f" 2| {single=}")


@print_function_header
def non_modifying_tuple_ops():
    """ non-modifying tuple operations """

    data = (2, 3, 5, "seven")
    print(f" 1| {data=}")
    print(f" 2| {data[1]=}")                # index access, 0-based, read
    print(f" 3| {data.index(3)=}")          # find or exception
    print(f" 4| {(5 in data)=}, {(6 in data)=}")                # contains
    print(f" 5| {(11 not in data)=}")       # contains not

    def load_data():
        return True, 23                     # return type is a tuple,
    result = load_data()                    # check with debug
    # error, data = load_data()                                 # usually this way
    print(f" 6| {result=}")

    print(" 7| traverse: ", end='')
    for n in data:  # traverse
        print(f"{n=} ", end='')
    print()

    print(f" 8| slicing: {data[-2:]=}")     # start=length-2, end=length(excl.), cf. string



@print_function_header
def using_defaultdict():
    """ test the defaultdict class """

    frequency:defaultdict = defaultdict(int)    # defaultdict with int (default value is 0)

    # count words; note that a missing key automatically generates a (key,0) entry
    words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
    for word in words:
        frequency[word] += 1
    print(f" 1| {frequency=}")

"""
Topic: Counter — counting things
"""


@print_function_header
def using_counter():
    """ Counter: the Pythonic way to count things """

    # create from an iterable
    words = "the quick brown fox jumps over the lazy fox".split()
    counts = Counter(words)
    print(f" 1| {counts}")
    print(f" 2| most common 2: {counts.most_common(2)}")

    # Counter from a string (counts characters)
    letters = Counter("mississippi")
    print(f" 3| letters: {letters}")

    # arithmetic on counters
    inventory_a = Counter(apples=3, oranges=2)
    inventory_b = Counter(apples=1, bananas=4)
    combined = inventory_a + inventory_b
    diff = inventory_a - inventory_b        # drops zero and negative
    print(f" 4| combined: {combined}")
    print(f" 5| diff (a-b): {diff}")

    # total count (Python 3.10+)
    print(f" 6| total items: {counts.total()}")


"""
Topic: deque — double-ended queue
"""


@print_function_header
def using_deque():
    """ deque: O(1) append and pop on both ends """

    # list.pop(0) is O(n), deque.popleft() is O(1)
    d = deque([1, 2, 3])
    d.appendleft(0)                         # add to the left
    d.append(4)                             # add to the right
    print(f" 1| after appends: {d}")

    left = d.popleft()
    right = d.pop()
    print(f" 2| popped: left={left}, right={right}, remaining={d}")

    # rotation
    d = deque([1, 2, 3, 4, 5])
    d.rotate(2)                             # rotate right by 2
    print(f" 3| rotated right 2: {d}")
    d.rotate(-2)
    print(f" 4| rotated back:    {d}")

    # bounded deque: maxlen drops oldest items
    recent:deque[int] = deque(maxlen=3)
    for i in range(5):
        recent.append(i)
    print(f" 5| bounded (maxlen=3): {recent}")      # keeps only last 3


"""
Topic: ChainMap — layered dictionaries
"""


@print_function_header
def using_chainmap():
    """ ChainMap: layered lookup across multiple dicts """

    # typical use case: config with defaults, env overrides, CLI overrides
    defaults = {"color": "blue", "size": 10, "verbose": False}
    env_config = {"color": "green", "debug": True}
    cli_args = {"verbose": True}

    config:ChainMap[str,Any] = ChainMap(cli_args, env_config, defaults)

    print(f" 1| color:   {config['color']}")        # 'green' (from env, not defaults)
    print(f" 2| size:    {config['size']}")          # 10 (from defaults, not overridden)
    print(f" 3| verbose: {config['verbose']}")       # True (from cli, highest priority)
    print(f" 4| debug:   {config['debug']}")         # True (from env)

    # writes go to the FIRST dict only
    config["new_key"] = 42
    print(f" 5| cli_args after write: {cli_args}")   # {'verbose': True, 'new_key': 42}
    print(f" 6| defaults unchanged: {defaults}")

    # list all unique keys
    print(f" 7| all keys: {list(config.keys())}")


if __name__ == "__main__":
    using_ranges()
    non_modifying_range_ops()

    using_sets()
    non_modifying_set_ops()
    modifying_set_ops()
    typical_set_ops()
    why_frozensets()
    using_tuples()
    non_modifying_tuple_ops()
    using_defaultdict()
    using_counter()
    using_deque()
    using_chainmap()
