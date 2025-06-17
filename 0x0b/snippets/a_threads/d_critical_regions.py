# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about race conditions, the GIL, deadlocks and livelocks.

Teaching focus
  - race conditions
  - deadlocks and livelocks
  - GIL

Note: The problems discussed here are not specific to Python, and the
solution can only be a matter of thought :-)

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import threading
from thread_helper import dt, gil_info

def determine_gil_info():
    """ determine GIL info """
    print("\ndetermine_gil_info\n==================")

    gil_removed, gil_active = gil_info()
    print(f" 1| GIL removed: {gil_removed}, active: {gil_active}")


def sum_benchmark(n: int):
    """ sum benchmark """
    print("\nsum_benchmark\n=============")

    dt(reset=True)
    total_sum = 0

    def worker(n_, inc_):
        nonlocal total_sum
        for i in range(n_):
            current = total_sum
            current = current + inc_
            #if hasattr(worker, 'logger'): ... # or a call, or a print
            total_sum = current

    print(f"{dt()}  1| start benchmark, {n=}")
    worker(n, +1)
    print(f"{dt()}  2| done, {total_sum=}")


def race_conditions(n: int):
    """ understand race conditions """
    print("\nrace_conditions\n===============")

    dt(reset=True)
    total_sum = 0

    def worker(n_, inc_):
        nonlocal total_sum
        for i in range(n_):
            current = total_sum
            current = current + inc_
            # if hasattr(worker, 'logger'): ... # or a call, or a print
            total_sum = current

    print(f"{dt()}  1| start threads, {n=}")

    t1 = threading.Thread(target=worker, args=(n, +1))     # test with +2
    t2 = threading.Thread(target=worker, args=(n, -1))
    t1.start()
    t2.start()

    print(f"{dt()}  2| wait for threads")
    t1.join()
    t2.join()

    print(f"{dt()}  3| done, {total_sum=}")

lock = threading.Lock()                     # Lock, RLock

def critical_regions(n: int):
    """ define critical regions """
    print("\ncritical_regions\n================")

    dt(reset=True)
    total_sum = 0

    def worker(n_, inc_):
        nonlocal total_sum
        # with lock                                                 # why is this not a good place?
        for i in range(n_):
            with lock:                                              # use contextmanager! (see below)
                current = total_sum
                current = current + inc_
                # if hasattr(worker, 'logger'): ...
                total_sum = current
            # lock.acquire()                                        # do not do this, why?
            # current = ...
            # lock.release()

    print(f"{dt()}  1| start threads, {n=}")

    t1 = threading.Thread(target=worker, args=(n, +1))
    t2 = threading.Thread(target=worker, args=(n, -1))
    t1.start()
    t2.start()

    print(f"{dt()}  2| wait for threads")

    t1.join()
    t2.join()
    print(f"{dt()}  3| done, {total_sum=}")


if __name__ == "__main__":
    determine_gil_info()
    n = 10000000
    sum_benchmark(n=n)
    race_conditions(n=n)             # n=10000 is ok
    critical_regions(n=n)

"""
Lock, RLock
For background see 
    https://docs.python.org/3/library/threading.html#lock-objects
We skip RLock here.

GIL
see https://docs.python.org/3/glossary.html#term-global-interpreter-lock
  - This is not only Python-specific, but even dependent on the concrete 
    Python implementation, namely Cpython.
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
"""
