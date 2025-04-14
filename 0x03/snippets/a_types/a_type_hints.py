# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses the use of data types and data type references.

Teaching focus
  - type hints
"""

from typing import Self


def add(a, b):                                                  # no types, see also 'test_add'
    """ Calculates a+b """
    return a + b


def test_add():
    """ what can be added? """
    print("\ntest_add\n========")

    print(f" 1| {add(2, 3)=}")
    print(f"    {add('2', '3')=}")                              # bug or feature?
    try:
        add('2', 3)                                             # run-time error, no IDE hint
    except TypeError as e:
        print(f" 2| {e=}")


def mul(a: str | int, b: int) -> str | int:                     # type hints, see also 'test_mul'
    """ Calculates a*b """
    return a * b


def test_mul():
    """ what can be multiplied? """
    print("\ntest_mul\n========")

    print(f" 3| {mul(2, 3)=}")
    print(f"    {mul('2', 3)=}")                                # bug or feature?
    try:
        mul('2', '3')                                           # run-time error, now with IDE hint (also mypy)
    except TypeError as e:
        print(f" 4| {e=}")


def vars_and_type_hints():
    """ variables and type hints """
    print("\nvars_and_type_hints\n===================")

    s: str = "Python"                                           # variable definition with (optional) type hint
    print(f" 1| Hello '{s}'")

    n: int = 23                                                 # with type 'int'.
    if n > 0:
        print(f" 2| {n=}, {2*n=}")
        n = -2.5                                                # assignment, with IDE hint (also mypy)
        print(f" 3| {n=}")


class Person:
    """ simple person class """

    def __init__(self, name: str) -> None:
        self._name: str = name  # Internal name attribute with type hint

    @property
    def name(self) -> str:
        """ getter method for name """
        return self._name

    # def clear_name(self) -> "Person":
    def clear_name(self) -> Self:                               # Python 3.11 and later
        """ clears the name and returns the instance """
        self._name = ""
        return self


def classes_and_type_hints():
    """ classes and type hints """
    print("\nclasses_and_type_hints\n======================")

    hp: Person = Person("Hans-Peter K.")
    print(f" 1| Hello '{hp.name}'")


if __name__ == "__main__":
    test_add()
    test_mul()
    vars_and_type_hints()
    classes_and_type_hints()


###############################################################################


"""
Summary

Topics
  - type hints

Python's type system
  - The primary aim here is to discuss and understand Python's type system and 
    the use of type information aka. type hints.
  - From Wikipedia: Python is dynamically typed. This is in contrast to 
    statically-typed languages, where each variable may contain only a value 
    of a certain type.
      - See https://en.wikipedia.org/wiki/Python_(programming_language)
      - and https://en.wikipedia.org/wiki/Type_system#DYNAMIC
    Example: s='Python' [...] s=5
    The assignment statement (=) binds a name as a reference to a separate, 
    dynamically allocated object. Variables may subsequently be rebound at 
    any time to any object. In Python, a variable name is a generic reference 
    holder without a fixed data type; however, it always refers to some object 
    with a type. 
  - Python uses 'duck typing' and has typed objects but untyped variable names.
    Duck typing in computer programming is an application of the duck test, i.e. 
        "If it walks like a duck and it quacks like a duck, then it must be a duck" 
    to determine whether an object can be used for a particular purpose.
    In duck typing, an object 'is' of a given type if it has all methods and 
    properties required by that type. 
    See https://en.wikipedia.org/wiki/Duck_typing
  - Cited 'DonaldPShimoda' (I like the wording): 
    Python is strongly typed. There's no implicit conversion among types. 
    Many people think that because Python is dynamically typed (i.e. you can pass 
    anything anywhere without compile-time restrictions), that it must also be 
    weakly typed. This is simply not the case. If I write a function which 
    expects an integer and I give it a string, I'm going to have a bad time 
    despite the fact that the code "compiles" and only fails at runtime.
      - See https://news.ycombinator.com/item?id=17484385
    Because there are many possibilities for explicit and implicit conversions, 
    C and C++ are more weakly typed in this sense. 
  - In the code snippets (and in the production code) I always use type hints 
    when they are helpful. If the data type is clearly derivable, the type 
    specification outside of a signature is rather omitted, like in other 
    languages (var n=23, auto n=23).

Function definition.
  - The function 'add' has two parameters of unknown type each. This means 
    that it can be called with any two objects. The operation '+' is then 
    defined for this combination or not, which can lead to a runtime error 
    (see example in 'test_add').

Type hints
  - A type hint is only an optional specification ('hint') for the IDE or 
    tools such as a linter to check. 
  - At runtime type specifications have no effect. In the first Python versions 
    there was no explicit specification of types at all.
      - See also https://docs.python.org/3/library/typing.html
  - There is a useful tool called mypy,
      - see https://pypi.org/project/mypy/
      - and https://www.mypy-lang.org
"""
