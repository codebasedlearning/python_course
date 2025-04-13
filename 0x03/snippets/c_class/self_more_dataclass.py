# (C) 2023 A.Voß, a.voss@fh-aachen.de, python@codebasedlearning.dev

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
class C:
    a: int
    b: int = 0
    c: int = field(repr=False, default=23)                          # more field info, cf. str()


@dataclass
class D:
    a: int
    _: KW_ONLY                                                      # dummy parameter, from here keyword only
    b: int


@dataclass(frozen=True)                                             # "immutable"
class E:
    a: int


@dataclass                                                          # (B) inheritance
class FBase:
    x: float = 3.14
    y: int = 0


@dataclass
class F(FBase):
    z: int = 10
    x: int = 15


@dataclass
class G:
    # l: list[int] = []                                             # mutable not allowed
    lst: list[int] = field(default_factory=list)
    cnt: int = 0

    def __post_init__(self):                                        # is called after init
        self.cnt = len(self.lst)


def main():
    item = InventoryItem(name="Apple", unit_price=0.99, quantity_on_hand=10)
    print(f"01| item={item}, costs={item.total_cost()}\n")

    c = C(a=1)
    print(f"02| c={c}\n"
          f"    c.dict={c.__dict__}")
    print(f"03| C.dict={C.__dict__}\n")

    d = D(1, b=2)                                                   # warning is a bug
    print(f"04| d={d}\n"
          f"    d.dict={d.__dict__}")
    print(f"05| D.dict={D.__dict__}, \n"
          f"    setter exists: {'__setattr__' in D.__dict__}\n")

    e = E(1)                                                        # frozen
    print(f"06| e={e}\n"
          f"    e.dict={e.__dict__}")
    print(f"07| E.dict={E.__dict__}\n"
          f"    setter exists: {'__setattr__' in E.__dict__}\n")

    f = F(1)                                                        # inherits
    print(f"08| f={f}\n"
          f"    f.dict={f.__dict__}")
    print(f"09| E.dict={E.__dict__}\n")


if __name__ == "__main__":
    main()

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
