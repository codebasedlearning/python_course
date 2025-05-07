# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses different forms of typing.

Teaching focus
  - nominal typing
  - subtyping
  - duck typing
  - structural typing
"""

from types import SimpleNamespace
from typing import Protocol

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


def show_nominal_typing():
    """
    Nominal Typing (a.k.a. “Name matters”)

    A type is identified by its name, not its structure.
    If two types have the same methods and fields but different names, they
    are considered different types.
    """
    print("\nshow_nominal_typing\n===================")

    class Dog: pass
    class Cat: pass

    def pet(dog: Dog):
        print(f" a| pet: {dog=}")

    # Is it running?
    # How can we check it (if we want to)?
    #
    # pylint 0x06/snippets/a_intro/a_typing.py      -> rated at 10.00/10
    # mypy 0x06/snippets/a_intro/a_typing.py        -> error: incompatible type "Cat"; expected "Dog"
    # => Even if Cat and Dog look the same, their names are different, so the type checker objects.

    dog = Dog()
    maybe_dog = Cat()
    print(" 1| call pet")
    pet(maybe_dog)

    # Note: excessive use of type checking can lead to code that's not very Pythonic.
    print(f" 2| type check: {isinstance(dog, Dog)=}, {isinstance(maybe_dog, Dog)=}")


def show_nominal_subtyping():
    """
    Subtyping (a.k.a. “Inheritance hierarchy”)

	A type is a subtype of another if it inherits from it. This is classic OOP.
	Subtyping is nominal in Python: it’s about declared inheritance.
    """
    print("\nshow_nominal_subtyping\n======================")

    class Animal: pass
    class Dog(Animal): pass

    def pet(animal: Animal):
        print(f" a| animal: {animal=}")

    dog = Dog()
    print(" 1| call pet")
    pet(dog)                                # no complains

    print(f" 2| type check: {isinstance(dog, Dog)=}, {isinstance(dog, object)=}, {isinstance(dog, str)=}")
    print(f" 3| subtype check: {issubclass(Dog,Dog)=}, {issubclass(Dog, Animal)=}, {issubclass(Dog, str)=}")


def show_duck_typing():
    """
    Duck Typing (a.k.a. “Runtime YOLO typing”)

	"If it quacks like a duck and swims like a duck, it’s a duck."
	It’s not enforced at type-checking, just assumed at runtime - Python’s default style.
    """
    print("\nshow_duck_typing\n================")

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

def show_structural_typing():
    """
    Structural Typing (a.k.a. “Looks like a duck” or “Duck typing with type hints”)

	If it has the right methods/attributes, it fits — even if it’s not declared as a subtype.
	Introduced: Python 3.8+ with typing.Protocol
	Duck typing that quacks at compile-time (Python’s way to get the best of both worlds).
    """
    print("\nshow_structural_typing\n======================")

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

    # quack(SimpleNamespace(quack=lambda: print("'Quack!!!!!'"))


if __name__ == "__main__":
    show_nominal_typing()
    show_nominal_subtyping()
    show_duck_typing()
    show_structural_typing()


###############################################################################


"""
Summary

Topics
  - nominal typing
  - subtyping
  - duck typing
  - structural typing
  
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
