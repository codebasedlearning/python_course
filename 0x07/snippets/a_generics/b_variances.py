# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses 'protocols'.

Teaching focus
  - protocol
  - first generics

From https://mypy.readthedocs.io/en/stable/protocols.html

  - Nominal subtyping is strictly based on the class hierarchy. If class D
    inherits class C, it’s also a subtype of C, and instances of D can be
    used when C instances are expected. This form of subtyping is used by
    default in mypy, since it’s easy to understand and produces clear and
    concise error messages, and since it matches how the native isinstance
    check works – based on class hierarchy.

  - Structural subtyping is based on the operations that can be performed
    with an object. Class D is a structural subtype of class C if the former
    has all attributes and methods of the latter, and with compatible types.
    Structural subtyping can be seen as a static equivalent of duck typing,
    which is well known to Python programmers.
    Mypy provides support for structural subtyping via protocol classes
    described below. See PEP 544 for the detailed specification of protocols
    and structural subtyping in Python.
"""

from typing import Protocol


# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods

"""
  - Variance describes how subtyping between complex types relates to subtyping 
    between their components.
  - Covariant: Preserves the subtype relationship.
    If Dog is a Animal, then List[Dog] is a List[Animal].
  - Contravariant: Reverses the subtype relationship.
    If Dog is a Animal, then Handler[Animal] is a Handler[Dog].
  - Invariant: No subtyping allowed at all.
    List[Dog] is not a List[Animal].
    (In Python, list is invariant)
