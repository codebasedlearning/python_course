# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses interfaces and abstract classes.

Teaching focus
  - idea behind interfaces
"""

from typing import Type
from abc import ABC, abstractmethod

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


def extract_class_names(cls: Type[object]):
    return [item.__name__ for item in cls.__mro__]


def show_informal_interfaces():
    """ shows an example of an 'abstract' but instantiable class"""
    print("\nshow_informal_interfaces\n========================")

    class Window:
        """ 'informal interface', we expect subclasses to implement this method. """

        def draw(self):
            pass
            # raise NotImplementedError("draw is missing")

    class Canvas(Window):
        ...

    print(f" 1| is IWindow a subclass of Canvas? {issubclass(Canvas, Window)}")
    canvas = Canvas()
    print(f" 2| is 'canvas' an instance of IWindow? {isinstance(canvas, Window)}")
    canvas.draw()
    # ...even when it is missing!?


def show_abstract_base_classes():
    """ shows an example of an 'abstract' class """
    print("\nshow_abstract_base_classes\n==========================")

    class Window(ABC):                      # module 'abc' (abstract base class') enables abstract methods
        """ abstract base class """

        @abstractmethod                     # we expect subclasses to implement these abstract methods
        def draw(self):
            print(" a|  - Window.draw")     # usually there is no implementation
            ...                             # pylint: disable=unnecessary-ellipsis

    # class Clickable(Root):                # would be also abstract
    #     ...

    class Button(Window):
        def draw(self):
            print(" b|  - Button.draw")
            super().draw()

    print(" 1| create button instance")
    # wnd = Window()                        # can't instantiate an abstract class without implementations
    btn = Button()
    btn.draw()
    print()

    class Checkbox(Window):
        def draw(self):
            print(" c|  - Checkbox.draw")
            super().draw()

    class StrangeWidget:                    # duck typing
        def draw(self):
            print(" d|  - StrangeWidget.draw")
            # no super().draw

    print(" 2| create drawables")

    windows = [
            Button(),
            Checkbox(),
            StrangeWidget()                 # note that mypy complains
    ]
    for wnd in windows:
        wnd.draw()
        print(f" e|    - instance of Window? {isinstance(wnd, Window)}")


if __name__ == "__main__":
    show_informal_interfaces()
    show_abstract_base_classes()


###############################################################################


"""
Summary

Topics
  - interfaces
  - ABC, abstract classes
  - duck typing

Informal Interface
  - Python does not have an 'interface' keyword. This is not necessary from a 
    technical point of view because it is resolved at runtime whether an object 
    knows a method and if so, which one it is. We will have a look at this in 
    the 'duck-typing' topic.  
  - However, it may be useful to make it clear which methods are expected. 
    These methods should be overwritten. Having a base class that essentially 
    contains the signatures - like an interface - is one way of doing this. 
    If you like, this is a kind of informal interface, e.g.. here 'IWindow'. 
    This approach is suitable for small class hierarchies.

Module ABC, abstractmethod
  - There is a module 'abc' (abstract base class') designed for this. You 
    can mark a method as 'abstract', and instantiating a class with such 
    an abstract method will result in an error. Watch out, not only when 
    calling, but when creating the object. For that, the class must inherit 
    from 'ABC'.
    This touches on the subject of meta-classes, which we will look at later.
  - See also
    https://docs.python.org/3/library/abc.html
    https://realpython.com/python-interface/

Duck typing
  - In Python, you don't have to declare an interface explicitly. Any object 
    that implements the interface you want can be used instead of another 
    object. This is called duck typing. Duck typing is usually explained as 
    "if it acts like a duck, then it's a duck". Here the 'StrangeWidget' class 
    isn't derived from 'Window', but it exposes the same interface that 
    is required.

  - A nice discussion can be found here
    https://realpython.com/inheritance-composition-python
    From that source:
    Since you don’t have to derive from a specific class for your objects to 
    be reusable by the program, you may be asking why you should use inheritance 
    instead of just implementing the desired interface. The following rules may 
    help you:
      - Use inheritance to reuse an implementation: Your derived classes should 
        leverage most of their base class implementation. 
      - They must also model an 'is a' relationship. A Customer class might also 
        have an id and a name like an Employee class, but a Customer is not an 
        Employee, so you should not use inheritance.
      - Implement an interface to be reused: When you want your class to be 
        reused by a specific part of your application, you implement the 
        required interface in your class, but you don’t need to provide a 
        base class, or inherit from another class.
"""
