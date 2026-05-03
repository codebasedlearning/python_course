# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses data classes and named tuples.

Teaching focus
  - using special data oriented classes
  - comparison with NamedTuple

Dataclass
  - Simple data storage classes containing the 'usual' methods such as
    initialisation, output, comparison operators are tedious to write.
  - The `dataclass' decorator selectively generates such methods for the class
    if they are not specified.
  - Without example: There are 'members' such as 'KW_ONLY', defining keyword-only
    parameters.

__slots__
  - By default, Python stores instance attributes in a per-instance dictionary
    called __dict__. This allows dynamic attribute creation but uses more memory.
  - __slots__ declares a fixed set of allowed attributes, replacing __dict__
    with a more compact internal structure.
  - Using __slots__ prevents adding arbitrary attributes at runtime and can
    improve memory usage and attribute access speed.

NamedTuple
  - NamedTuple is an alternative for simple immutable data containers.
  - Like dataclass, it generates __repr__, __eq__, and supports type hints.
  - Unlike dataclass, instances are immutable by default (they are tuples),
    can be used as dictionary keys, and have less memory overhead.

Prefer NamedTuple for small, immutable records; prefer dataclass for
mutable objects or when you need methods and post-init logic.

See also
  - https://docs.python.org/3/library/dataclasses.html
  - https://realpython.com/python-data-classes/
  - https://docs.python.org/3/library/typing.html#typing.NamedTuple
"""

import sys
from typing import NamedTuple
from utils import print_function_header

class SlottedPerson:
    """ person class with __slots__ instead of __dict__ """
    __slots__ = ('name', 'age')

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"SlottedPerson({self.name!r}, {self.age})"


@print_function_header
def show_slots():
    """ __slots__ vs __dict__ """

    sp = SlottedPerson("Eve", 30)
    print(f" 1| {sp=}, {sp.name=}, {sp.age=}")

    try:
        sp.hobby = "chess"                  # AttributeError: no __dict__
    except AttributeError as e:
        print(f" 2| cannot add attribute: {e}")

    print(f" 3| has __dict__: {hasattr(sp, '__dict__')}")
    print(f" 4| has __slots__: {sp.__slots__=}")

    print(f" 5| {sys.getsizeof(sp)=}")
    #person = Person("Alice", 20)
    #p#rint(f" 6| {sys.getsizeof(person)=}, {sys.getsizeof(person.__dict__)=})")


"""
Topic: NamedTuple comparison
"""


class PointNT(NamedTuple):
    """ an immutable 2D point as NamedTuple """
    x: int
    y: int


@print_function_header
def compare_with_namedtuple():
    """ dataclass vs NamedTuple """

    #p_dc = Point(x=1, y=2)
    p_nt = PointNT(x=1, y=2)

    #print(f" 1| dataclass: {p_dc=}, {type(p_dc)=}")
    print(f" 2| namedtuple: {p_nt=}, {type(p_nt)=}")

    # NamedTuple supports tuple unpacking
    x, y = p_nt
    print(f" 3| unpacking: {x=}, {y=}")

    # NamedTuple can be used as dict key (immutable + hashable)
    lookup = {p_nt: "origin-ish"}
    print(f" 4| as dict key: {lookup[PointNT(1, 2)]=}")

    # NamedTuple supports indexing like a tuple
    print(f" 5| index access: {p_nt[0]=}, {p_nt[1]=}")

    # immutability
    try:
        p_nt.x = 99
    except AttributeError as e:
        print(f" 6| immutable: {e}")

if __name__ == '__main__':
    show_slots()
    compare_with_namedtuple()
