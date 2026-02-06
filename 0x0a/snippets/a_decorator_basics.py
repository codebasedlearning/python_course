# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about simple decorators.

Teaching focus
  - first decorators - what is a decorator?
  - recap: functions are first-class objects (global and local)
"""

from datetime import datetime
from typing import Callable
import time


def op_plus(a: int, b: int) -> int:
    """ simple addition """
    return a + b


def call_op_with(a: int, b: int, op: Callable[[int, int], int]) -> int:
    """ calculate with a given operator """
    return op(a, b)


def functions_are_first_class_citizens():  # functions as arguments
    """ work with functions as objects """
    print("\nfunctions_are_first_class_citizens\n==================================")

    n, m = 3, 2

    # call with a global object
    print(f" 1| {n=}, {m=}, n+m={call_op_with(n, m, op_plus)}")

    def op_mul(a, b):
        """ simple multiplication """
        return a * b

    # or with a local object
    print(f" 2| {n=}, {m=}, n*m={call_op_with(n, m, op_mul)}")

    # or with a lambda expression
    print(f" 3| {n=}, {m=}, n**m={call_op_with(n, m, lambda a, b: a ** b)}")


def functions_as_results():
    """ return functions as a result """
    print("\nfunctions_as_results\n====================")

    def op_from_input(op_str):
        if op_str == "+":
            return op_plus
        if op_str == "*":
            def op_mul(a, b):
                return a * b
            return op_mul
        raise NotImplementedError(f"op {op_str} not defined")

    n, m = 3, 2
    print(f" 1| {n=}, {m=}, n*m={call_op_with(n, m, op_from_input('*'))}")


"""
Assume we want to print some text before and after a function call.
How can we archive this in a general way?
"""

"""
Hint: We need functions as arguments and return values.
"""


def print_text_around():
    """ print some text before and after a function call """
    print("\nprint_text_around\n=================")

    # A decorator function is a higher-order function that takes another
    # function as its argument and returns a new function (often wrapping
    # the original function with some additional behavior).

    def with_text_around(some_f):  # a decorator function
        def wrapper():
            print("--- text before")
            some_f()
            print("--- text after")
        return wrapper  # return the inner function

    # the function we want to wrap (aka 'decorate')
    def print_something():
        print(" a| -> 'something'")

    # re-define the function - this is the basic idea of all decorators
    print_something = with_text_around(print_something)

    print(" 1| call 'print_something'")
    print_something()

    # @-syntax: print_more_text = with_text_around(print_more_text)

    @with_text_around
    def print_more_text():
        print(" b| -> 'more text'")

    print(" 2| call 'print_more_text'")
    print_more_text()


def more_decorator_functions():
    """ more decorator functions """
    print("\nmore_decorator_functions\n========================")

    def at_office_hours_only(some_f):  # another decorator function
        def wrapper():
            if 7 <= datetime.now().hour < 22:
                some_f()  # conditional calling
            else:
                pass
        return wrapper

    # same as: print_more = at_office_hours_only(print_more)

    @at_office_hours_only
    def print_more():  # function we want to 'decorate'
        print(" a| -> 'more'")

    print(f" 1| call function at {datetime.now().hour}h")
    print_more()

    def time_it(some_f):
        def wrapper():
            t0 = time.process_time()
            some_f()
            t1 = time.process_time()
            print(f"--- duration: dt={t1 - t0}")
        return wrapper

    @time_it  # syntactic sugar for f = decorator(f)
    def print_fibs():
        def fib(n):
            return fib(n - 1) + fib(n - 2) if n >= 3 else 1 if n >= 1 else 0

        fibs = [fib(n) for n in range(1, 30)]
        print(f" b| -> {fibs=}")

    print(f" 2| call fib(1..)")
    print_fibs()


def nested_decorator():
    """ decorator order matters """
    print("\nnested_decorator\n================")

    def deco1(some_f):
        def wrapper():
            print(" a| -> deco1")
            some_f()
        return wrapper

    def deco2(some_f):
        def wrapper():
            print(" b| -> deco2")
            some_f()
        return wrapper

    @deco1
    @deco2
    def f(): print(" c| -> in f")

    @deco2
    @deco1
    def g(): print(" d| -> in g")

    print(f" 1| call f")
    f()
    print(f" 2| call g")
    g()


if __name__ == "__main__":
    functions_are_first_class_citizens()
    functions_as_results()
    print_text_around()
    more_decorator_functions()
    nested_decorator()

"""
  - A decorator is a Python construct created when the decorator function 
    is applied to another function, often via the `@` syntax.
  - The term "decorator" in Python is a somewhat flexible concept and can 
    refer to different aspects depending on the context.

Refs:
  - https://realpython.com/primer-on-python-decorators/#simple-decorators
  - https://realpython.com/primer-on-python-decorators/
  - https://peps.python.org/pep-0318/#background
"""
