# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about deadlocks and livelocks.

Teaching focus
  - deadlocks and livelocks

deadlocks
  - The basic problem here is that threads have already acquired some
    resources and are waiting for others, which in turn are being blocked
    by other threads.
  - See
    https://superfastpython.com/threading-in-python/

livelocks
  - In this situation, no thread is blocking, but by continually blocking
    one resource and asking for the second, no thread is making any progress.

So it is not about deadlocks, but about a situation where the system
is in a state of infinite waiting.

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import threading

from utils import (
    print_function_header,
    print_gil_info,
    reset_timing,
    sign_in,
    tprint,
)


@reset_timing
@print_function_header
def discuss_deadlocks():
    """ discuss deadlocks """

    def worker(first_lock,second_lock):
        tprint(" a| - thread starting, try to get first lock")
        with first_lock:
            sign_in(budget=0.1)
            tprint(f" b| - got first lock {id(first_lock)}, try to get second lock {id(second_lock)}")
            with second_lock:
                # never happen...
                print(f" c| !!!!! got second lock {id(second_lock)}, do work ...")

    tprint(" 1| create locks, start threads")
    lock1 = threading.Lock()
    lock2 = threading.Lock()

    t1 = threading.Thread(target=worker, args=(lock1,lock2))
    t2 = threading.Thread(target=worker, args=(lock2,lock1))
    t1.start()
    t2.start()

    tprint(" 2| wait for threads...")
    t1.join()
    t2.join()

    tprint(" 3| done")


@reset_timing
@print_function_header
def discuss_livelocks():
    """ discuss livelocks """

    def worker(first_lock,second_lock):
        tprint(" a| - thread starting, get locks")
        while True:
            tprint(f" b| - lock status: {first_lock.locked()},{second_lock.locked()}")
            with first_lock:
                sign_in(budget=1)
                tprint(f" c| - got lock {id(first_lock)}, try to get lock {id(second_lock)}")
                if second_lock.locked():
                    tprint(f" d| - lock {id(second_lock)} not avail., try again later")
                else:
                    with second_lock:
                        tprint(f" e| !!!!! got lock {id(second_lock)}, do work")

    tprint(" 1| create locks, start threads")
    lock1 = threading.Lock()
    lock2 = threading.Lock()

    t1 = threading.Thread(target=worker, args=(lock1,lock2))
    t2 = threading.Thread(target=worker, args=(lock2,lock1))
    t1.start()
    t2.start()

    tprint(" 2| wait for threads...")
    t1.join()
    t2.join()

    tprint(" 3| done")


if __name__ == "__main__":
    ...
    # discuss_deadlocks()
    # discuss_livelocks()
    print_gil_info()
