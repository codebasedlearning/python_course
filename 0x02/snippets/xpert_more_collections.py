# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses more collections.

Teaching focus
  - Hashable keys are needed for dictionaries. Therefore we need an immutable set -> frozenset.


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
    using_defaultdict()
    using_counter()
    using_deque()
    using_chainmap()
