# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Duck Corn' """

from itertools import islice
import itertools
from typing import Iterator


# Most of the solutions are inspired by the "roughly equivalent" implementation of itertools.
# So 'my_function' is not always 'my' literally. See https://docs.python.org/3/library/itertools.html.


def itertools_count():
    def my_count(start):
        n = start
        while True:
            yield n
            n += 1

    print(f"01| my_count:  {list(islice(my_count(10), 6))}\n"
          f"    cmp count: {list(islice(itertools.count(10), 6))}\n")


def itertools_repeat():
    def my_repeat(obj, times=None):
        if times is None:
            while True:
                yield obj
        for i in range(times):
            yield obj

    print(f"02| my_repeat:  {list(my_repeat(10, 3))}\n"
          f"    cmp repeat: {list(itertools.repeat(10, 3))}\n"
          f"    my_repeat:  {list(map(pow, range(10), my_repeat(2)))}\n"
          f"    cmp repeat: {list(map(pow, range(10), itertools.repeat(2)))}\n")


def itertools_chain():
    def my_chain(*iterables):
        for it in iterables:
            for element in it:
                yield element

    def f_gen(): return (i*i for i in range(6))
    rg = range(2,5,2)
    print(f"03| my_chain:  {list(my_chain(rg,f_gen()))}\n"
          f"    cmp chain: {list(itertools.chain(rg,f_gen()))}\n")


def itertools_drop_and_takewhile():
    def my_dropwhile(predicate, iterable):
        iterable = iter(iterable)
        for x in iterable:
            if not predicate(x):
                yield x
                break
        for x in iterable:
            yield x

    def my_takewhile(predicate, iterable):
        for x in iterable:
            if predicate(x):
                yield x
            else:
                break

    data = [1, 4, 9, 16, 25]
    pred = lambda x: x < 10
    print(f"04| my_dropwhile:  {list(my_dropwhile(pred, data))}\n"
          f"    cmp dropwhile: {list(itertools.dropwhile(pred, data))}\n")
    print(f"05| my_takewhile:  {list(my_takewhile(pred, data))}\n"
          f"    cmp takewhile: {list(itertools.takewhile(pred, data))}\n")


def builtin_zip():
    def my_zip(iterable1, iterable2):
        return ((iterable1[i], iterable2[i]) for i in range(min(len(iterable1),len(iterable2))))
    chars = ['A', 'B', 'C']
    numbers = [1, 2, 3]
    print(f"06| my_zip:  {list(my_zip(chars, numbers))}\n"
          f"    cmp zip: {list(my_zip(chars, numbers))}\n")


def new_cross_zip():
    class cross(Iterator):
        def __init__(self, iterable1, iterable2):
            self._it1 = iterable1
            self._it2 = iterable2
            self._i = 0
            self._len = min(len(iterable1), len(iterable2))
            #print(self._len)

        def __iter__(self):
            return self

        def __next__(self):
            if self._i >= self._len:
                raise StopIteration
            rc = (self._it1[self._i], self._it2[-self._i-1])
            self._i += 1
            return rc
    chars = ['A', 'B', 'C']
    numbers = [1, 2, 3]
    print(f"07| cross: {list(cross(chars, numbers))}\n")


def itertools_compress():
    def loc_compress(data, selectors):
        return (d for d, s in zip(data, selectors) if s)
    sieve = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]                 # see Task
    numbers = range(0, len(sieve))
    print(f"08| my_compress:  {list(loc_compress(numbers, (1-i for i in sieve)))}\n"
          f"    cmp compress: {list(itertools.compress(numbers, (1 - i for i in sieve)))}\n")


def itertools_product():
    def my_product(*args):
        pools = [tuple(pool) for pool in args]
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)
    major = [1, 2]
    minor = [5, 6]
    sub = ["alpha", "beta"]
    print(f"09| my_product:  {list(my_product(major, minor, sub))}\n"
          f"    cmp product: {list(itertools.product(major, minor, sub))}\n")


def builtin_enumerate():
    def my_enumerate(iterable):
        i = 0
        for item in iterable:
            yield i, item
            i += 1
    numbers = ['A', 'B', 'C']
    print(f"10| my_enumerate:  {list(my_enumerate(numbers))}\n"
          f"    cmp enumerate: {list(enumerate(numbers))}\n")


def string_splitlines():
    text = """Lorem ipsum... 
At vero eos et accusam... 
Stet clita kasd ..."""
    def my_splitlines(_text: str):
        start = 0
        while True:
            pos = _text.find('\n', start)
            if pos < 0:
                yield _text[start:]
                break
            yield _text[start:pos]
            start = pos+1
    print(f"11| my_splitlines:  {list(my_splitlines(text))}\n"
          f"    cmp splitlines: {list(text.splitlines())}\n")


def new_pinq_first_steps():
    def select_from(op, iterable): return (op(item) for item in iterable)
    def where(predicate, iterable): return (item for item in iterable if predicate(item))
    data = [1, 2, 3]
    print(f"12| where, select_from: {list(where(lambda x: x > 11, select_from(lambda x: (x + 10), data)))}")


def main():
    itertools_count()
    itertools_repeat()
    itertools_chain()
    itertools_drop_and_takewhile()
    builtin_zip()
    new_cross_zip()
    itertools_compress()
    itertools_product()
    builtin_enumerate()
    string_splitlines()
    new_pinq_first_steps()


if __name__ == "__main__":
    main()

"""
See https://docs.python.org/3/library/itertools.html
"""
