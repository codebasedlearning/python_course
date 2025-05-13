# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet explains iterables and iterators.

Teaching focus
  - iterables
  - iterators

Iterables have an .__iter__() method that produces items on demand.
Iterators implement an .__iter__() method that typically returns self and
a .__next__() method that returns an item in every call.

According to this internal structure, you can conclude that all iterators
are iterables because they meet the iterable protocol. However, not all
iterables are iterators — only those implementing the .__next__() method.
"""

from collections.abc import Iterator, Iterable


def show_iterables():
    """ discuss iterables """
    print("\nshow_iterables\n==============")

    # All of these are 'Iterables': lists, tuples, strings, dicts, sets, ranges, etc.
    # they have an __iter__() method that produces items on demand
    list123 = [1, 2, 3]
    print(" 1| list123: ", end='')
    for item in list123:
        print(f"{item} ", end='')
    print()
    print(f" 2| {isinstance(list123, Iterable)=}")

    class Obj1234:
        def __iter__(self):
            return iter([1, 2, 3, 4])       # use built-in function iter() to create iterator from iterable

    obj1234 = Obj1234()
    print(" 3| obj1234: ", end='')
    for item in obj1234:
        print(f"{item} ", end='')
    print()
    print(f" 4| {isinstance(obj1234, Iterable)=}")   # oops?

    # Python doesn’t require you to explicitly inherit from Iterable to be
    # considered one. If your object implements the required method (__iter__()),
    # Python says: "Looks like an iterable. Quacks like one. Good enough for me."
    #
    # Precisely: Does obj.__class__ or any of its bases have an __iter__() method?
    # If yes then it’s an Iterable.

def show_iterators():
    """ discuss iterators """
    print("\nshow_iterators\n==============")

    # A list is an iterable, not an iterator — but it can give you one
    # if you call iter(list)
    list123 = [1, 2, 3]

    # 'for item in list123' is basically this (using the magic 'iter' function)
    it = iter(list123)
    print(" 1| list123: ", end='')
    while True:
        try:
            item = next(it)
            print(f"{item} ", end='')
        except StopIteration:
            break
    print()

    class Iterator1234:
        def __init__(self):
            self.data = [1, 2, 3, 4]
            self.index = 0

        def __iter__(self):
            return self                     # Required for iterator

        def __next__(self):
            if self.index >= len(self.data):
                raise StopIteration
            value = self.data[self.index]
            self.index += 1
            return value

    it = Iterator1234()
    print(" 2| Iterator1234: ", end='')
    while True:
        try:
            item = next(it)
            print(f"{item} ", end='')
        except StopIteration:
            break
    # note that from here the iterator is exhausted
    print()
    print(f" 3| {isinstance(it, Iterator)=}")

    # An object is considered an iterator if:
    # - It has a __next__() method (for getting the next item)
    # - It has an __iter__() method that returns self.


def check_its(obj):                         # check types
    def check_iterable(_obj):
        _is = isinstance(_obj, Iterable)
        _has = hasattr(_obj, "__iter__")
        try:
            iter(_obj)
            return True, _is, _has
        except TypeError:
            return False, _is, _has

    def check_iterator(_obj):
        _is = isinstance(_obj, Iterator)
        _has = hasattr(_obj, "__iter__") and hasattr(_obj, "__next__")
        return _is, _has                    # in modern Python this is always the same

    x1, x2, x3 = check_iterable(obj)
    is_x = f"{x1}" if x1 == x2 and x2 == x3 else f"{x1}/{x2}/{x3}"
    y1, y2 = check_iterator(obj)
    is_y = f"{y1}" if y1 == y2 else f"{y1}/{y2}"
    return f"(iterable? {is_x}, iterator? {is_y})"


def check_iterables_and_iterators():
    """ check for both types """
    print("\ncheck_iterables_and_iterators\n=============================")

    lst = [2, 3, 5, 7, 11]
    print(f" 1| {lst=} | {check_its(lst)}")

    lst_rev = reversed(lst)
    print(f" 2| {lst_rev=} | {check_its(lst_rev)}")

    rg = range(5)
    print(f" 3| {rg=} | {check_its(rg)}")

    lst_iter = iter(lst)
    print(f" 4| {lst_iter=} | {check_its(lst_iter)}")

    # sometimes it gets wild

    class ItemHolder:                       # note, no __iter__ !
        def __init__(self, data):
            self.data = data

        def __getitem__(self, index):
            return self.data[index]

        def __len__(self):
            return len(self.data)

    holder = ItemHolder([2, 3, 5])
    print(f" 5| {holder=} | {check_its(holder)} | items: ", end='')
    for item in holder:                     # does it work? why or why not?
        print(f"{item} ", end='')
    print()

    class ItemDelegating:                   # we use delegation here, 'data' has all we need
        def __init__(self, data):
            self.data = data

        def __iter__(self):
            return iter(self.data)          # delegating here

    items = ItemDelegating([5, 7, 11])
    print(f" 6| {items=} | {check_its(items)}")

    class CleverIterator(Iterator):         # inherits from Iterator
        def __init__(self, data):
            self.data = data
            self.index = 0

        # def __iter__(self): ...           # missing, but base has it

        def __next__(self): ...             # as before, see above

    clever = CleverIterator([1,2,3])
    print(f" 7| {clever=} | {check_its(clever)}")


if __name__ == "__main__":
    show_iterables()
    show_iterators()
    check_iterables_and_iterators()


"""
check types
  - From https://realpython.com/python-iterators-iterables
    Iterables have an .__iter__() method that produce items on demand. 
    Iterators implement an .__iter__() method that typically returns self 
    and a .__next__() method that returns an item in every call.
    According to this internal structure, you can conclude that all iterators 
    are iterables because they meet the iterable protocol. However, not all 
    iterables are iterators — only those implementing the .__next__() method.

next item and StopIteration
  - From https://realpython.com/python-iterators-iterables
    You shouldn’t use .__iter__() and .__next__() directly in your code. 
    Instead, you should use the built-in iter() and next() functions, which 
    fall back to calling the corresponding special methods.
    The StopIteration is the way 'next' says it is done.

see also:
  - https://pypi.org/project/more-itertools

Feature             Iterable            Iterator                    Generator
Implements          __iter__()          __iter__() + __next__()     Same as iterator (auto)
Works with iter()   yes                 yes (returns self)          yes
Works with next()   no(need iter first) yes                         yes
Reusable            yes                 no(consumed)                no(consumed)
Built-in Example    list, str, dict     iter(list), file obj        Generator function
Custom Example      Class w/ __iter__() Class w/ __next__()         Function w/ yield
"""
