# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about descriptors.

Teaching focus
  - descriptors
  - look up order
  - descriptor protocol
  - __get__(), __set__(), __delete__()
"""

import time


def recap_resolution_order():
    """ remember the resolution order """
    print("\nrecap_resolution_order\n======================")

    class C:
        x = 42

    c = C()
    print(f" 1| {c.__dict__=}, {c.x=}, {C.x=}")         # remember the resolution order
    c.x = 23                                            # or c.__dict__['x'] = 23
    print(f" 2| {c.__dict__=}, {c.x=}, {C.x=}")
    del c.x
    print(f" 3| {c.__dict__=}, {c.x=}, {C.x=}")

    class D:
        @property
        def x(self): return 99

    d = D()
    print(f" 4| {d.__dict__=}, {d.x=}, {D.x=}\n")       # another way to access x and another type in D


def control_access():
    """ an attribute with min and max bounds """
    print("\ncontrol_access\n==============")

    class BoundedBy:                        # see class 'Employee' below first
        def __init__(self, min_x: int, max_x: int):
            self.min_x, self.max_x = min_x, max_x

        def __set_name__(self, owner, name):
            self.name = name

        def __set__(self, obj, value):
            if not (self.min_x <= value <= self.max_x):
                raise ValueError(f"'{value}' not in [{self.min_x},{self.max_x}]")
            obj.__dict__[self.name] = value

        def __get__(self, obj, owner=None):
            return obj.__dict__[self.name]

    # We want to control access similar to a setter property, but not
    # for each property individually.

    class Employee:
        age = BoundedBy(14, 67)             # age 'allowed' to work
        income = BoundedBy(12000, 150000)   # minimum and maximum salary (for regular employees)

        def __init__(self, name, age, income):
            self.name = name
            self.age = age
            self.income = income

    print(f" 1| Employee: {Employee.__dict__=}")        # note the 'BoundedBy' objects

    alice = Employee("Alice", age=42, income=65000)
    print(f" 2|  - Alice: {alice.name=}, {alice.age=}, {alice.income=}")

    bob = Employee("Bob", age=32, income=55000)
    print(f" 3|  - Bob: {bob.name=}, {bob.age=}, {bob.income=}")

    try:
        bob.income = 3500                   # hour reduction, missing '0' by accident
    except ValueError as e:
        print(f" 4|    -> bound error: {e}")


"""
From https://realpython.com/python-descriptors

  - Descriptors are Python objects that implement a method of the 
    descriptor protocol, which gives you the ability to create objects 
    that have special behavior when they’re accessed as attributes of 
    other objects. 

  - The descriptor protocol:
    __get__(self, obj, type=None) -> object
    __set__(self, obj, value) -> None
    __delete__(self, obj) -> None
    __set_name__(self, owner, name)

  - Classification:
      - non-data descriptor:
            If your descriptor implements just .__get__(), then it’s said to 
            be a non-data descriptor. 

      - data descriptor:
            If it implements .__set__() or .__delete__(), then it’s said to 
            be a data descriptor. 

      - read-only data descriptor:
            To make a read-only data descriptor, define both __get__() and 
            __set__() with the __set__() raising an AttributeError when called. 

      Note that this difference is not just about the name, but it’s also 
      a difference in behavior. That’s because data descriptors have precedence 
      during the lookup process. 

---

Most from https://elfi-y.medium.com/python-descriptor-a-thorough-guide-60a915f67aa9

