# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses mixins.

Teaching focus
  - Mixins and interfaces often get lumped together, but they serve different
    roles:
	  - An interface (like Java’s Cloneable) says: “You must implement this
	    method.” (contract)
	  - A mixin says: “Here’s a free implementation of something useful.”
	    (behavior)
  - In Python, a mixin is a partial class you combine via multiple inheritance
    to add functionality, not define a type or contract.
"""

from typing import Type, Callable
from abc import ABC, abstractmethod
import json

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


def extract_class_names(cls: Type[object]):
    return [item.__name__ for item in cls.__mro__]

def show_clickable_mixin():
    """ discuss a mixin-example """
    print("\nshow_clickable_mixin\n====================")

    class Window(ABC):
        @abstractmethod
        def draw(self):
            ...

    class ColoredRectangle(Window):
        def draw(self):
            ...
            super().draw()

    class Clickable:
        """ clickable area we want to 'mix-in' """

        def __init__(self, *args, handler: Callable[[Window], None] = None, **kwargs):
            self.handler = handler or (lambda x: None)
            # remember the MRO issues
            super().__init__(*args, **kwargs)

        def register_handler(self, handler: Callable[[Window], None]):
            self.handler = handler

        def simulate_click(self):
            self.handler(self)

    class Button(ColoredRectangle, Clickable):
        def draw(self):
            ...
            super().draw()

    print(" 1| use mixin, register")

    def on_click(event_source):
        print(f" a| -> click from {event_source}")

    # register click-handler; btw: is a reference to local function ok?
    wnd = Button()
    wnd.register_handler(on_click)
    wnd.simulate_click()

    print(f" 2| Button.mro={extract_class_names(Button)}")


def show_serializable_mixin():
    """ discuss another mixin-example """
    print("\nshow_serializable_mixin\n=======================")

    class JsonMixin:
        """ assumes the object has a __dict__, which most classes do, and adds a to_json() method """
        def to_json(self) -> str:
            return json.dumps(self.__dict__)

        # No __init__() unless you call super() properly.

    class Animal:
        def __init__(self, name: str):
            self.name = name

    # You didn’t have to reimplement serialization logic in every subclass — just mixed it in.
    # Maby not all subclasses of Animal should have that behavior (e.g., if some require custom serialization).

    class Dog(Animal, JsonMixin):
        """ a serializable dog """
        def __init__(self, name: str, breed: str):
            super().__init__(name)
            self.breed = breed

    print(" 1| use mixin, serialize")
    fido = Dog("Fido", "Beagle")

    print(f" 2| fido: {fido.to_json()}")


if __name__ == "__main__":
    show_clickable_mixin()
    show_serializable_mixin()


###############################################################################


"""
Summary

Topics
  - Mixins and interfaces

Mixin
  - One reason for the window hierarchy problems seen before ('ClickableArea') 
    is that it mixes two aspects in one class: Window representation and 
    Click behaviour.
  - If you were to isolate one aspect and make it selectively available to 
    some windows, you would have a 'mixin' situation. These classes are 
    designed in such a way that they can be easily integrated into an existing 
    hierarchy (technically via multiple inheritance) and then provide very 
    specific and limited functionality. This is what we have modelled here, 
    using a click handler as an example.
  - Some design rules:
      - No __init__() unless you call super() properly.
      - Stateless or assume state provided by other parents.
      - Single purpose: A mixin should do one thing well.

  - See also:
    https://realpython.com/lessons/multiple-inheritance-python/
    https://realpython.com/inheritance-composition-python/
    https://realpython.com/python-super/

Callable
  - A signature of a method that receives a function, see
    https://docs.python.org/3/library/typing.html#typing.Callable
"""
