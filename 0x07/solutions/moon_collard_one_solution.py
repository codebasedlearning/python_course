# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

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


@slow_down_v2(dt=0.5)                       # also works as: @slow_down_v2
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
    # def wrapper():
    #     func()
    # return wrapper
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

def test_timer():
    class Timer:
        def __new__(cls, *args, **kwargs):
            if args and callable(args[0]):
                self = super().__new__(cls)
                cls.__init__(self)  # default label=None
                return self(args[0])
            return super().__new__(cls)

        def __init__(self, label=None):
            self.label = label

        def __call__(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start
                name = self.label or func.__name__
                print(f"{name} took {duration:.4f} seconds")
                return result
            return wrapper

    @Timer
    def quick():
        time.sleep(0.3)
    @Timer(label="slow!")
    def slow():
        time.sleep(0.5)

    print(" 1| quick() start")
    quick()
    print(" 2| stop")
    print(" 3| slow() start")
    slow()
    print(" 4| stop")

def test_lru_cache():
    from collections import OrderedDict

    def my_lru_cache(maxsize=128):
        """A simple LRU cache decorator using OrderedDict.

        - Cache keys are derived from positional and keyword arguments.
        - When the cache exceeds `maxsize`, the least recently used entry
          is evicted (FIFO order in the OrderedDict, refreshed on hit).
        - The decorated function exposes `cache_info()` and `cache_clear()`.
        """
        def decorator(func):
            cache = OrderedDict()
            hits = 0
            misses = 0

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal hits, misses
                key = (args, tuple(sorted(kwargs.items())))

                if key in cache:
                    hits += 1
                    cache.move_to_end(key)          # mark as recently used
                    return cache[key]

                misses += 1
                result = func(*args, **kwargs)
                cache[key] = result

                if len(cache) > maxsize:
                    cache.popitem(last=False)        # evict least recently used

                return result

            def cache_info():
                return f"hits={hits}, misses={misses}, size={len(cache)}, maxsize={maxsize}"

            def cache_clear():
                nonlocal hits, misses
                cache.clear()
                hits = misses = 0

            wrapper.cache_info = cache_info
            wrapper.cache_clear = cache_clear
            return wrapper
        return decorator

    @my_lru_cache(maxsize=4)
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    print(f"05| fib(10) = {fib(10)}")
    print(f"06| cache_info: {fib.cache_info()}")

    # verify correctness against known values
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    for i, want in enumerate(expected):
        assert fib(i) == want, f"fib({i}) should be {want}"
    print(f"07| fib(0..10) correct")
    print(f"08| cache_info after re-calls: {fib.cache_info()}")

    # demonstrate eviction: only 4 entries survive
    fib.cache_clear()
    for i in range(8):
        fib(i)
    print(f"09| after fib(0..7) with maxsize=4: {fib.cache_info()}")


def main():
    #test_debug()
    #test_slow_down()
    test_example_test_cases()
    #test_timer()
    test_lru_cache()

if __name__ == "__main__":
    main()

"""
For print: https://realpython.com/python-print/
"""
