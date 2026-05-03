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

from dataclasses import dataclass, field

from utils import print_function_header

"""
Topic: Dataclasses
"""


@dataclass
class InventoryItem:
    """ a simple data class """
    name: str                               # type hint is needed
    unit_price: float                       # use 'Any' if the type should not be specified
    quantity_on_hand: int = 0               # with default

    # def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0):
    #     self.name = name
    #     self.unit_price = unit_price
    #     self.quantity_on_hand = quantity_on_hand
    #
    # The `@dataclass` decorator will automatically handle repetitive tasks like
    # creating the `__init__` and `__repr__` method

    def total_cost(self) -> float:
        """ total cost (all units) """
        return self.unit_price * self.quantity_on_hand


@dataclass(init=True, repr=True, frozen=False)  # controls method generation
class Point:
    """ point class """
    x: int
    y: int = 0
    root: int = field(repr=False, default=-1)   # removed from repr, more field info, cf. str()


@dataclass
class SizedList:
    """ a list with a size """
    # lst: list[int] = []                           # mutable not allowed
    lst: list[int] = field(default_factory=list)    # use a factory
    size: int = 0

    def __post_init__(self):                # is called after init
        self.size = len(self.lst)

    def append(self, item):
        """ append an item """
        self.lst.append(item)
        self.size += 1


@dataclass(frozen=True)                     # "immutable"
class FrozenInt:
    """ an immutable integer """
    a: int


@print_function_header
def work_with_dataclasses():
    """ work with dataclasses """

    item = InventoryItem(name="Apple", unit_price=0.99, quantity_on_hand=10)
    print(f" 1| {item=}, costs={item.total_cost()}")

    p = Point(x=1)                          # y with default value
    print(f" 2| {p=}\n"
          f"    {p.__dict__=}\n"
          f"    {Point.__dict__=}")         # root is hidden (repr=False)

    lst = SizedList(lst=[1, 2, 3])
    print(f" 3| {lst}=\n"
          f"    {lst.__dict__=}")

    const = FrozenInt(a=23)
    print(f" 4| {const=}")
    # e.a = 12



if __name__ == "__main__":
    work_with_dataclasses()
