# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses 'variances'.
"""

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods

from utils import print_function_header

"""
  - Variance describes how subtyping between complex types relates to subtyping 
    between their components.
  - Covariant: Preserves the subtype relationship.
    If Dog is an Animal, then List[Dog] is a List[Animal].
  - Contravariant: Reverses the subtype relationship.
    If Dog is an Animal, then Handler[Animal] is a Handler[Dog].
  - Invariant: No subtyping allowed at all.
    List[Dog] is not a List[Animal].
    (In Python, list is invariant)
"""


@print_function_header
def construct_generic_box():
    """ construct a box as in 'boxing' """

    class AnyBox:
        """ class can hold any value """
        def __init__(self, value): self.value = value
        def get(self): return self.value
        def set(self, new_value): self.value = new_value
        def __repr__(self): return f"{self.value}[{type(self.value).__name__}]"

    int_box = AnyBox(42)
    print(f" 1| {int_box=}")                # 42

    str_box = AnyBox("hello")
    print(f" 2| {str_box=}")                # hello

    str_box.set("world")
    print(f" 3| {str_box=}")                # world

    str_box.set(12.34)                      # ok? mypy: ok
    print(f" 4| {str_box=} ???")            # but once set, stick to it => but how?


# T = TypeVar('T')                          # a generic type placeholder named 'T'

class Box[T]:                               # Box(Generic[T]) from Python 3.12
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    def set(self, new_value: T) -> None:
        # with optional runtime safety
        # if not isinstance(new_value, type(self.value)): raise TypeError("Wrong type")
        self.value = new_value

    def __repr__(self):
        return f"{self.value}[{type(self.value).__name__}]"


@print_function_header
def construct_generic_typesafe_box():
    """ discuss a generic box """

    int_box = Box(42)                       # int_box: Box[int] = Box(42)
    print(f" 1| {int_box=}")                # 42

    # str_box = Box[int]("hello")           # mypy: incompatible type
    str_box = Box[str]("hello")
    print(f" 2| {str_box=}")                # hello

    str_box.set("world")
    print(f" 3| {str_box=}")                # world

    str_box.set(12.34)                      # mypy: incompatible type => that is what we wanted!  # ty:ignore[invalid-argument-type]
    print(f" 4| {str_box=} ???")            # remember: at runtime it works (if no type check)


if __name__ == "__main__":
    construct_generic_box()
    construct_generic_typesafe_box()
