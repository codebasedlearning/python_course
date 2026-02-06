# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about decorators for functions with parameters and return value.

Teaching focus
  - decorators for functions with parameters
"""

import functools
import time


def do_twice_without_args():
    """ work with functions as objects """
    print("\ndo_twice_without_args\n=====================")

    # 'decorator' that runs a function twice
    def do_twice(some_f):
        def wrapper_do_twice():             # so many 'wrapper'...
            some_f()
            some_f()
        return wrapper_do_twice

    @do_twice
    def print_some_text():
        print(" a| -> 'some text'")

    print(" 1| call 'print_some_text'")
    print_some_text()                       # printed twice?


"""
Now, let's try to do the same with parameters.
But how?
"""


def do_twice_with_args():
    """ work with functions as objects """
    print("\ndo_twice_with_args\n==================")

    # version 1: first try, does it work?

    def do_twice_v1(some_f):
        def wrapper_do_twice():
            some_f()
            some_f()
        return wrapper_do_twice

    @do_twice_v1
    def print_text_v1(text: str):
        print(f" a| -> text: '{text}'")

    print(" 1| call 'print_text_v1'")
    # print_text_v1('ok, here is the text')

    # => error: [...] takes 0 positional arguments, but 1 was given
    print(f" 2| whats is 'print_text_v1': {print_text_v1=}")
    print(f" 3| name of 'print_text_v1': '{print_text_v1.__name__}'\n")
    # keep this 'name problem' in mind for later!

    # version 2: second try, does it work?

    def do_twice_v2(some_f):
        def wrapper_do_twice(text: str):
            some_f(text)
            some_f(text)
        return wrapper_do_twice

    @do_twice_v2
    def print_text_v2(text: str):
        print(f" b| -> text: '{text}'")

    print(" 4| call 'print_text_v2'")
    print_text_v2('ok, here is the text')

    # => works,
    #    but where is the problem here?

    @do_twice_v2
    def print_text_v2_int(n: int):
        print(f" c| -> n: '{n}'")

    print(" 5| call 'print_text_v2_int'")
    print_text_v2_int(23)

    # => works,
    #    so, is there still a problem?

    @do_twice_v2
    def print_text_v2_int_str(n: int, text: str):
        print(f" d| -> n: '{n}', text: '{text}'")

    print(" 6| call 'print_text_v2_int_str'")
    # print_text_v2_int_str(42,"ok, here is the text")

    # => error: [...] takes 1 positional argument, but 2 were given
    print()

    # version 3: third try, does it work?

    def do_twice_v3(some_f):
        def wrapper_do_twice(*args, **kwargs):      # forwarding parameters
            some_f(*args, **kwargs)
            some_f(*args, **kwargs)
        return wrapper_do_twice

    @do_twice_v3
    def print_text_v3_str(text: str):
        print(f" e| -> text: '{text}'")

    @do_twice_v3
    def print_text_v3_int_str(n: int, text: str):
        print(f" f| -> n: '{n}', text: '{text}'")

    print(" 7| call 'print_text_v3_str' and 'print_text_v3_int_str'")
    print_text_v3_str('ok, here is the text')
    print_text_v3_int_str(99,"ok, here is the text")

    # => works in all cases!

    # version 4: one more... what about this?

    def do_twice_v4(some_f, text):                                            # not a solution, why?
        def wrapper_do_twice():
            some_f(text)
            some_f(text)
        return wrapper_do_twice
    # @do_twice_v4
    def print_text_v4(text: str):
        print(f" g| -> text: '{text}'")

    # => error: [...] missing 1 required positional argument: 'text'


"""
What about return values of the decorated function?
Any idea?
"""


def time_it_with_return():
    """ work with functions with return values """
    print("\ntime_it_with_return\n===================")

    def time_it(some_f):
        def wrapper(*args, **kwargs):
            t0 = time.process_time()
            z = some_f(*args, **kwargs)     # just return the result from the wrapper
            t1 = time.process_time()
            print(f"--- duration: dt={t1 - t0}")
            return z # ,t1-t0; if you want both, return a tuple
        return wrapper

    @time_it
    def calc_a_plus_b(a: int, b: int):
        s = a+b
        print(f" a| -> {a}+{b}={s}")
        return s

    print(" 1| call 'calc_a_plus_b'")
    y = calc_a_plus_b(2,3)
    print(f" 2| {y=}")


def who_am_I():
    """ solve the name problem with functools.wraps """
    print("\nwho_am_I\n========")

    def time_it(some_f):
        @functools.wraps(some_f)
        def wrapper(*args, **kwargs):
            t0 = time.process_time()
            z = some_f(*args, **kwargs)
            t1 = time.process_time()
            return z, t1-t0
        return wrapper

    @time_it
    def calc_a_times_b(a: int, b: int):
        s = a*b
        print(f" a| -> {a}*{b}={s}")
        return s

    print(" 1| call 'calc_a_times_b'")
    y,dt = calc_a_times_b(2,3)
    print(f" 2| {y=}, {dt=}")

    print(f" 3| name of 'calc_a_times_b': '{calc_a_times_b.__name__}'")


if __name__ == "__main__":
    do_twice_without_args()
    do_twice_with_args()
    time_it_with_return()
    who_am_I()

"""
See
  - https://docs.python.org/3/library/functools.html
"""
