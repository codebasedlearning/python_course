# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about parameterized decorators.

Teaching focus
  - decorators with parameters, i.e. parameterize the decorator itself
  - but... how can we equip the decorator with parameters?

partial:
  - https://docs.python.org/3/library/functools.html
  - https://stackoverflow.com/questions/5929107/decorators-with-parameters
"""

import functools
from functools import partial

from utils import print_function_header


@print_function_header
def do_twice_or_more():
    """ decorate a function and call it a number of times """

    # remember do_twice; skip args, return values and @functools.wraps

    def do_repeat(some_f, n):               # first try
        def wrapper_do_repeat():
            for _ in range(n): some_f()
        return wrapper_do_repeat

    def f():
        print(" a| -> in 'f'")

    print(" 1| define 'f'")
    f = do_repeat(f, 3)                     # remember the original idea
    print(" 2| call 'f'")                   # -> this works
    f()

    # let's try the @-syntax

    print(" 3| define 'g'")

    # @do_repeat(3)
    def g():
        print(" b| -> in 'g'")
    print(" 4| call 'g'")
    g()

    # => error: [...] missing 1 required positional argument: 'n'

    # 'do_repeat' expects the target function `some_f` and the parameter `n`
    # simultaneously, but that does not work with the decorator syntax,
    #
    # any idea?


    # What if we think of 'currying', first apply `n`, then `some_f`
    #
    # g = do_repeat(3)(g)
    #
    # Here do_repeat(3) must return a decorator function, and this decorator
    # must then be applied to g => ok, increase level, return a decorator...
    #
    # and the reason is did not work before is simply
    #   do_repeat(3)(g) != do_repeat(g,3)


@print_function_header
def do_repeat_with_params():
    """ decorator function with parameters """

    def do_repeat(n):
        def decorator_repeat(some_f):            # here is the decorator function as before
            def wrapper_repeat():
                for _ in range(n): some_f()
            return wrapper_repeat           # end of decorator function
        return decorator_repeat

    @do_repeat(3)
    def f():
        print(" a| -> in 'f'")
    print(" 1| call 'f'")                   # -> this works
    f()

    def g():
        print(" b| -> in 'g'")
    g = do_repeat(n=4)(g)                   # our motivation – works as well
    print(" 2| call 'g'")
    g()


    # Now we have a decorator function with parameters. But what if we want to
    # use this decorator function with or without parameters?

    # @do_repeat
    # def h():
    #     print(f" c| -> in 'h'")
    #
    # print(f" 3| call 'h'")
    # h()
    #
    # => error, pos. arg. missing...
    #
    # We need to differentiate the two cases.


@print_function_header
def do_repeat_flexible_style():
    """ do_repeat again, but with a flexible style """

    # remember: any argument after '*' must be specified using a keyword

    def do_repeat(_f=None, *, n=2):
        def decorator_repeat(some_f):            # as before
            def wrapper_repeat():
                for _ in range(n): some_f()
            return wrapper_repeat

        # two cases: if _f is given, apply the decorator,
        #            otherwise n is given, then use the parameterized version

        print(f" a| callable? {callable(_f)}, {_f=}")
        if callable(_f):
            return decorator_repeat(_f)
        else:
            return decorator_repeat

    @do_repeat(n=3)                         # need to use named parameters
    def f():
        print(" b| -> in 'f'")

    print(" 1| call 'f'")
    f()

    @do_repeat
    def g():
        print(" c| -> in 'g'")
    print(" 2| call 'g'")
    g()


@print_function_header
def do_repeat_partially():
    """do_repeat again, but using 'partial' """

    # there is another way to do the same thing: 'partial'

    def my_pow(base, n):
        return base ** n

    pow2 = partial(my_pow, base=2)          # partial -> fix some args (as in math.)
    print(f" 1| 2^3={my_pow(2, 3)}={pow2(n=3)}\n")

    def do_repeat(_f=None, *, n=2):         # like the initial version
        if callable(_f):                    # the no-param = function-only case
            def wrapper_repeat():
                for _ in range(n): _f()
            return wrapper_repeat
        return partial(do_repeat, n=n)      # _f is still a free parameter, only n is fixed

    @do_repeat(n=3)                         # need to use named parameters
    def f():
        print(" a| -> in 'f'")
    print(" 1| call 'f'")
    f()

    @do_repeat
    def g():
        print(" b| -> in 'g'")
    print(" 2| call 'g'")
    g()


@print_function_header
def show_complete():

    def do_repeat(_f=None, *, n=2):                 # case 1 or 2 depends on _f==None
        def decorator_repeat(some_f):
            @functools.wraps(some_f)                # for the function name
            def wrapper_repeat(*args, **kwargs):    # for the function args
                value = None
                for _ in range(n):                  # functionality of do_repeat
                    value = some_f(*args, **kwargs)
                return value                        # return value
            return wrapper_repeat

        # two cases: if _f is given, apply the decorator resulting in a wrapper,
        #            otherwise if n is given, then use the parameterized version being a decorator

        print(f" a| callable? {callable(_f)}, {_f=}")
        if callable(_f):                            # case 1: function only
            return decorator_repeat(_f)
        else:
            return decorator_repeat                 # case 2: do_repeat with parameters

    # with partial
    #
    # def do_repeat(_f=None, *, n=2):
    #     if callable(_f):                            # two cases
    #         @functools.wraps(_f)                    # for the function name
    #         def wrapper_repeat(*args, **kwargs):    # for the function args
    #             value = None
    #             for _ in range(n):                  # functionality of do_repeat
    #                 value = _f(*args, **kwargs)     # call of original function
    #             return value                        # return value
    #         return wrapper_repeat                   # case 1: function only
    #     return partial(do_repeat, n=n)              # case 2: do_repeat with parameters

    @do_repeat(n=3)
    def p():
        print(" a| -> in 'p'")
        return 1
    print(" 1| repeat 'p' 3 times", end='')
    r1 = p()
    print(f" -> {r1=}")

    @do_repeat
    def q():
        print(" b| -> in 'q'")
        return 2
    print(" 2| repeat 'q' 2 times", end='')
    r2 = q()
    print(f" -> {r2=}")


if __name__ == "__main__":
    do_twice_or_more()
    do_repeat_with_params()
    do_repeat_flexible_style()
    do_repeat_partially()
    show_complete()
