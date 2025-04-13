# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This example introduces a 'dataclass'. """

from dataclasses import dataclass, field, KW_ONLY


@dataclass                                                          # (A) dataclass
class InventoryItem:
    name: str                                                       # type hint is needed
    unit_price: float                                               # use 'Any' if the type should not be specified
    quantity_on_hand: int = 0                                       # default

    # def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0):
    #     self.name = name
    #     self.unit_price = unit_price
    #     self.quantity_on_hand = quantity_on_hand

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


@dataclass(init=True, repr=True, frozen=False)                      # controls method generation
class Point:
    x: int
    y: int = 0
    root: int = field(repr=False, default=-1)                          # more field info, cf. str()

@dataclass
class SizedList:
    # lst: list[int] = []                                             # mutable not allowed
    lst: list[int] = field(default_factory=list)
    size: int = 0

    def __post_init__(self):                                        # is called after init
        self.size = len(self.lst)

    def append(self, item):
        self.lst.append(item)
        self.size += 1

@dataclass(frozen=True)                                             # "immutable"
class FrozenInt:
    a: int

def work_with_dataclasses():
    print("\nwork_with_dataclasses\n=====================")

    item = InventoryItem(name="Apple", unit_price=0.99, quantity_on_hand=10)
    print(f" 1| {item=}, costs={item.total_cost()}")

    p = Point(x=1)                  # y def.
    print(f" 2| {p=}\n"
          f"    {p.__dict__=}\n"
          f"    {Point.__dict__=}")
    #print(f"03| C.dict={Point.__dict__=}\n")


    lst = SizedList(lst=[1, 2, 3])
    print(f" 3| {lst}=\n"
          f"    {lst.__dict__=}")
    #      f"    {SizedList.__dict__=}")
    #print(f"05| {SizedList.__dict__=}\n")

    const = FrozenInt(a=23)
    print(f" 4| {const=}")
    # e.a = 12

if __name__ == "__main__":
    work_with_dataclasses()

"""
(A) dataclass
Added in Python 3.7.
Simple data storage classes containing the 'usual' methods such as initialisation, output, comparison operators are
tedious to write.
The `dataclass' decorator selectively generates such methods for the class if they are not specified.
    See https://docs.python.org/3/library/dataclasses.html
    or https://realpython.com/python-data-classes/

(B) inheritance
Members are created using reverse MRO (i.e. starting from the object).
"""
