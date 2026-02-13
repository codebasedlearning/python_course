# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses abstract classes and methods used in the IPO framework.

Teaching focus
  - Abstract concept; use ABC when:
      - you need runtime behavior, like abstract base class checking;
      - you’re defining a framework or library where you control the hierarchy;
      - you want enforced overrides and possibly shared logic.
  - We discuss Protocols later; use this when:
      - you’re defining an interface purely for type checking;
      - you want to support third-party or duck-typed implementations;
      - you’re writing library or utility functions with loose coupling.
"""

from abc import ABC, abstractmethod


class Drawable(ABC):
    """ abstract base class for drawable objects """

    def __init__(self, label: str):
        self.label = label

    @abstractmethod
    def draw(self) -> None:
        """ draw the object """

    def describe(self) -> None:
        """ shared logic """
        print(f" a| This is a {self.__class__.__name__} labeled '{self.label}'")


class Circle(Drawable):
    """ a circle class """
    def draw(self) -> None:
        print(f" b| Drawing a circle labeled '{self.label}'")


class Square(Drawable):
    """ a square class """
    def draw(self) -> None:
        print(f" c| Drawing a square labeled '{self.label}'")


def show_abstract_methods():
    """ show abstract methods """
    print("\nshow_abstract_methods\n=====================")

    shapes = [
        # Drawable("Figure"),               # error: abstract class
        Circle("Sun"),
        Square("Window"),
        "oops"                              # what?
    ]
    for shape in shapes:
        if isinstance(shape, Drawable):     # it works with ABC
            shape.describe()
            shape.draw()


if __name__ == "__main__":
    show_abstract_methods()
