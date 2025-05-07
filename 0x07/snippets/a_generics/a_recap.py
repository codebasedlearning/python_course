# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet recaps protocols.

Teaching focus
  - protocols
"""

from typing import Iterable, Protocol


class Clickable(Protocol):
    def on_click(self) -> None: ...


class Button:                               # No Clickable base class!
    def on_click(self) -> None:             # rename it to 'click' and start 'mypy' => error
        print(" a|   - Button.on_click")


class Switch:
    def on_click(self) -> None:
        print(" b|   - Switch.on_click")


def recap_protocol():
    """ recap protocol """
    print("\nrecap_protocol\n==============")

    def click_all(clickable: Iterable[Clickable]) -> None:
        for c in clickable:
            c.on_click()

    print(f" 1| click all")
    click_all([Button(), Switch()])


if __name__ == "__main__":
    recap_protocol()


###############################################################################


"""
Summary

Topics
  - protocols
  - Iterable

Note the 'Iterable[Clickable]'-type.

Protocols
  - Structural subtyping is based on the operations that can be performed 
    with an object. Class D is a structural subtype of class C if the former 
    has all attributes and methods of the latter, and with compatible types.
  - Structural subtyping can be seen as a static equivalent of duck typing, 
    which is well known to Python programmers. 
  - Mypy provides support for structural subtyping via protocol classes 
    described below. See 
    PEP 544 peps.python.org/pep-0544/
    for the detailed specification of protocols 
    and structural subtyping in Python.

See
  - https://mypy.readthedocs.io/en/stable/protocols.html

Predefined-protocols
    Iterable[T]     def __iter__(self) -> Iterator[T]
    Iterator[T]     def __next__(self) -> T
                    def __iter__(self) -> Iterator[T]
    Sized           def __len__(self) -> int
    Container[T]    def __contains__(self, x: object) -> bool       # in-operator

    Sequence        def __getitem__(self, s)
                    def __len__(self):

see also
    https://docs.python.org/3/reference/datamodel.html
    https://docs.python.org/3/library/collections.abc.html
    https://docs.python.org/3/library/typing.html
    
mypy
    https://mypy.readthedocs.io/en/stable/index.html
"""
