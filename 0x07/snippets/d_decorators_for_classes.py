# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about decorators for classes.

Teaching focus
  - decorators for classes
  - decorate classes -> same, but class 'cls' instead of function 'f'

wraps, update_wrapper
  - See https://docs.python.org/3/library/functools.html
"""

import functools

from utils import print_function_header


@print_function_header
def define_singleton_with_function():
    """ example for classes, version 1 """

    def singleton(cls):
        @functools.wraps(cls)               # preserves name as before, but for classes
        def wrapper_singleton(*args, **kwargs):
            # the attribute is set at the time the function is called
            if wrapper_singleton._instance is None:                         # ty:ignore[unresolved-attribute]
                wrapper_singleton._instance = cls(*args, **kwargs)          # ty:ignore[unresolved-attribute]
            return wrapper_singleton._instance                              # ty:ignore[unresolved-attribute]

        wrapper_singleton._instance = None  # save _the_ instance  here     # ty:ignore[unresolved-attribute]
        return wrapper_singleton

    @singleton
    class LightSensor: ...

    s1 = LightSensor()
    s2 = LightSensor()
    print(f" 1| {id(s1)=}, {id(s2)=}, identical? {s1 is s2}")
    print(f" 2| {type(LightSensor)=}, {LightSensor.__name__=}")


@print_function_header
def define_singleton_with_class():
    """ example for classes, version 2 """

    # In fact, we do not wrap the class but replace a function in the original
    # class – called 'monkey-patching'.
    # The class itself is returned unchanged in identity, just modified.

    def singleton(cls):
        cls._instance = None                # note, __instance do not use name mangling here
    
        def __new__(inner_cls):
            if inner_cls._instance is None:
                inner_cls._instance = object.__new__(inner_cls)
            return inner_cls._instance
    
        cls.__new__ = __new__
        return cls

    @singleton
    class LightSensor:
        # Note, __init__ is always called, even if the class is already
        # initialized. So maybe you want to check for that.
        def __init__(self):
            if hasattr(self, "_initialized"):   # optional, protect a second init
                return
            self._initialized = True
        ...

    s1 = LightSensor()
    s2 = LightSensor()
    print(f" 1| {id(s1)=}, {id(s2)=}, identical? {s1 is s2}")
    print(f" 2| {type(LightSensor)=}, {LightSensor.__name__=}")


@print_function_header
def add_repr_to_class():
    """ modify class, same idea as in @dataclass """

    def add_repr(cls):
        def __repr__(self):
            return f"{self.__dict__}"

        cls.__repr__ = __repr__
        return cls

    @add_repr                               # comment out to see the difference
    class Data:
        def __init__(self, n: int):
            self.n = n

    d = Data(n=1)
    print(f" 1| {d=}, is instance of 'Data'? {isinstance(d,Data)}")
    print(f" 2| {type(Data)=}, {Data.__name__=}")


@print_function_header
def add_repr_with_parameters():
    """ modify class, same idea as before: add an outer factory function """

    def add_repr(fmt: str):
        def decorator(cls):
            def __repr__(self):
                return f"{fmt}:{self.__dict__}"
            cls.__repr__ = __repr__
            return cls
        return decorator

    @add_repr(fmt="Data-Class")
    class Data:
        def __init__(self, n: int):
            self.n = n

    d = Data(n=1)
    print(f" 1| {d=}, is instance of 'Data'? {isinstance(d,Data)}")
    print(f" 2| {type(Data)=}, {Data.__name__=}")


@print_function_header
def add_repr_flexible_style():
    """ modify class, same idea as before """

    def add_repr(cls=None, *, fmt: str = "MyDict"):
        def decorator(cls):
            def __repr__(self):
                return f"{fmt}:{self.__dict__}"
            cls.__repr__ = __repr__
            return cls

        if cls is not None:                 # used directly
            return decorator(cls)
        return decorator

    @add_repr
    class Data1:
        def __init__(self, n: int):
            self.n = n

    @add_repr(fmt="Data2-Class")
    class Data2:
        def __init__(self, n: int):
            self.n = n

    d1 = Data1(n=1)
    print(f" 1| {d1=}, is instance of 'Data1'? {isinstance(d1,Data1)}")
    print(f" 2| {type(Data1)=}, {Data1.__name__=}")

    d2 = Data2(n=2)
    print(f" 1| {d2=}, is instance of 'Data2'? {isinstance(d2,Data2)}")
    print(f" 2| {type(Data2)=}, {Data2.__name__=}")


@print_function_header
def preview_using_class_decorators():
    """ using a class as a function decorator """

    # Without params, there's only one call to __init__.
    # __call__ is the wrapper.

    class with_text_around:
        def __init__(self, some_f):
            self._some_f = some_f
            # instead of @functools.wraps(some_f)
            functools.update_wrapper(self, some_f)      # copies __name__, __doc__, etc.

        def __call__(self):
            print("--- text before")
            self._some_f()
            print("--- text after")

    # expands to:
    # print_something = with_text_around(print_something) and __init__(some_f=print_something)

    @with_text_around
    def print_something():
        print(" a| -> 'something'")

    print(" 1| call 'print_something'")
    print_something()
    print(f" 2| {print_something.__name__=}")       # ty:ignore[unresolved-attribute]


if __name__ == "__main__":
    define_singleton_with_function()
    define_singleton_with_class()
    add_repr_to_class()
    add_repr_with_parameters()
    add_repr_flexible_style()
    preview_using_class_decorators()
