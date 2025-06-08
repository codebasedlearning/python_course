# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about parameterized decorators.

Teaching focus
  - decorators with parameters, i.e. parameterize the decorator itself
  - but... how can we equip the decorator with parameters?
"""

import functools
from functools import partial


def do_twice_or_more():
    """ decorate a function and call it a number of times """
    print("\ndo_twice_or_more\n================")

    # remember do_twice

    def do_repeat(some_f, n):                                             # first try
        @functools.wraps(some_f)
        def wrapper_do_repeat(*args, **kwargs):
            value = None
            for _ in range(n):
                value = some_f(*args, **kwargs)
            return value
        return wrapper_do_repeat

    def f():
        print(f" a| -> in 'f'")

    print(" 1| define 'f'")
    f = do_repeat(f, 3)                     # remember the original idea
    print(f" 2| call 'f'")                  # -> this works
    f()

    # let's try the @-syntax

    # @do_repeat(3)
    def g():
        print(f" b| -> in 'g'")
    print(f" 3| call 'g'")
    g()

    # => error: [...] missing 1 required positional argument: 'n'
    #
    # 'do_repeat' expects the target function `some_f` and the parameter `n`
    # simultaneously, but that does not work with the decorator syntax,
    # or short
    #   do_repeat(3)(g) != do_repeat(g,3)
    #
    # any idea?


    # do_repeat(3) must return a decorator function, and this decorator
    # must then be applied to g => increase level, return a decorator...


def do_repeat_with_params():
    """ decorator function with parameters """
    print("\ndo_repeat_with_params\n=====================")

    def do_repeat(n):
        # here is the decorator function
        def decorator_repeat(f):
            @functools.wraps(f)
            def wrapper_repeat(*args, **kwargs):    # btw. closure for 'n' and 'f'
                value = None
                for _ in range(n):
                    value = f(*args, **kwargs)
                return value
            return wrapper_repeat
        # end of decorator function
        return decorator_repeat

    @do_repeat(3)
    def g():
        print(f" a| -> in 'g'")

    print(f" 1| call 'g'")                  # -> this works
    g()

    """
    Now we have a decorator function with parameters. But what if we want to
    use this decorator function with or without parameters?
    """

    # @do_repeat
    # def h():
    #     print(f" b| -> in 'h'")
    #
    # print(f" 2| call 'h'")
    # h()
    #
    # => error, pos. arg. missing...


def do_repeat_flexible_style():
    """ do_repeat again, but with a flexible style """
    print("\ndo_repeat_flexible_style\n========================")

    # remember: any argument after '*' must be specified using a keyword

    def do_repeat(_f=None, *, n=2):
        def decorator_repeat(f):            # as before
            @functools.wraps(f)
            def wrapper_repeat(*args, **kwargs):
                print(f" a| _f callable? {callable(_f)}, {_f=}")
                value = None
                for _ in range(n):
                    value = f(*args, **kwargs)
                return value
            return wrapper_repeat

        # two cases: if _f is given, apply the decorator,
        #            otherwise use the parameterized version

        if callable(_f):
            return decorator_repeat(_f)
        else:
            return decorator_repeat

    @do_repeat(n=3)                         # need to use named parameters
    def g():
        print(f" b| -> in 'g'")

    print(f" 1| repeat 'g' 3 times, name of g: '{g.__name__}'")
    g()

    @do_repeat
    def h():
        print(f" c| -> in 'h'")
    print(f" 2| repeat 'h' 2 times, name of h: '{h.__name__}'")
    h()
    print()

    # there is another way to do the same thing: using 'partial'

    def my_pow(base, n): return base ** n
    pow2 = partial(my_pow, base=2)          # partial -> fix some args (as in math.)
    print(f" 3| 2^3={my_pow(2, 3)}={pow2(n=3)}\n")

    def do_repeat_alt(_f=None, *, n=2):                                  # one level less
        if callable(_f):                    # the no-param case
            @functools.wraps(_f)
            def wrapper_repeat(*args, **kwargs):
                value = None
                for _ in range(n):
                    value = _f(*args, **kwargs)
                return value
            return wrapper_repeat                                       # _f is given
        return partial(do_repeat_alt, n=n)                               # _f is still a free parameter, only n is fixed

    @do_repeat_alt(n=3)
    def p():
        print(f" d| -> in 'p'")
    print(f" 4| repeat 'p' 3 times")
    p()

    @do_repeat_alt
    def q():
        print(f" e| -> in 'q'")
    print(f" 5| repeat 'q' 2 times")
    q()


if __name__ == "__main__":
    do_twice_or_more()
    do_repeat_with_params()
    do_repeat_flexible_style()



"""
partial:
  - https://docs.python.org/3/library/functools.html
  - https://stackoverflow.com/questions/5929107/decorators-with-parameters
"""
