# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses 'variance'.
"""

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods
from collections.abc import Callable
from typing import Generic, Protocol, TypeVar

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


# we need a class hierarchy to discuss variance
class Animal: pass
class Dog(Animal): pass                     # a Dog is an Animal
class Cat(Animal): pass                     # same for Cat


@print_function_header
def consider_variances():
    """ discuss variances """

    # consider subtypes as generic types (Animal, Dog, Cat)

    def print_id(box: Box[Animal]):
        print(f" 1| {box=}")                # just read it

    fifi_box = Box(Dog())                   # Box[Dog]
    print_id(fifi_box)                      # ok? mypy: incompatible type  # ty:ignore[invalid-argument-type]

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

    =>  Dog is an Animal, so now assume (!) 'Box[Dog]' is a 'Box[Animal]' (covariant)
        Or: if Box[Dog] is allowed to be used wherever Box[Animal] is expected, then Box is covariant.
    """

    def modify_content(box: Box[Animal]):
        print(f" 2| {box=}")
        box.set(Cat())                      # mypy: ok; as we modify it according to the type (Animal)

    rex_box = Box(Dog())
    modify_content(rex_box)                 # ty:ignore[invalid-argument-type]
    print(f" 3| {rex_box=} ???")            # here we start with a Dog-Box and end up with a Cat

    """
    => writing is dangerous when having covariance

    Now let’s go the other way
        Assume (!) Box[Animal] is a Box[Dog] (contravariant)
        Or: use Box[Animal] where a Box[Dog] is expected, that is contravariant.
    """

    def expect_dog(box: Box[Dog]):
        print(f" 4| {box=}")
        dog = box.get()
        # this would break if box contains an Animal that is not a Dog:
        # dog.bark()  => AttributeError if not a Dog

    generic_box = Box(Animal())
    expect_dog(generic_box)                 # unsafe, but pretend this is allowed via contravariance  # ty:ignore[invalid-argument-type]

    """
    => reading is dangerous when having contravariance

    Now let’s demonstrate a case where contravariance would actually be safe
    """

    def store_a_dog(box: Box[Dog]):
        box.set(Dog())                      # only sets, no get()

    zoo_box = Box(Animal())                 # assume Box[Animal] is accepted as Box[Dog] (contravariant)
    store_a_dog(zoo_box)                    # mypy: incompatible type, but ok  # ty:ignore[invalid-argument-type]
    print(f" 5| {zoo_box=}")

    """
    => writing-only functions are safe when using contravariance
    """

T_cov = TypeVar('T_cov', covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)

@print_function_header
def construct_co_boxes():
    """ construct covariant and contravariant boxes """

    class ReadOnlyBox(Generic[T_cov]):       # makes it a covariant type
        def __init__(self, value: T_cov):
            self.value = value

        def get(self) -> T_cov:              # output
            return self.value

        def __repr__(self):
            return f"{self.value}[{type(self.value).__name__}]"

    def print_id(box: ReadOnlyBox[Animal]):
        print(f" 1| {box=}")                # just read it

    fifi_box = ReadOnlyBox(Dog())           # ReadOnlyBox[Dog]
    print_id(fifi_box)                      # ok? now mypy: ok!

    """
    => Covariant: Box[Dog] can be used where Box[Animal] is expected — because we’re only reading.
    """

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

    """
    => Contravariant: Box[Animal] can be used where Box[Dog] is expected — because we’re only writing.
    """

    
"""
Use Case        TypeVar                     Direction       Substitution

Read-only       T_cov (covariant)           Output only     Allows Box[Dog] -> Box[Animal]
Write-only      T_contra (contravariant)    Input only      Allows Box[Animal] -> Box[Dog]
Read & write    T (invariant)               Both            Prevents all substitution
"""

# for static check, a template variable that keeps track of the types
# remove 'covariant' to make it invariant
S = TypeVar("S", covariant=True)


@print_function_header
def show_generic_protocol_example():
    """ discuss a generic protocol example """

    class MyIterator(Protocol[S]):
        def current(self) -> S: ...
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

    def to_list(it: MyIterator[S], steps: int) -> list[S]:
        results = []
        for _ in range(steps):
            results.append(it.current())
            it.advance()
        return results

    print(f" 1| lines: {to_list(CountingIterator(start=5), steps=3)}")
    print(f" 2| words: {to_list(CyclicIterator(items=['a', 'b', 'c']), steps=7)}")


@print_function_header
def consider_callable_variance():
    """ discuss Callable[[X], Y]: contravariant in X, covariant in Y """

    """
    Callable[[X], Y] is the canonical example: a *single* type that is
      - contravariant in the input  X  (you may widen the accepted type)
      - covariant     in the output Y  (you may narrow the returned type)

    Nice side-effect: Python's typing has the variance baked in, so we
    don't need T_cov / T_contra here — mypy already plays along.
    """

    # --- contravariance on the input (predicate-style functions) ---

    def is_friendly_animal(a: Animal) -> bool:
        return True                             # works for *any* Animal

    def is_friendly_dog(d: Dog) -> bool:
        return True                             # only works for Dog

    def filter_dogs(dogs: list[Dog], pred: Callable[[Dog], bool]) -> list[Dog]:
        return [d for d in dogs if pred(d)]     # uses pred only on Dog

    dogs = [Dog(), Dog()]
    print(f" 1| filter with dog-predicate    = {filter_dogs(dogs, is_friendly_dog)}")
    print(f" 2| filter with animal-predicate = {filter_dogs(dogs, is_friendly_animal)}")
    # mypy: ok — Callable[[Animal], bool] is a *subtype* of Callable[[Dog], bool]
    # Intuition: a function that handles any animal can stand in for one that handles only dogs.

    # --- covariance on the output (factories / producers) ---

    def make_dog() -> Dog:
        return Dog()

    def make_animal() -> Animal:
        return Animal()

    def use_animal_factory(make: Callable[[], Animal]) -> Animal:
        return make()                           # caller only reads the result

    print(f" 3| factory returning Animal = {use_animal_factory(make_animal).__class__.__name__}")
    print(f" 4| factory returning Dog    = {use_animal_factory(make_dog).__class__.__name__}")
    # mypy: ok — Callable[[], Dog] is a *subtype* of Callable[[], Animal]
    # Intuition: a function promising a Dog also satisfies "give me some Animal".

    # --- both variances at once: Liskov in one line ---

    def take_widely_make_narrowly(a: Animal) -> Dog:
        return Dog()

    f: Callable[[Animal], Dog]    = take_widely_make_narrowly  # wider in, narrower out
    g: Callable[[Dog],    Animal] = f                          # mypy: ok!

    result = g(Dog())
    print(f" 5| g(Dog()) -> {result.__class__.__name__} (declared Animal)")

    # --- the *wrong* direction is rejected ---

    def take_narrowly_make_widely(d: Dog) -> Animal:
        return Animal()

    # h: Callable[[Animal], Dog] = take_narrowly_make_widely  # mypy: incompatible type

    # Why not? It promises to accept any Animal but only knows how to handle Dog,
    # and it promises to return a Dog but might return any Animal. Both directions wrong.

    """
    Cheat sheet — Callable[[X], Y] subtype rule
        X may be *wider*    than expected  (contravariant in X)
        Y may be *narrower* than expected (covariant     in Y)
    """


if __name__ == "__main__":
    consider_variances()
    construct_co_boxes()
    show_generic_protocol_example()
    consider_callable_variance()
