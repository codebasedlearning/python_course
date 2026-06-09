# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about classes as decorators.

Teaching focus
  - classes (instead of functions) as decorators

Whether to use a decorator function or a decorator class depends on your use case.
  - Decorator functions are more commonly used in day-to-day Python programming
    because of their simplicity and readability.
      - Lightweight and concise.
      - Ideal for simple use cases where the decorator doesn't need to manage
        state or complex logic.

  - Decorator Classes
      - More flexible and powerful but involve more boilerplate code.
      - Classes allow decorators to maintain state (via instance attributes) or
        implement complex logic (beyond what's feasible with nested functions).
      - Slightly less common when a decorator function suffices, but
        indispensable in advanced use cases.

wraps, update_wrapper
  - See https://docs.python.org/3/library/functools.html
"""

import functools

from utils import print_function_header

"""
    def with_text_around(some_f):           # a decorator function
        def wrapper():
            print("--- text before")
            some_f()
            print("--- text after")
        return wrapper                      # return the inner function

"""

@print_function_header
def using_class_decorators_for_functions():
    """ using a class as a decorator """

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


@print_function_header
def using_class_decorators_for_functions_with_parameters():
    """ first example using a class as decorator """

    # With params, the first call goes to __init__ with the params,
    # and the second call (with the function) goes to __call__.

    class with_text_around:
        def __init__(self, before: str = "---", after: str = "---"):
            self._before = before
            self._after = after

        def __call__(self, some_f):
            @functools.wraps(some_f)
            def wrapper():
                print(self._before)
                some_f()
                print(self._after)

            # functools.update_wrapper(wrapper, some_f)
            return wrapper

    @with_text_around(before=">>> start", after="<<< end")
    def print_something():
        print(" a| -> 'something'")

    print(" 1| call 'print_something'")
    print_something()
    print(f" 2| {print_something.__name__=}")       # ty:ignore[unresolved-attribute]


@print_function_header
def add_repr_with_class_decorator_v1():
    """ modify class """

    # This works, but Data is now an add_repr instance.
    # It behaves like a class (callable) but isinstance(d, Data) does not work.

    class add_repr:
        def __init__(self, cls):
            def __repr__(self):
                return f"{self.__dict__}"

            cls.__repr__ = __repr__
            self._cls = cls

        def __call__(self, *args, **kwargs):
            return self._cls(*args, **kwargs)

    @add_repr
    class Data:
        def __init__(self, n: int):
            self.n = n
    
    d = Data(n=12)
    print(f" 1| {d=}")                      # error: {isinstance(d,Data)=}
    print(f" 2| {type(Data)=}")


@print_function_header
def add_repr_with_class_decorator_v2():
    """ modify class """

    class add_repr:
        def __new__(cls, decorated_cls):
            def __repr__(self):
                return f"{self.__dict__}"
            decorated_cls.__repr__ = __repr__
            return decorated_cls
    
    @add_repr
    class Data:
        def __init__(self, n: int):
            self.n = n
    
    d = Data(n=2)                                                       # ty:ignore[call-non-callable]
    print(f" 1| {d=}, is instance of 'Data'? {isinstance(d,Data)}")     # ty:ignore[invalid-argument-type]
    print(f" 2| {type(Data)=}, {Data.__name__=}")                       # ty:ignore[unresolved-attribute]

@print_function_header
def add_repr_with_class_decorator_with_parameters():
    """ modify class """

    # __init__ gets the params, __call__ gets the class
    # and returns it directly

    class add_repr:
        def __init__(self, fmt: str = "MyDict"):
            self._fmt = fmt
    
        def __call__(self, cls):
            fmt = self._fmt                 # why copy?
            def __repr__(self):
                return f"{fmt}:{self.__dict__}"
            cls.__repr__ = __repr__
            return cls

    @add_repr(fmt="Data-Class")
    class Data:
        def __init__(self, n: int):
            self.n = n

    d = Data(n=2)
    print(f" 1| {d=}, is instance of 'Data'? {isinstance(d, Data)}")
    print(f" 2| {type(Data)=}, {Data.__name__=}")


@print_function_header
def add_repr_with_class_decorator_flexible_style():
    """ modify class """

    class add_repr:
        def __new__(cls, decorated_cls=None, *, fmt: str = "MyDict"):
            instance = super().__new__(cls)
            instance._fmt = fmt
            if decorated_cls is not None:   # @add_repr — class passed directly
                return instance(decorated_cls)
            return instance                 # @add_repr(...) — return decorator

        def __call__(self, cls):
            fmt = self._fmt                 # ty:ignore[unresolved-attribute]
            def __repr__(self):
                return f"{fmt}:{self.__dict__}"
            cls.__repr__ = __repr__
            return cls

    @add_repr
    class Data1:
        def __init__(self, n: int):
            self.n = n

    @add_repr(fmt="Data2-Class")
    class Data2:
        def __init__(self, n: int):
            self.n = n

    d1 = Data1(n=1)                                                         # ty:ignore[missing-argument, unknown-argument]
    print(f" 1| {d1=}, is instance of 'Data1'? {isinstance(d1,Data1)}")     # ty:ignore[invalid-argument-type]
    print(f" 2| {type(Data1)=}, {Data1.__name__=}")                         # ty:ignore[unresolved-attribute]

    d2 = Data2(n=2)
    print(f" 1| {d2=}, is instance of 'Data2'? {isinstance(d2,Data2)}")
    print(f" 2| {type(Data2)=}, {Data2.__name__=}")


if __name__ == "__main__":
    using_class_decorators_for_functions()
    using_class_decorators_for_functions_with_parameters()
    add_repr_with_class_decorator_v1()
    add_repr_with_class_decorator_v2()
    add_repr_with_class_decorator_with_parameters()
    add_repr_with_class_decorator_flexible_style()
