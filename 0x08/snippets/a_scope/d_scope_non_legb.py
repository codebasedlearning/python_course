# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet covers the scopes not affected by the LEGB rule.

Teaching focus
  - LEGB
"""


# comprehension variables Scope: lists, dictionaries and sets

def show_comprehension_scope():
    """ show comprehension scope """
    print("\nshow_comprehension_scope\n========================")

    s = 0
    for i in range(5):
        s += i
    print(f" 1| locals={locals()}")                                 # 'i' is known (last value)

    lst = [item*2 for item in range(5)]                             # (A) comprehensions, 'item' is not
    dct = {item: item**2 for item in range(5)}
    loc = [f"{locals()}" for item in range(1)]                      # try to access temp. locals()
    print(f" 2| locals={locals()}")


# exception scope

def show_exception_scope():
    """ show exception scope """
    print("\nshow_exception_scope\n====================")

    err = 1                                                         # 'err' is defined here...
    print(f" 1| {err=}, {locals()=}")
    try:
        raise RuntimeError("something wrong")
    except RuntimeError as err:                                     # exception blocks, 'err' local to the block
        print(f" 2| {err=}, {locals()=}")
    # print(err)
    print(f" 3| {err if 'err' in locals() else "?"}, {locals()=}")
    # print(err)                                                    # and 'err' may be unknown here (in case of exc.)


def non_dunder_names(dct):
    return [name for name in dct if not name.startswith('__')]


# class scope, defining a class creates a new local Python scope with different rules

class Base:
    attr = 123                                                      # class attributes

    def __init__(self, n):
        self.n = n


class Derived(Base):
    id = 456

    def __init__(self, n, m):
        super().__init__(n)
        self.m = m


def show_class_scope():
    """ show class scope """
    print("\nshow_class_scope\n================")

    print(f" 1| Base.attr={Base.attr}\n"
          f"    Base.dict={non_dunder_names(Base.__dict__)}\n"
          f"    dir(Base)={non_dunder_names(dir(Base))}")

    b = Base(12)
    print(f" 2| {b.n=}, {b.attr=}\n"
          f"    b.dict={non_dunder_names(b.__dict__)}\n"
          f"    dir(b)={non_dunder_names(dir(b))}")

    print(f" 3| Derived.id={Derived.id}\n"
          f"    Derived.dict={non_dunder_names(Derived.__dict__)}\n"
          f"    dir(Derived)={non_dunder_names(dir(Derived))}")

    d = Derived(32, 42)
    print(f" 4| {d.n=}, {d.m=}\n"
          f"    d.dict={non_dunder_names(d.__dict__)}\n"
          f"    dir(d)={non_dunder_names(dir(d))}")
    d.k = 12
    print(f" 5| {d.n=}, {d.m=}, {d.k=}\n"
          f"    d.dict={non_dunder_names(d.__dict__)}\n"
          f"    dir(d)={non_dunder_names(dir(d))}")


if __name__ == "__main__":
    show_comprehension_scope()
    show_exception_scope()
    show_class_scope()

"""
comprehension
  - The loop variable in a comprehension is only local to the structure.
"""
