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

from typing import Protocol, TypeVar

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


def show_protocol_example():
    """ discuss a protocol example """
    print("\nshow_protocol_example\n=====================")

    class LineProcessor(Protocol):
        def process_line(self, line: str) -> None: ...
        def result(self) -> str: ...

    class LineCounter:
        def __init__(self):
            self.count = 0

        def process_line(self, _: str) -> None:
            self.count += 1

        def result(self) -> str:
            return f"{self.count} lines"

    class UniqueWordCollector:
        def __init__(self):
            self.words = set()

        def process_line(self, line: str) -> None:
            self.words.update(line.strip().split())

        def result(self) -> str:
            return f"{len(self.words)} unique words"

    def run_processor(processor: LineProcessor, lines: list[str]) -> str:
        for line in lines:
            processor.process_line(line)
        return processor.result()

    data = [
        "This is one line",
        "and another one",
        "last line here"
    ]

    print(f" 1| lines: {run_processor(LineCounter(), data)}")
    print(f" 2| words: {run_processor(UniqueWordCollector(), data)}")


def show_generic_protocol_example():
    """ discuss a generic protocol example """
    print("\nshow_generic_protocol_example\n=============================")

    T = TypeVar('T', covariant=True)        # for static check, a template variable that keeps track of the types

    class MyIterator(Protocol[T]):
        def current(self) -> T: ...
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

    def run_iterator(it: MyIterator[T], steps: int) -> list[T]:
        results = []
        for _ in range(steps):
            results.append(it.current())
            it.advance()
        return results

    print(f" 1| lines: {run_iterator(CountingIterator(5), 3)}")
    print(f" 2| words: {run_iterator(CyclicIterator(['a', 'b', 'c']), 7)}")


if __name__ == "__main__":
    show_protocol_example()
    show_generic_protocol_example()


###############################################################################


"""
Summary

Topics
  - protocol
  - mypy

Protocol

From https://en.wikipedia.org/wiki/Nominal_type_system
  - In computer science, a type system is a nominal or nominative type system 
    (or name-based type system) if compatibility and equivalence of data types 
    is determined by explicit declarations and/or the name of the types. 
    Nominal systems are used to determine if types are equivalent, as well as 
    if a type is a subtype of another. 
    Nominal type systems contrast with structural systems, where comparisons 
    are based on the structure of the types in question and do not require 
    explicit declarations.

See also
  - https://peps.python.org/pep-0484/   type hints, type metadata for static type checkers, only specifies the semantics of nominal subtyping
  - https://peps.python.org/pep-0544/   specify static and runtime semantics of protocol classes that will provide a support for structural subtyping (static duck typing).

  - https://mypy.readthedocs.io/en/stable/protocols.html#predefined-protocols-reference
  - https://auth0.com/blog/protocol-types-in-python/

Predefined-protocols
    Iterable[T]     def __iter__(self) -> Iterator[T]
    Iterator[T]     def __next__(self) -> T
                    def __iter__(self) -> Iterator[T]
    Sized           def __len__(self) -> int
    Container[T]    def __contains__(self, x: object) -> bool       # in-operator

    Sequence        def __getitem__(self, s)
                    def __len__(self):

see also
  - https://docs.python.org/3/reference/datamodel.html
  - https://docs.python.org/3/library/collections.abc.html
  - https://docs.python.org/3/library/typing.html
    
mypy:
    https://mypy.readthedocs.io/en/stable/index.html
"""
