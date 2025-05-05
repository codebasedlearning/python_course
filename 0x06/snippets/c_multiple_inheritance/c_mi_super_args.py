# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses multiple inheritance with respect to arguments.

Teaching focus
  - calling base-class functions with arguments (kwargs)
"""

from typing import Type

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


def extract_class_names(cls: Type[object]):
    return [item.__name__ for item in cls.__mro__]


def extend_signature():
    """ signature change """
    print("\nextend_signature\n================")

    class Root:
        def draw(self): print("Root ", end='')          # explicitly no call to super().draw()

    class Window(Root):
        def draw(self, redraw: bool): print(f"Window({redraw}) ", end=''); super().draw()

    class ColoredRectangle(Window):
        def draw(self, redraw: bool): print(f"ColoredRectangle({redraw}) ", end=''); super().draw(redraw)   # just base

    print(f" 1| ColoredRectangle.mro={extract_class_names(ColoredRectangle)}")
    print("    draw: ", end='')
    ColoredRectangle().draw(True)
    print()

    class ClickableArea(Root):
        def draw(self, focus: bool):
            print(f"ClickableArea({focus}) ", end='')
            super().draw()  # only Root

    # different draws combined -> problem
    class Button(ColoredRectangle, ClickableArea):
        def draw(self, redraw: bool, focus: bool):
            print(f"Button({redraw},{focus}) ", end='')
            # super().draw(redraw)      # focus?

    # extended, or with changed order -> problem
    class Checkbox(ColoredRectangle, ClickableArea, Window):
        def draw(self, redraw: bool):
            print(f"Checkbox({redraw}) ", end='')
            super().draw(redraw)

    print(f" 2| Button.mro={extract_class_names(Button)}")
    print("    draw: ", end='')
    Button().draw(redraw=True, focus=True)
    print()

    print(f" 3| Checkbox.mro={extract_class_names(Checkbox)}")
    print("    draw: ", end='')
    # Checkbox().draw(True)
    print()


def extend_signature_with_kwargs():
    """ signature change """
    print("\nextend_signature_with_kwargs\n============================")

    class Root:
        def draw(self, **kwargs):
            print(f"Root({kwargs}) ", end='')

    # note that 'redraw' is removed from kwargs
    class Widget(Root):
        def draw(self, redraw: bool, **kwargs):
            print(f"Widget({redraw},{kwargs}) ", end='')
            super().draw(**kwargs)          # call it with or without 'redraw'???

    print(f" 1| Widget.mro={extract_class_names(Widget)}")
    print("    draw: ", end='')
    Widget().draw(redraw=True, more_args=23)
    print()

    # the solution is to keep the signature and, optionally, go with kwargs (only);
    # avoid *args unless you’re mimicking built-ins, or you’re explicitly designing for positional extensibility

    # add '*' (everything after must be passed as keyword arguments) and a (necessary) param '_'
    # as 'draw(self, *, **kwargs)' is invalid

    class Window(Root):
        def draw(self, *, _=None, **kwargs):
            redraw = kwargs.get("redraw", False)
            print(f"Window({redraw},{kwargs}) ", end='')
            super().draw(**kwargs)

    class ColoredRectangle(Window):
        def draw(self, *, _=None, **kwargs):
            redraw = kwargs.get("redraw", False)
            print(f"ColoredRectangle({redraw},{kwargs}) ", end='')
            super().draw(**kwargs)

    print(f" 2| ColoredRectangle.mro={extract_class_names(ColoredRectangle)}")
    print("    draw: ", end='')
    ColoredRectangle().draw(redraw=True)
    print()

    class ClickableArea(Root):
        def draw(self, *, _=None, **kwargs):
            focus = kwargs.get("focus", False)
            print(f"ClickableArea({focus},{kwargs}) ", end='')
            super().draw(**kwargs)

    # different draws combined -> problem
    class Button(ColoredRectangle, ClickableArea):
        def draw(self, *, _=None, **kwargs):
            redraw = kwargs.get("redraw", False)
            focus = kwargs.get("focus", False)
            print(f"Button({redraw},{focus},{kwargs}) ", end='')
            super().draw(**kwargs)

    # extended, or with changed order -> problem
    class Checkbox(ColoredRectangle, ClickableArea, Window):
        def draw(self, *, _=None, **kwargs):
            redraw = kwargs.get("redraw", False)
            focus = kwargs.get("focus", False)
            print(f"Checkbox({redraw},{focus},{kwargs}) ", end='')
            super().draw(**kwargs)

    print(f" 3| Button.mro={extract_class_names(Button)}")
    print("    draw: ", end='')
    Button().draw(redraw=True, focus=True)
    print()

    print(f" 4| Checkbox.mro={extract_class_names(Checkbox)}")
    print("    draw: ", end='')
    Checkbox().draw(redraw=True, focus=True)
    print()


if __name__ == "__main__":
    extend_signature()
    extend_signature_with_kwargs()


###############################################################################


"""
Summary

Topics
  - calling base-class functions with arguments (kwargs)

Signature Change
  - The core of the problem here is the extension of the signature of the 
    'draw' method. This is not an uncommon situation in inheritance. Derived 
    classes often represent an extension and methods are augmented with 
    additional parameters.
    However, we have learnt that this situation is very fragile and can 
    change at any time. Depending on the order in the MRO, it is not clear 
    which parameters 'super.draw' gets.

kwargs Solution
Basically, there are two possible solutions:
  - One is to leave the signature of the overridable functions unchanged. 
    That way the arguments are clear and everything works as expected.
  - If there are reasons not to do this, you can wrap all parameters as 
    'named parameters' in 'kwargs' and add '**kwargs' to the corresponding 
    signatures.
    This will allow the methods called in the hierarchy to use 'their' 
    parameters from 'kwargs' and pass the remaining ones (or all) on. We 
    have already seen that the used parameters are removed from 'kwargs'.
    Finally, the hierarchy is rounded off as before with a universal base 
    class 'Root', which consumes all 'kwargs'.
  - Note: In principle, 'args' could also be used, but using 'positional 
    parameters' makes things worse rather than better (imho).
"""
