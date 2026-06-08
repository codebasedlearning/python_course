# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Diamond Bay' """

import functools


def use_lru_cache():
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

            wrapper.cache_info = cache_info     # ty:ignore[unresolved-attribute]
            wrapper.cache_clear = cache_clear   # ty:ignore[unresolved-attribute]
            return wrapper
        return decorator

    @my_lru_cache(maxsize=4)
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    print(f" 1| fib(10) = {fib(10)}")
    print(f" 2| cache_info: {fib.cache_info()}")

    # verify correctness against known values
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    for i, want in enumerate(expected):
        assert fib(i) == want, f"fib({i}) should be {want}"
    print(f" 3| fib(0..10) correct")
    print(f" 4| cache_info after re-calls: {fib.cache_info()}")

    # demonstrate eviction: only 4 entries survive
    fib.cache_clear()
    for i in range(8):
        fib(i)
    print(f" 5| after fib(0..7) with maxsize=4: {fib.cache_info()}")


if __name__ == "__main__":
    use_lru_cache()
