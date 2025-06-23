# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about slots.

Teaching focus
  - slots
"""

from abc import ABC

"""
Most from https://wiki.python.org/moin/UsingSlots

'__slots__' has a mixed reputation in the Python community. On the one hand, they are considered to be popular. 
Lots of people like using them. Others say that they are badly understood, tricky to get right, and don't have 
much of an effect unless there are many instances of objects that use them. 

So, what is '__slots__'? 

'__slots__' is a class variable that is usually assigned a sequence of strings that are variable names 
used by instances. See:
"""


def introducing_slots():
    """ ... """
    print("\nintroducing_slots\n=================")

    class PointV1:
        __slots__ = ('x', 'y')              # known attributes

        def __init__(self, x, y):
            self.x, self.y = x, y           # only those are allowed declared at class level

        def __repr__(self):
            return f"({self.x},{self.y})"

    p = PointV1(2, 3)
    print(f" 1| {p=}\n"
          f"    {dir(p)=}\n"
          f"    {type(PointV1.x)=}")
    # p.a = 1                                                       # error, there is no __dict__

    # Any alternative to __dict__? Yes, define them (at class level).

    class PointV2:
        __slots__ = ('x', 'y', '__dict__')                          # now we have a dict and all freedom as before

        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"({self.x},{self.y})"

    p = PointV2(2, 3)
    p.a = 1                                                         # dynamically added
    print(f" 2| {p=}\n"
          f"    dir={dir(p)}\n")


"""
From https://docs.python.org/3/howto/descriptor.html#member-objects-and-slots
and https://wiki.python.org/moin/UsingSlots and Python Language Reference

For the descriptor-expert (for us :-) ): '__slots__' are implemented at the class level by creating descriptors ... 
for each variable name. 

When a class defines __slots__, it replaces instance dictionaries with a fixed-length array of slot values. 
From a user point of view that has several effects:
  - Provides immediate detection of bugs due to misspelled attribute assignments. Only attribute names specified 
    in __slots__ are allowed.
  - Helps create immutable objects where descriptors manage access to private attributes stored in __slots__.
  - Saves memory. On a 64-bit Linux build, an instance with two attributes takes 48 bytes with __slots__ 
    and 152 bytes without. This flyweight design pattern (structural design pattern) likely only matters when 
    a large number of instances are going to be created.
  - Improves speed. Reading instance variables is 35% faster with __slots__ (as measured with Python 3.10 on 
    an Apple M1 processor).

There are some disadvantages, see end.
"""


def issues_default_values():
    """ ... """
    print("\nissues_default_values\n====================")

    class A:
        __slots__ = ('x', 'y')                                      # no default values
        # x = 12                                                    # class attribute would overwrite the descriptor

        def __init__(self):
            self.x = 12                                             # use defaults here

    class B(A):                                                     # slots variables are available in child classes,
        ...                                                         # but child subclasses will have __dict__ attributes

    class C(A):                                                     # unless they also define __slots__, which should
        __slots__ = ('z',)                                          # only contain names of additional slots

    a = A()
    b = B()
    c = C()
    print(f" 1| {hasattr(a, '__dict__')=}\n"
          f"    {hasattr(b, '__dict__')=}, {b.x=}\n"
          f"    {hasattr(c, '__dict__')=}")


def issues_inheritance():
    """ ... """
    print("\nissues_inheritance\n===================")

    class A1:
        __slots__ = ('a1',)

    class A2:
        __slots__ = ()   # must be empty, otherwise "multiple bases have instance lay-out conflict"

    class B12(A1, A2):
        ...

    class BaseA(ABC):
        __slots__ = ()

    class A(BaseA):
        __slots__ = ('x', 'y')

    class BaseB:
        __slots__ = ()

    class B(BaseB):
        __slots__ = ('x', 'y')

    class Mixin:
        __slots__ = ()

    class C(BaseA, BaseB, Mixin):                                   # no conflict here
        __slots__ = 'x', 'y'


if __name__ == "__main__":
    introducing_slots()
    issues_default_values()
    issues_inheritance()

"""
From https://wiki.python.org/moin/UsingSlots and Python Language Reference:

Default Values
    __slots__ are implemented at the class level by creating descriptors ... for each variable name. As a result, 
class attributes cannot be used to set default values for instance variables defined by __slots__; otherwise, 
the class attribute would overwrite the descriptor assignment.
Some readers might find this documentation confusing. It is not necessary for a user to implement descriptors in order 
to use __slots__. The point to remember is that default values for variables declared in __slots__ cannot be set 
using class attributes. If default values are desired, they must be set in the __init__(self) definition. 
However, it is not necessary to assign all variables a value in the __init__ function. As long as it has been declared 
in __slots__, a variable can be assigned a value using dot notation after the class has been instantiated.

Why Not Use Slots?
    There may be cases when you might not want to use __slots__; for example, if you would like for your class to use 
dynamic attribute creation or weak references. In those cases, you can add '__dict__' as the last element in the 
__slots__ declaration.

Certain Python objects may depend on the __dict__ attribute. For example, descriptor classes depend on the __dict__ 
attribute being present in the owner class. Programmers may want to avoid __slots__ in any case where another 
Python object requires __dict__ or __weak_ref__to be present. According to the Descriptor How To Guide for Python 3.9, 
the functools.cached_property() is another example that requires an instance dictionary to function correctly.

Beyond The Basics
    There are a few things to be aware of when going beyond the basics. Slots variables declared in parents are 
available in child classes. However, child subclasses will have __dict__ attributes unless they also define 
__slots__, which should only contain names of additional slots. 
    Multiple inheritance with multiple slotted parent classes can be used, but only one parent is allowed to 
have attributes created by slots. The other bases must have empty slot layouts. 

For additional details, please see the Python Language Reference.

More refs:
https://wiki.python.org/moin/UsingSlots
https://python.land/python-class-slots
https://medium.com/@stephenjayakar/a-quick-dive-into-pythons-slots-72cdc2d334e
"""
