# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses multiple inheritance - the super function.

Teaching focus
  - inheritance order
"""

from typing import Type
from collections import OrderedDict

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


def extract_class_names(cls: Type[object]):
    return [item.__name__ for item in cls.__mro__]


def discover_unnoticed_intruder():
    """ inheritance changed """
    print("\ndiscover_unnoticed_intruder\n===========================")

    class Window:
        def draw(self): print("Window ", end='') # ; super().draw()

    class ColoredRectangle(Window):
        def draw(self): print("ColoredRectangle ", end=''); super().draw()

    class ClickableArea(Window):
        def draw(self): print("ClickableArea ", end=''); super().draw()

    class Button(ColoredRectangle, ClickableArea):
        def draw(self): print("Button ", end=''); super().draw()

    print(f" 1| ColoredRectangle.mro={extract_class_names(ColoredRectangle)}")
    print("    draw: ", end='')
    ColoredRectangle().draw()
    print()

    # note, new class in between: ClickableRect -> is that a problem?
    # (ColoredRectangle thinks it inherits from Window)
    print(f" 2| Button, mro={extract_class_names(Button)}")
    print("    draw: ", end='')
    Button().draw()
    print()


def new_base_class_in_town():
    """ changing base classes """
    print("\nnew_base_class_in_town\n======================")

    class Window:
        def draw(self): print("Window ", end='')            # ; super().draw() missing?

    class ColoredRectangle(Window):
        def draw(self): print("ColoredRectangle ", end=''); super().draw()

    class ClickableBase:
        def draw(self): print("ClickableBase ", end='')     # ; super().draw() missing?

    class ClickableArea(Window, ClickableBase):
        def draw(self): print("ClickableArea ", end=''); super().draw()

    class Button(ColoredRectangle, ClickableArea):
        def draw(self): print("Button ", end=''); super().draw()

    print(f" 1| ColoredRectangle.mro={extract_class_names(ColoredRectangle)}")
    print("    draw: ", end='')
    ColoredRectangle().draw()
    print()

    # new class after 'Window', call 'draw'? any solution to this?
    print(f" 2| Button.mro={extract_class_names(Button)}")
    print("    draw: ", end='')
    Button().draw()
    print()


def introduce_root_class():
    """ introduce a universal 'Root' class """
    print("\nintroduce_root_class\n====================")

    # Only one path to Root is needed in the hierarchy.

    class Root:
        def draw(self): print("Root ", end='')          # explicitly no call to super().draw()

    class Window(Root):
        def draw(self): print("Window ", end=''); super().draw()

    class ColoredRectangle(Window):
        def draw(self): print("ColoredRectangle ", end=''); super().draw()

    class ClickableBase(Root):
        def draw(self): print("ClickableBase ", end='');  super().draw()

    class ClickableArea(Window, ClickableBase):
        def draw(self): print("ClickableArea ", end=''); super().draw()

    class Button(ColoredRectangle, ClickableArea):
        def draw(self): print("Button ", end=''); super().draw()

    print(f" 1| ColoredRectangle.mro={extract_class_names(ColoredRectangle)}")
    print("    draw: ", end='')
    ColoredRectangle().draw()
    print()

    print(f" 2| Button.mro={extract_class_names(Button)}")
    print("    draw: ", end='')
    Button().draw()
    print()


def show_non_cooperating_classes():
    """ example for non-cooperative classes """
    print("\nshow_non_cooperating_classes\n============================")

    class LogDict(dict):                                            # dict with logging new values
        def __setitem__(self, key, value):                          # self[key] = value
            print(f" a| - LogDict['{key}']={value}")
            super().__setitem__(key, value)

    class LogOrderedDict(LogDict, OrderedDict):                     # OrderedDict unaware of other super class
        pass

    class OrderedLogDict(OrderedDict, LogDict):                     # different order only!
        pass

    print(f" 1| LogDict.mro={extract_class_names(LogDict)}")
    ld = LogDict()
    ld['one'] = 1                           # note output
    print()

    print(f" 2| LogOrderedDict.mro={extract_class_names(LogOrderedDict)}")
    lod = LogOrderedDict()
    lod['two'] = 2                          # here we have an output
    print()

    print(f" 3| OrderedLogDict.mro={extract_class_names(OrderedLogDict)}")
    old = OrderedLogDict()
    old['three'] = 3                        # but not here...
    print()


if __name__ == "__main__":
    discover_unnoticed_intruder()
    new_base_class_in_town()
    introduce_root_class()
    show_non_cooperating_classes()



###############################################################################


"""
Summary

Topics
  - mro
  - root class problem

UI / Window
  - In this snippet, and in all others on the subject of multiple inheritance, 
    we consider a highly simplified situation of specialised classes around a GUI.

Inheritance
  - Depending on the constellation, 'Window' is no longer the 'last' class 
    before 'object'. Here is the problem:
      - If 'Window.draw' wants to call the parent function, this is not possible 
        with 'object', because this class does not know a 'draw' method.
      - But if 'Window' is not in the last position and 'draw' does not call 
      'super.draw' there, this call is missing. 
    Note that the class 'Window' itself has not been changed in any way at all!
    This is just due to "later" inheritance, and you can imagine that in larger 
    class hierarchies this can happen anytime.
    So what can be done?
  - The essential idea for solving the above problem is a universal 'Root' class 
    from which all classes that play a role in multiple inheritance must inherit.
    In this way, 'Root' always moves to the last position in the MRO (before 
    'object') and can 'consume' all calls and later all parameters.
  - This has serious design implications and must be considered in the context 
    of multiple inheritance. Especially by the classes involved. It is also said 
    that classes need to co-operate. 
  - https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
  - https://fuhm.net/super-harmful/

OrderedDict
  - OrderedDict' only matters here insofar as it inherits from 'dict'. The 
    special thing about it is that the order in which the elements are inserted 
    is kept. This is something that a previous version of the 'dict' class could 
    not guarantee. In the meantime, however, this feature is also available in 
    an improved version of 'dict', though more by accident than necessity. The 
    story is here 
    https://realpython.com/python-ordereddict/
"""