"""

from typing import TypeVar, Generic

def construct_generic_box():
    """ construct a box as in 'boxing' """
    print("\nconstruct_generic_box\n=====================")

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

    #---

T = TypeVar('T')                            # a generic type placeholder named 'T'

class Box[T]:                               # Box(Generic[T])
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


def construct_generic_typesafe_box():
    """ discuss a generic box """
    print("\nconstruct_generic_typesafe_box\n==============================")

    int_box = Box(42)                       # int_box: Box[int] = Box(42)
    print(f" 1| {int_box=}")                # 42

    # str_box = Box[int]("hello")           # mypy: incompatible type
    str_box = Box[str]("hello")
    print(f" 2| {str_box=}")                # hello

    str_box.set("world")
    print(f" 3| {str_box=}")                # world

    str_box.set(12.34)                      # mypy: incompatible type => that is what we wanted!
    print(f" 4| {str_box=} ???")            # remember: at runtime it works


# we need a class hierarchy to discuss variance
class Animal: pass
class Dog(Animal): pass                     # a Dog is an Animal
class Cat(Animal): pass                     # same for Cat


def consider_variances():
    """ discuss variances """
    print("\nconsider_variances\n==================")

    # consider subtypes as generic types (Animal, Dog, Cat)

    def print_id(box: Box[Animal]):
        print(f" 1| {box=}")                # just read it

    fifi_box = Box(Dog())                   # Box[Dog]
    print_id(fifi_box)                      # ok? mypy: incompatible type

    """
    1) Why is this a problem for mypy?
    2) Why is this no problem at runtime?
    3) How can we solve this?
    """

    """
    1) Box is invariant, i.e. 'Box[Dog]' is not a 'Box[Animal]', these are
       distinct types.
    2) We only read Animal-related info, there is no mutation.
    3) We need a concept for when you can treat Box[Dog] as Box[Animal] (and vice versa)
    """

    # Dog is an Animal, so now assume (!) 'Box[Dog]' is a 'Box[Animal]' (covariant)
    # (if Box[Dog] is allowed to be used wherever Box[Animal] is expected, then Box is covariant)

    def modify_content(box: Box[Animal]):
        print(f" 2| {box=}")
        box.set(Cat())                      # mypy: ok; as we modify it according to the type (Animal)

    rex_box = Box(Dog())
    modify_content(rex_box)
    print(f" 3| {rex_box=} ???")            # here we start with a Dog-Box and end up with a Cat

    # => writing is dangerous when having covariance

    # Now let’s go the other way — assume (!) Box[Animal] is a Box[Dog] (contravariant)
    # (use Box[Animal] where a Box[Dog] is expected, that is contravariant)

    def expect_dog(box: Box[Dog]):
        print(f" 4| {box=}")
        dog = box.get()
        # this would break if box contains an Animal that is not a Dog
        # dog.bark()  => AttributeError if not a Dog

    generic_box = Box(Animal())
    expect_dog(generic_box)                 # unsafe, but pretend this is allowed via contravariance

    # => reading is dangerous when having contravariance

    # Now let’s demonstrate a case where contravariance would actually be safe

    def store_a_dog(box: Box[Dog]):
        box.set(Dog())                      # only sets, no get()

    zoo_box = Box(Animal())                 # assume Box[Animal] is accepted as Box[Dog] (contravariant)
    store_a_dog(zoo_box)                    # mypy: incompatible type, but ok
    print(f" 5| {zoo_box=}")

    # => writing-only functions are safe when using contravariance


def construct_co_boxes():
    """ construct covariant and contravariant boxes """
    print("\nconstruct_co_boxes\n==================")

    T_co = TypeVar('T_co', covariant=True)

    class ReadOnlyBox(Generic[T_co]):       # makes it a covariant type
        def __init__(self, value: T_co):
            self.value = value

        def get(self) -> T_co:              # output
            return self.value

        def __repr__(self):
            return f"{self.value}[{type(self.value).__name__}]"

    def print_id(box: ReadOnlyBox[Animal]):
        print(f" 1| {box=}")                # just read it

    fifi_box = ReadOnlyBox(Dog())           # ReadOnlyBox[Dog]
    print_id(fifi_box)                      # ok? now mypy: ok!

    # => Covariant: Box[Dog] can be used where Box[Animal] is expected — because we’re only reading.

    T_contra = TypeVar('T_contra', contravariant=True)  # makes it a contravariant type

    class WriteOnlyBox(Generic[T_contra]):
        def __init__(self, value: T_contra):
            self.value = value

        def set(self, new_value: T_contra) -> None: # input
            self.value = new_value

        def __repr__(self):
            return f"{self.value}[{type(self.value).__name__}]"

    def store_a_dog(box: WriteOnlyBox[Dog]):
        box.set(Dog())                      # only sets, no get()

    zoo_box = WriteOnlyBox(Animal())
    store_a_dog(zoo_box)                    # now mypy: ok
    print(f" 2| {zoo_box=}")

    # => Contravariant: Box[Animal] can be used where Box[Dog] is expected — because we’re only writing.

    """
    Use Case        TypeVar                     Direction       Substitution

    Read-only       T_co (covariant)            Output only     Allows Box[Dog] -> Box[Animal]
    Write-only      T_contra (contravariant)    Input only      Allows Box[Animal] -> Box[Dog]
    Read & write    T (invariant)               Both            Prevents all substitution
    """


def show_generic_protocol_example():
    """ discuss a generic protocol example """
    print("\nshow_generic_protocol_example\n=============================")

    T_co = TypeVar('T_co', covariant=True)  # for static check, a template variable that keeps track of the types

    class MyIterator(Protocol[T_co]):
        def current(self) -> T_co: ...
        def advance(self) -> None: ...

    class CountingIterator:
        def __init__(self, start: int = 0):
            self._value = start

        def current(self) -> int:
            return self._value

        def advance(self) -> None:
            self._value += 1

    class CyclicIterator:
        def __init__(self, items):
            self._items = items
            self._index = 0

        def current(self):
            return self._items[self._index]

        def advance(self):
            self._index = (self._index + 1) % len(self._items)

    def run_iterator(it: MyIterator[T_co], steps: int) -> list[T_co]:
        results = []
        for _ in range(steps):
            results.append(it.current())
            it.advance()
        return results

    print(f" 1| lines: {run_iterator(CountingIterator(5), 3)}")
    print(f" 2| words: {run_iterator(CyclicIterator(['a', 'b', 'c']), 7)}")


if __name__ == "__main__":
    construct_generic_box()
    construct_generic_typesafe_box()
    consider_variances()
    construct_co_boxes()
    show_generic_protocol_example()


###############################################################################


"""
  - Note: You can reuse the same TypeVar across your entire module if it 
    has the same meaning everywhere. It’s just a symbol, not a specific 
    instantiation.
"""
