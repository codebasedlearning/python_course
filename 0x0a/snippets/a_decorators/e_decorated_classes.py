# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about decorators for classes.

Teaching focus
  - decorators for classes
  - decorate classes -> same, but class 'cls' instead of function 'f'
"""

import functools
from dataclasses import dataclass

def use_singleton():
    """ example for classes """
    print("\nuse_singleton\n================")

    def singleton(cls):
        @functools.wraps(cls)
        def wrapper_singleton(*args, **kwargs):
            if wrapper_singleton.instance is None:
                wrapper_singleton.instance = cls(*args, **kwargs)
            return wrapper_singleton.instance

        wrapper_singleton.instance = None   # as before, save _the_ instance  here
        return wrapper_singleton

    @singleton
    class LightSensor:
        ...

    s1 = LightSensor()
    s2 = LightSensor()
    print(f" 1| {id(s1)=}, {id(s2)=}, identical? {s1 is s2}\n")


# here, the class itself is modified


def use_add_repr():
    """ modify class """
    print("\nuse_add_repr\n================")

    def add_str(cls):
        def my_str(this):
            return f"MyDict:{this.__dict__}"

        setattr(cls, '__str__', my_str)
        return cls

    @add_str
    class Data:
        def __init__(self, n: int):
            self.n = n

    @dataclass                              # cf. 'Declaration or Usage'
    class DataExample:
        ...

    d = Data(n=12)
    print(f" 1| d: {d}, is instance of 'Data'? {isinstance(d,Data)}")


if __name__ == "__main__":
    use_singleton()
    use_add_repr()

"""
wraps, update_wrapper
  - See https://docs.python.org/3/library/functools.html
"""
