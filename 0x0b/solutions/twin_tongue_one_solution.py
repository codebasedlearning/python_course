# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Twin Tongue' """

from typing import Callable
import math
import time
import concurrent.futures
import functools
from dataclasses import dataclass


@dataclass
class TestConfig:
    a: float
    b: float
    exact: float
    f: Callable


def trapezoidal_rule(a: float, b: float, f: Callable, n: int):
    h = (b-a)/n
    return h*(0.5*(f(a)+f(b))+sum((f(a+i*h) for i in range(1, n))))


def measure_serial(config: TestConfig, m: int, repeat: int):
    print(f" 2| start serial calc.")
    area = 0
    t0 = time.process_time()
    for _ in range(repeat):
        area = trapezoidal_rule(config.a, config.b, config.f, m)
    dt = time.process_time()-t0
    err = math.fabs(area - config.exact)
    print(f" 3| done, {dt=}, {area=}, {err=}\n")


def measure_parallel(config: TestConfig, m: int, repeat: int, workers: int):
    print(f" 4| start parallel calc.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        a, b, f = config.a, config.b, config.f
        n = m//workers
        dx = (b-a)/workers
        t0 = time.process_time()
        for _ in range(repeat):
            results = [executor.submit(trapezoidal_rule, a=a+k*dx, b=a+(k+1)*dx, f=f, n=n) for k in range(workers)]
            area = functools.reduce(lambda x, w: x+w.result(), results, 0)  # assuming all tasks need nearly same time
        dt = time.process_time() - t0
        err = math.fabs(area - config.exact)
        print(f" 5| done, {dt=}, {area=}, {err=}")


def solve():
    test_config = TestConfig(a=0.0, b=2.0, exact=728 / (9 * math.log(3)),
                             f=lambda x: math.pow(3, 3 * x - 1))
    print(f" 1| approx {test_config.exact}\n")
    m = 40000
    rep = 100
    worker = 4
    measure_serial(test_config, m, rep)
    measure_parallel(test_config, m, rep, worker)


if __name__ == "__main__":
    solve()

"""
Trapezregel
  - https://de.wikipedia.org/wiki/Trapezregel
  - https://de.wikipedia.org/wiki/Numerische_Integration
"""
