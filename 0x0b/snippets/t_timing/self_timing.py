# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
In this snippet is about timer and timing.

Teaching focus
  - different timers
"""

import time
import timeit

"""
From Wikipedia https://en.wikipedia.org/wiki/Elapsed_real_time
  - Elapsed real time, real time, wall-clock time, wall time, or walltime is 
    the actual time taken from the start of a computer program to the end. 
    In other words, it is the difference between the time at which a task 
    finishes and the time at which the task started.
  - Wall time is thus different from CPU time, which measures only the time 
    during which the processor is actively working on a certain task  
  - The difference between the two can arise from architecture and run-time 
    dependent factors, e.g. programmed delays or waiting for system resources 
    to become available. 

Note: Often time functions call platform-specific library functions, i.e. 
these functions are platform-dependent under the hood.

Also note:
  - `time.process_time()` measures the total aggregated CPU time for 
    all threads in the program.
    This can make the value seem inflated if compared to wall-clock time 
    for multi-threaded tasks.

  - To measure CPU time on a per-thread basis, consider external libraries 
    like `psutil`.
"""

# we need a non-trivial task -> recursive fib(n)
benchmark_n = 35


def fib(n):
    return fib(n-1)+fib(n-2) if n >= 3 else 1 if n >= 1 else 0


def beware_of_small_deltas():
    """ beware of small time deltas """
    print("\nbeware_of_small_deltas\n======================")

    print(f" 1| try to use time... but", end='')
    t0 = time.time()                        # seconds since a given point in time (epoch)
    t1 = t0 + 1e-9
    print(f" {t0=}, {t1=} => dt={t1-t0=}") # same -> small times are a problem


def use_perf_counter():
    """ use perf_counter (wall-clock time) """
    print("\nuse_perf_counter\n================")

    t0 = time.perf_counter()                # fractional seconds
    fib_n = fib(benchmark_n)                # include time elapsed during sleep, system-wide
    t1 = time.perf_counter()
    print(f" 1| perf_counter:    fib({benchmark_n})={fib_n} in {t1 - t0:0.4f} seconds | {t0=}, {t1=}")

    t0_ns = time.perf_counter_ns()
    fib_n_ns = fib(benchmark_n)
    t1_ns = time.perf_counter_ns()
    print(f" 2| perf_counter_ns: fib({benchmark_n})={fib_n_ns} in {(t1_ns - t0_ns)/1e9:0.4f} seconds | t0={t0_ns}, t1={t1_ns}")


def use_process_time():
    """ use process_time (process time) """
    print("\nuse_process_time\n================")

    t0 = time.process_time()                # fractional seconds
    fib_n = fib(benchmark_n)                # does not incl. sleep-time, process-wide
    t1 = time.process_time()
    print(f" 1| process_time:   fib({benchmark_n})={fib_n} in {t1 - t0:0.4f} seconds | {t0=}, {t1=}")

    t0_ns = time.process_time_ns()
    fib_n_ns = fib(benchmark_n)
    t1_ns = time.process_time_ns()
    print(f" 2| process_time_ns: fib({benchmark_n})={fib_n_ns} in {(t1_ns - t0_ns)/1e9:0.4f} seconds | t0={t0_ns}, t1={t1_ns}")

def compare_timer():
    """ compare timer """
    print("\ncompare_timer\n=============")

    t0 = time.perf_counter()
    fib_n = fib(benchmark_n)
    time.sleep(1)
    t1 = time.perf_counter()
    print(f" 1| perf_counter:   fib({benchmark_n}), sleep 1s in {t1 - t0:0.4f} seconds | {t0=}, {t1=}")

    t0 = time.process_time()
    fib_n = fib(benchmark_n)
    time.sleep(1)
    t1 = time.process_time()
    print(f" 2| process_time:   fib({benchmark_n}), sleep 1s in {t1 - t0:0.4f} seconds | {t0=}, {t1=}")


def use_timeit():
    """ use timeit (process time); 'timeit' can also be used from the command line """
    print("\nuse_timeit\n==========")

    dt = timeit.timeit(lambda: fib(benchmark_n), number=1)  # the default timer is time.perf_counter
    print(f" 1| timeit: {dt=:.4f} seconds")


if __name__ == "__main__":
    beware_of_small_deltas()
    use_perf_counter()
    use_process_time()
    compare_timer()
    use_timeit()


"""
More sources:
    https://docs.python.org/3/library/time.html
    https://docs.python.org/3/library/timeit.html
    https://realpython.com/python-timer/
    https://www.pythoncentral.io/measure-time-in-python-time-time-vs-time-clock/
and
    https://de.wikipedia.org/wiki/Fibonacci-Folge
"""
