# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about race conditions, the GIL, deadlocks and livelocks.

Teaching focus
  - race conditions
  - deadlocks and livelocks
  - GIL

Note: The problems discussed here are not specific to Python, and the
solution can only be a matter of thought :-)

Lock, RLock
For background see
    https://docs.python.org/3/library/threading.html#lock-objects
We skip RLock here.

GIL
see https://docs.python.org/3/glossary.html#term-global-interpreter-lock
  - This is not only Python-specific, but even dependent on the concrete
    Python implementation, namely CPython.
  - The mechanism used by the CPython interpreter to assure that only one
    thread executes Python bytecode at a time. This simplifies the CPython
    implementation by making the object model (including critical built-in
    types such as dict) implicitly safe against concurrent access. Locking
    the entire interpreter makes it easier for the interpreter to be
    multi-threaded, at the expense of much of the parallelism afforded by
    multi-processor machines.
  - You can even customise these time frames when threads change, but it
    is better to avoid this and use the defaults. See here
        sys.setswitchinterval(0.0005)

clean up or call something
  - The crucial point here is the small, inconsequential change in the code
    that suddenly causes a bug to appear in a function that is supposed to
    be working...

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import threading

from utils import (
    print_function_header,
    print_gil_info,
    reset_timing,
    tprint,
)

# @print_function_header
# def determine_gil_info():
#     """ determine GIL info """
#
#     gil_removed, gil_active = gil_info()
#     print(f" 1| GIL removed: {gil_removed}, active: {gil_active}")


@reset_timing
@print_function_header
def sum_benchmark(loops: int):
    """ sum benchmark """

    total_sum = 0

    def worker(n_, inc_):
        nonlocal total_sum
        for _ in range(n_):
            total_sum += inc_

    tprint(f" 1| start benchmark, {loops=}")
    worker(loops, +1)
    tprint(f" 2| done, {total_sum=}")


@reset_timing
@print_function_header
def race_conditions(loops: int):
    """ understand race conditions """

    total_sum = 0

    def worker(n_, inc_):
        nonlocal total_sum
        for _ in range(n_):
            total_sum += inc_
            # print("", end='')             # or a call

    tprint(f" 1| start threads, {loops=}")

    t1 = threading.Thread(target=worker, args=(loops, +1))
    t2 = threading.Thread(target=worker, args=(loops, -1))
    t1.start()
    t2.start()

    tprint(" 2| wait for threads")
    t1.join()
    t2.join()

    tprint(f" 3| done, {total_sum=}")


lock = threading.Lock()                     # Lock, RLock

@reset_timing
@print_function_header
def critical_regions(loops: int):
    """ define critical regions """

    total_sum = 0

    def worker(n_, inc_):
        nonlocal total_sum
        # with lock - why is here not a good place?
        for _ in range(n_):
            with lock:                      # use contextmanager
                total_sum += inc_
                print("", end="")

            # lock.acquire()                # do not do this, why?
            # current = ...
            # lock.release()

    tprint(f" 1| start threads, {loops=}")

    t1 = threading.Thread(target=worker, args=(loops, +1))
    t2 = threading.Thread(target=worker, args=(loops, -1))
    t1.start()
    t2.start()

    tprint(" 2| wait for threads")

    t1.join()
    t2.join()
    tprint(f" 3| done, {total_sum=}")


if __name__ == "__main__":
    n = 1000                                # =1000 is ok
    sum_benchmark(loops=n)
    race_conditions(loops=n)
    critical_regions(loops=n)

    print_gil_info()
