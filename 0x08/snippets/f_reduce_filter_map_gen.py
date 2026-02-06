# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates reduce, filter, map and enumerate and previews generator expressions.

Teaching focus
  - reduce
  - filter
  - map
  - generator expression
"""

from functools import reduce


def functional_style():
    """ functional_style """
    print("\nfunctional_style\n================")

    sum_1_9 = reduce(lambda result, i: result+i, range(1, 10), 11)  # it is: result += i, i in iterable
    print(f" 1| sum 1..9 + 11 = {sum_1_9}")                         # (A) reduce

    odds = filter(lambda i: i % 2 != 0, range(1, 10))               # returns an iterator, not a list
    print(f" 2| odds in 1..9: {[*odds]}")                           # iterator at end!

    evens = filter(lambda i: i % 2 == 0, range(1, 10))              # (B) filter
    d = reduce(lambda dct, item: dct | {item[0]: item[1]}, enumerate(evens), {})
    print(f" 3| evens in 1..9 as dict: {d}")

    rg2x = map(lambda i: i+i, range(1, 10))                         # (C) map
    print(f" 4| map 2*rg: {list(rg2x)}")                            # or *rg2

    upper = map(lambda s: s.upper(), ["one", "two", "three"])
    print(f" 5| map upper: {list(upper)}")

    measured = ["1.23", "4.5", "-6.78"]
    temps = list(filter(lambda t: t > 0, map(float, measured)))
    print(f" 6| temps>0: {temps}")

    tuples = list(map(lambda i, j: i+j, range(1, 10), range(20, 10, -1)))   # multiple iterables
    print(f" 7| 21-tuples: {tuples}")


def pythonic_style():
    """ pythonic_style """
    print("\nmore_pythonic_style\n===================")

    rg = [int(i / 2) for i in range(-6, 20, 2) if i > 0]            # recap "didactic" comprehension, eq. range(1, 10)
    print(f" 1| rg = {rg}")

    list_map = list(map(lambda i: i+i, range(1, 5)))                # list with map
    list_comp = [i+i for i in range(1, 5)]                          # comprehension
    gen_ex = (i+i for i in range(1, 5))                             # generator expression...
    list_gen = list(gen_ex)                                         # list with generator expression
    print(f" 2| lists: {list_map} vs. {list_comp} vs. {list_gen}")

    evens_filter = list(filter(lambda i: i % 2 == 0, range(1, 5)))  # list with filter
    evens_gen = list(i for i in range(1, 5) if i % 2 == 0)          # list with generator expression - preview!
    print(f" 3| lists: {evens_filter} vs. {evens_gen}")


if __name__ == "__main__":
    functional_style()
    pythonic_style()


"""
reduce
See https://docs.python.org/3/library/functools.html

filter
https://docs.python.org/3/library/functions.html?highlight=map#filter

map
https://docs.python.org/3/library/functions.html?highlight=map#map

generator expression
https://docs.python.org/3/glossary.html#term-generator-iterator
"""
