# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Moon Collard' """

import functools
import time
import random
from functools import partial


def debug(func):
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]     # !r means to use 'repr', !s means 'str'
        signature = ", ".join(args_repr + kwargs_repr)
        print(f">>> called {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"<<< result {value!r}")
        return value
    return wrapper_debug


@debug
def concat(a: str, b: int) -> str:
    return f"{a}{b}"


def test_debug():
    result = concat("and the answer is: ", 42)
    print(f"01| concat: '{result}'\n")


def slow_down_v1(func):
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper_slow_down


@slow_down_v1
def countdown_v1(from_number):
    if from_number < 1:
        print("--- Liftoff")
    else:
        print(f"--- cnt: {from_number}...")
        countdown_v1(from_number - 1)


def slow_down_v2(_f=None, *, dt: float = 1):
    if callable(_f):
        @functools.wraps(_f)
        def wrapper_slow_down(*args, **kwargs):
            time.sleep(dt)
            return _f(*args, **kwargs)
        return wrapper_slow_down
    return partial(slow_down_v2, dt=dt)


@slow_down_v2(dt=0.5)                                               # also works as: @slow_down_v2
def countdown_v2(from_number):
    if from_number < 1:
        print("--- Liftoff")
    else:
        print(f"--- cnt: {from_number}...")
        countdown_v2(from_number - 1)


def test_slow_down():
    n = 3
    print(f"02| countdown from {n=} ...")
    countdown_v1(n)
    print(f"02| countdown from {n=} ...")
    countdown_v2(n)
    print()


EXAMPLES = dict()


def example(func):
    EXAMPLES[func.__name__] = func
    return func


@example
def test_case1():
    return 23


# @example                                                          # skip this
def test_case2():
    return -1


@example
def test_case3():
    return 42


def test_example_test_cases():
    print(f"03| call a random test case: test value={random.choice(list(EXAMPLES.values()))()}")
    print(f"04| {EXAMPLES.items()}")


def main():
    test_debug()
    test_slow_down()
    test_example_test_cases()


if __name__ == "__main__":
    main()

"""
For print: https://realpython.com/python-print/
"""