Invocation from an instance

  - The default behavior for attribute access is to get, set, or delete 
    the attribute from an object’s dictionary (see below: obj.x has 
    a lookup chain starting with obj.__dict__['x'], then type(obj).__dict__['x'], 
    and continuing through the base classes of type(obj) excluding metaclasses).

  - If the looked-up value is an object defining one of the descriptor methods, 
    then Python may override the default behavior and invoke the descriptor 
    method instead. Where this occurs in the precedence chain depends on which 
    descriptor methods were defined (again looking for attribute x on object obj):

      - data descriptors: value from __get__ method of the data descriptor 
        named after x (invoked with: desc.__get__(obj, type(obj) or obj=None 
        for class access)
      - instance variables: value of obj.__dict__ for the key named as x
      - non-data descriptors: value from __get__ method of the non-data descriptor 
        named after x
      - class variables: type(obj).__dict__ for the key named as x
      - parent’s class variables all the way along the MRO,
      - __getattr__() if it is provided.

  - object.__getattribute__() is doing most of the look up.
"""

# example: lazy property (from https://realpython.com/python-descriptors)
# or functools.cached_property (from https://docs.python.org/3/library/functools.html)

def lazy_property_example():
    """ see the loop up in action """
    print("\nlazy_property_example\n=====================")

    # what kind of descriptor is this and why does it work?
    class LazyProperty:
        def __init__(self, function):
            self.function = function
            self.name = function.__name__

        def __get__(self, obj, type=None) -> object:
            obj.__dict__[self.name] = self.function(obj)
            return obj.__dict__[self.name]

    class DeepThought:
        @LazyProperty
        def meaning_of_life(self):
            time.sleep(0.1)
            return 42

    print(f" 1| ask and remember...")
    dt2 = DeepThought()
    print(f"    {dt2.meaning_of_life}...")  # this is attribute access
    print(f"    {dt2.meaning_of_life}...")
    print(f"    {dt2.meaning_of_life}")


# more descriptor examples


def log_access_example():
    """ logging attribute access """
    print("\nlog_access_example\n==================")

    class LoggingAttribute:                 # what kind of descriptor?
        def __get__(self, obj, typ=None) -> object:
            print(" a| - get")
            return 42

        def __set__(self, obj, value) -> None:
            print(" b| - set")
            raise AttributeError("read-only")  # recommended way to implement read-only descriptors

    class C:
        x = LoggingAttribute()

    print(f" 1| access c.x")
    c = C()
    print(f" 2| {c.x=} or {C.x=}")


def complete_example():
    """ play around with all functions in the descriptor protocol """
    print("\ncomplete_example\n================")

    class UseAllProtocolMethods:
        def __init__(self):
            print(" a| - __init__")

        def __set_name__(self, owner, name):
            print(f" b| - __set_name__ {owner=}, {name=})")
            self.name = name

        def __get__(self, obj, owner=None):
            print(f" c| - __get__ {obj=}")
            return obj.__dict__.get(self.name)

        def __set__(self, obj, value):
            print(f" d| - __set__ {obj}, {value=})")
            obj.__dict__[self.name] = value

        def __delete__(self, obj):
            print(f" e| - __delete__ {obj=})")
            del obj.__dict__[self.name]

    class C:
        x = UseAllProtocolMethods()

    print(f" 1| create c")
    c = C()
    print(f" 2| access c.x")
    x = c.x
    c.x = 23
    print(f" 3| delete c.x")
    del c.x


"""
recap @property:

class C:
    @property
    def x(self) -> object:
        print("--- get")
        return 42

    @x.setter
    def x(self, _) -> None:
        print("--- set")
        raise AttributeError("read-only")

    # recap @property is syntactic sugar for:

    def getter_for_y(self) -> object:
        print("--- get")
        return 42

    def setter_for_y(self, _) -> None:
        print("--- set")
        raise AttributeError("read-only")

    y = property(getter_for_y, setter_for_y) 
"""


if __name__ == "__main__":
    recap_resolution_order()
    control_access()
    lazy_property_example()
    log_access_example()
    complete_example()

"""
References:

https://docs.python.org/3/howto/descriptor.html
https://realpython.com/python-descriptors/
https://python-reference.readthedocs.io/en/latest/docs/dunderdsc/

https://towardsdatascience.com/python-descriptors-and-how-to-use-them-5167d506af84
https://elfi-y.medium.com/python-descriptor-a-thorough-guide-60a915f67aa9
https://blog.peterlamut.com/2018/11/04/python-attribute-lookup-explained-in-detail/
"""
