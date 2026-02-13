# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses generators.

Teaching focus
  - generator functions
  - yield
  - generator expressions

A generator expression is similar to a list comprehension, but instead of
creating a list and storing it in memory, it creates a generator that can then
be iterated over.

The syntax is very similar to a list comprehension, but uses parentheses ()
instead of square brackets [].

Pro/Con?
"""


def simple_generator():
    """ a simple generator with values 1,2,3 """
    yield 1                                 # it is like return but continues here for the next iteration
    yield 2                                 # until the function ends
    yield 3


def factorial_generator(limit):
    """ a generator creating factorials """
    fact = 1
    for i in range(1, limit + 1):
        fact *= i
        yield fact                          # also like return, but all local vars live on


def show_generators():
    """ classes and type hints """
    print("\nshow_generators\n==================")

    print(" 1| gen-values:", end='')
    for value in simple_generator():
        print(f" {value=}", end='')
    print()

    print(" 2| factorial:", end='')
    for number in factorial_generator(5):
        print(f" {number=}", end='')
    print()

    print(" 3| generator expression:", end='')
    gen_exp = (x ** 2 for x in range(4))

    for value in gen_exp:
        print(f" {value=}", end='')
    print()

    # factorial = [number for number in factorial_generator(5)]
    factorial = [*factorial_generator(5)]   # if you explicitly want a list
    print(f" 4| {factorial}")


if __name__ == "__main__":
    show_generators()
