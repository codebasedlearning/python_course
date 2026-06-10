# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Marsh Wintercress'

Count primes in a range, parallelized with processes instead of threads.
  1) serial vs. ThreadPoolExecutor vs. ProcessPoolExecutor -> only processes
     actually speed up this CPU-bound work (the GIL serializes the threads).
  2) the pickle boundary: a lambda / nested function cannot be submitted to a
     process pool (it is not picklable); a module-level function can.

The same Future API (submit / result / map) works for threads AND processes -
only the worker must be importable (top-level), because it is pickled and sent
to a child process with its own memory.
"""

import concurrent.futures
import time


def is_prime(n: int) -> bool:               # top-level -> picklable -> ships to a child
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def count_in_range(n0: int, n1: int) -> int:
    return sum(1 for n in range(n0, n1) if is_prime(n))


def chunks(n0: int, n1: int, workers: int):
    step = (n1 - n0) // workers
    bounds = [n0 + k * step for k in range(workers)] + [n1]
    return list(zip(bounds, bounds[1:]))


def run_serial(n0: int, n1: int) -> int:
    t0 = time.perf_counter()
    total = count_in_range(n0, n1)
    print(f" .| {'serial':<20} -> {total}, {time.perf_counter() - t0:.3f}s")
    return total


def run_pool(title: str, executor_cls, n0: int, n1: int, workers: int):
    """ identical code for threads and processes - just a different executor class """
    t0 = time.perf_counter()
    with executor_cls(max_workers=workers) as executor:
        futures = [executor.submit(count_in_range, a, b) for a, b in chunks(n0, n1, workers)]
        total = sum(f.result() for f in futures)
    print(f" .| {title:<20} -> {total}, {time.perf_counter() - t0:.3f}s")
    return total


if __name__ == "__main__":
    n0, n1, workers = 2, 200_000, 8
    print(f" 1| primes in [{n0}, {n1}), {workers=}\n")

    print(" 2| CPU-bound: threads don't help, processes do:")
    run_serial(n0, n1)
    run_pool("ThreadPoolExecutor", concurrent.futures.ThreadPoolExecutor, n0, n1, workers)
    run_pool("ProcessPoolExecutor", concurrent.futures.ProcessPoolExecutor, n0, n1, workers)
