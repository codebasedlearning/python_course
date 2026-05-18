# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses different forms of typing.

Teaching focus
  - nominal typing
  - subtyping
  - duck typing
  - structural typing
  - generic types / TypeVar

Summary

Topics
  - nominal typing
  - subtyping
  - duck typing
  - structural typing
  - generic types / TypeVar

See also
  - Typing module (standard library)
    https://docs.python.org/3/library/typing.html

  - Abstract Base Classes
    https://docs.python.org/3/library/abc.html

  - Data Model Reference (Duck typing & method resolution)
    https://docs.python.org/3/reference/datamodel.html

  - PEP 544 – Protocols: Structural subtyping (static duck typing)
    https://peps.python.org/pep-0544/

  - PEP 484 – Type Hints (the foundation)
    https://peps.python.org/pep-0484/

  - PEP 3119 – Introduction of abc
    https://peps.python.org/pep-3119/
"""

from types import SimpleNamespace
from typing import Generic, Protocol, Self, TypeVar, get_args

from utils import print_function_header

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


@print_function_header
def show_nominal_typing():
    """
    Nominal Typing (a.k.a. "Name matters")

    A type is identified by its name, not its structure.
    If two types have the same methods and fields but different names, they
    are considered different types.
    """

    class Dog: pass
    class Cat: pass

    def pet(dog: Dog):
        print(f" a| pet: {dog=}")

    # Is it running?
    # How can we check it (if we want to)?
    #
    # pylint 0x04/snippets/a_typing.py      -> rated at 10.00/10
    # mypy 0x04/snippets/a_typing.py        -> error: incompatible type "Cat"; expected "Dog"
    # ty check 0x04/snippets/a_typing.py    -> error: Argument to function `pet` is incorrect...
    # => Even if Cat and Dog look the same, their names are different, so the type checker objects.

    dog = Dog()
    maybe_dog = Cat()
    print(" 1| call pet")
    pet(maybe_dog)

    # Note: excessive use of type checking can lead to code that's not very Pythonic.
    print(f" 2| type check: {isinstance(dog, Dog)=}, {isinstance(maybe_dog, Dog)=}")


@print_function_header
def show_nominal_subtyping():
    """
    Subtyping (a.k.a. "Inheritance hierarchy")

	A type is a subtype of another if it inherits from it. This is classic OOP.
	Subtyping is nominal in Python: it's about declared inheritance.
    """

    class Animal: pass
    class Dog(Animal): pass

    def pet(animal: Animal):
        print(f" a| animal: {animal=}")

    dog = Dog()
    print(" 1| call pet")
    pet(dog)                                # no complains

    print(f" 2| type check: {isinstance(dog, Dog)=}, {isinstance(dog, object)=}, {isinstance(dog, str)=}")
    print(f" 3| subtype check: {issubclass(Dog,Dog)=}, {issubclass(Dog, Animal)=}, {issubclass(Dog, str)=}")


@print_function_header
def show_duck_typing():
    """
    Duck Typing (a.k.a. "Runtime YOLO typing")

	"If it quacks like a duck and swims like a duck, it's a duck."
	It's not enforced at type-checking, just assumed at runtime - Python's default style.
    """

    class Duck:
        def quack(self): print("'Quack!'")

    def quack(thing):                       # No type information here! What should we take?
        thing.quack()

    # No types, no annotations. If you pass something without a quack() method,
    # it crashes at runtime, not during type checking.
    #
    # Is it running?
    # How can we check it (if we want to)?

    print(" 1|     you -> ", end='')
    quack(Duck())

    class Parrot:
        def quack(self): print("'Quack!!!'")

    print(" 2| now you -> ", end='')
    quack(Parrot())

    # SimpleNamespace is a simple class that provides attribute access.
    # It is essentially like an 'object' but with mutable attributes.
    print(" 3| and you -> ", end='')
    quack(SimpleNamespace(quack=lambda: print("'Quack!!!!!'"))

    # pylint and mypy are happy! Duck typing is OK by design (but still unsafe...)
)

@print_function_header
def show_structural_typing():
    """
    Structural Typing (a.k.a. "Looks like a duck" or "Duck typing with type hints")

	If it has the right methods/attributes, it fits — even if it's not declared as a subtype.
	Introduced: Python 3.8+ with typing.Protocol
	Duck typing that quacks at compile-time (Python's way to get the best of both worlds).
    """

    class Quacker(Protocol):
        def quack(self) -> None: ...

    class Person:
        def quack(self): print("I pretend I'm a duck")

    def quack(q: Quacker):
        q.quack()

    print(" 1|     you -> ", end='')
    quack(Person())

    class Snake:                            # Snake structurally (!) matches Quacker.
        def quack(self) -> None:            # It fits the protocol!
            print("'Quacksssss'")

    print(" 2| now you -> ", end='')
    quack(Snake())

    # quack(object())
    # quack(SimpleNamespace(quack=lambda: print("'Quack!!!!!'")))


"""
    A TypeVar is a placeholder for a type — it says "some type T, to be determined later".
    Generic[T] makes a class parameterized over T, so the type checker can track
    what's actually inside without forcing you to use Any.
    
    From Python 3.12 a new syntax 
        def foo[T](x: T) -> T 
    or
        class Box[T]
    creates implicit TypeVars.
"""
T = TypeVar('T')

@print_function_header
def show_generic_types():
    """
    Generic Types (a.k.a. "parameterized containers")
    """

    class Box(Generic[T]):              # Box is generic over T, or: class Box[T]
        def __init__(self, value: T) -> None:
            self.value = value

        def unwrap(self) -> T:          # return type follows from T
            return self.value

    int_box: Box[int] = Box(42)
    str_box: Box[str] = Box("hello")

    print(f" 1| int_box.unwrap() -> {int_box.unwrap()!r}  (type: {type(int_box.unwrap()).__name__})")
    print(f" 2| str_box.unwrap() -> {str_box.unwrap()!r}  (type: {type(str_box.unwrap()).__name__})")

    # TypeVar also constrains generic functions
    def first(items: list[T]) -> T:     # T binds to the element type at call site
        return items[0]

    print(f" 3| first([1, 2, 3])     -> {first([1, 2, 3])!r}")
    print(f" 4| first(['a', 'b'])    -> {first(['a', 'b'])!r}")

@print_function_header
def use_type_annotations():
    """
    Calling a class method on a generic type — two approaches.

    TypeVar T is erased at runtime. You cannot do T() or T.create() inside a
    generic function/class body, because T is just a checker-level name.

    Approach A — pass type[T] explicitly:
        Simple, explicit, type-checker friendly. Use when the caller knows T.

    Approach B — extract T via __orig_bases__ + get_args:
        The concrete subclass (e.g. SensorRepo(Repository[Sensor])) carries the
        parameterized base in __orig_bases__ before erasure. get_args recovers
        the bound type at runtime. Use when T must be implicit (framework-style).
    """

    class Sensor:
        def __init__(self, value: float) -> None:
            self.value = value

        @classmethod
        def default(cls) -> Self:           # or 'Sensor'
            return cls(0.0)

        def __repr__(self) -> str:
            return f"{type(self).__name__}(value={self.value})"

    class PressureSensor(Sensor):
        @classmethod
        def default(cls) -> Self:           # or 'PressureSensor'
            return cls(1013.25)             # standard atmosphere as default

    # --- Approach A: pass the class explicitly ---

    def make_default(cls: type[T]) -> T:   # cls IS the class object; T tracks its type
        return cls.default()

    print(f" 1| make_default(Sensor)         -> {make_default(Sensor)!r}")
    print(f" 2| make_default(PressureSensor) -> {make_default(PressureSensor)!r}")

    # --- Approach B: extract T from __orig_bases__ ---
    # Useful inside a base class that needs to know its own type argument without
    # any explicit parameter — the subclass declaration carries that information.

    class Repository(Generic[T]):
        def _entity_class(self) -> type:
            for base in vars(type(self)).get('__orig_bases__', ()):
                args = get_args(base)        # e.g. (Sensor,) or (PressureSensor,)
                if args:
                    return args[0]          # first (and only) type argument
            raise TypeError(f"{type(self)} has no generic type argument")

        def make_default_entity(self) -> T:
            cls = self._entity_class()
            return cls.default()            # call the class method on the recovered type

    class SensorRepo(Repository[Sensor]): pass
    class PressureSensorRepo(Repository[PressureSensor]): pass

    sr = SensorRepo().make_default_entity()
    pr = PressureSensorRepo().make_default_entity()

    print(f" 3| SensorRepo().make_default_entity()         -> {sr!r}")
    print(f" 4| PressureSensorRepo().make_default_entity() -> {pr!r}")


if __name__ == "__main__":
    show_nominal_typing()
    show_nominal_subtyping()
    show_duck_typing()
    show_structural_typing()
    show_generic_types()
    use_type_annotations()
