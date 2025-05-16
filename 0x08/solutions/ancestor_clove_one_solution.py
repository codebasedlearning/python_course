# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Ancestor Clove' """

from contextlib import contextmanager
import time

benchmark_n = 35


def fib(n):
    return fib(n-1)+fib(n-2) if n >= 3 else 1 if n >= 1 else 0


def use_perf_counter():
    t0 = time.perf_counter()
    fib_n = fib(benchmark_n)
    t1 = time.perf_counter()
    print(f" 1| perf_counter: fib({benchmark_n})={fib_n} in {t1 - t0:0.4f} seconds | t0={t0}, t1={t1}")


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        self.end = 0.0
        return lambda: self.end - self.start

    def __exit__(self, *args):
        self.end = time.perf_counter()


def use_timer_class():
    with Timer() as dt:
        fib_n = fib(benchmark_n)
    print(f" 2| timer class: fib({benchmark_n})={fib_n} in {dt():0.4f} seconds")


@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield lambda: end - start
    finally:
        end = time.perf_counter()


def use_timer_fct():
    with timer() as dt:
        fib_n = fib(benchmark_n)
    print(f" 3| timer fct: fib({benchmark_n})={fib_n} in {dt():0.4f} seconds")


if __name__ == "__main__":
    use_perf_counter()
    use_timer_class()
    use_timer_fct()
