# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates key functools utilities beyond wraps and partial.

Teaching focus
  - @lru_cache and @cache for memoization
  - @singledispatch for type-based function overloading
  - cache_info() and cache_clear() for introspection

functools
  - These decorators are among the most commonly used in production Python.
  - @lru_cache: Least Recently Used cache with optional maxsize.
  - @cache: Unbounded cache (shorthand for @lru_cache(maxsize=None), since 3.9).
  - @singledispatch: Dispatch to different implementations based on the type
    of the first argument — Python's answer to function overloading.

See also
  https://docs.python.org/3/library/functools.html
  https://peps.python.org/pep-0443/
"""

import functools
import time

from utils import print_function_header


"""
Topic: Memoization with @lru_cache and @cache
"""


@print_function_header
def memoization_basics():
    """ lru_cache turns expensive functions into cached ones """

    # without cache: exponential time
    def fib_slow(n):
        if n < 2:
            return n
        return fib_slow(n - 1) + fib_slow(n - 2)

    # with cache: linear time (each value computed once)
    @functools.lru_cache(maxsize=128)
    def fib_cached(n):
        if n < 2:
            return n
        return fib_cached(n - 1) + fib_cached(n - 2)

    start = time.perf_counter()
    result_slow = fib_slow(30)
    dt_slow = time.perf_counter() - start

    start = time.perf_counter()
    result_cached = fib_cached(30)
    dt_cached = time.perf_counter() - start

    print(f" 1| fib(30) = {result_slow}, slow: {dt_slow:.4f}s")
    print(f" 2| fib(30) = {result_cached}, cached: {dt_cached:.6f}s")

    # introspection: how's the cache doing?
    info = fib_cached.cache_info()
    print(f" 3| cache_info: {info}")
    #        hits=28, misses=31, maxsize=128, currsize=31

    fib_cached.cache_clear()                # reset the cache
    print(f" 4| after clear: {fib_cached.cache_info()}")


@print_function_header
def cache_unbounded():
    """ @cache (Python 3.9+) is lru_cache without a size limit """

    @functools.cache                        # same as @lru_cache(maxsize=None)
    def factorial(n):
        return n * factorial(n - 1) if n else 1

    print(f" 1| 10! = {factorial(10)}")
    print(f" 2| 5!  = {factorial(5)}")      # already cached from the 10! computation
    print(f" 3| cache_info: {factorial.cache_info()}")

    # important: cached functions must receive hashable arguments
    # @cache on a function taking a list → TypeError: unhashable type: 'list'


"""
Topic: Type-based dispatch with @singledispatch
"""


@print_function_header
def using_singledispatch():
    """ dispatch to different implementations based on argument type """

    @functools.singledispatch
    def format_value(value):
        """Default handler for unknown types."""
        return f"<{type(value).__name__}: {value}>"

    @format_value.register(int)
    def _(value):
        return f"integer: {value:,}"        # thousand separators

    @format_value.register(float)
    def _(value):
        return f"float: {value:.4f}"

    @format_value.register(str)
    def _(value):
        return f"string: '{value}' (len={len(value)})"

    @format_value.register(list)
    def _(value):
        return f"list with {len(value)} elements: {value}"

    # dispatch happens on the type of the first argument
    print(f" 1| {format_value(42)}")
    print(f" 2| {format_value(3.14159)}")
    print(f" 3| {format_value('hello')}")
    print(f" 4| {format_value([1, 2, 3])}")
    print(f" 5| {format_value((1, 2))}")    # no tuple handler → default

    # check which implementation is registered for a type
    print(f" 6| dispatch(int): {format_value.dispatch(int).__name__}")
    print(f" 7| registry: {list(format_value.registry.keys())}")


@print_function_header
def singledispatch_with_type_hints():
    """ since Python 3.7: register via type annotations """

    @functools.singledispatch
    def process(data):
        raise NotImplementedError(f"No handler for {type(data)}")

    @process.register
    def _(data: int) -> str:                # type annotation determines dispatch
        return f"processing int: {data * 2}"

    @process.register
    def _(data: str) -> str:
        return f"processing str: {data.upper()}"

    @process.register
    def _(data: dict) -> str:
        return f"processing dict with keys: {list(data.keys())}"

    print(f" 1| {process(21)}")
    print(f" 2| {process('hello')}")
    print(f" 3| {process({'a': 1, 'b': 2})}")

    try:
        process(3.14)
    except NotImplementedError as e:
        print(f" 4| expected error: {e}")


if __name__ == "__main__":
    memoization_basics()
    cache_unbounded()
    using_singledispatch()
    singledispatch_with_type_hints()
