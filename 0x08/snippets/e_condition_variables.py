# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about condition variables and locks.

Teaching focus
  - condition variables
  - the lost-wakeup pitfall (notify before wait) and why it needs a predicate

We will leave that out:
    Semaphore, Timer, Barrier

See also
    https://docs.python.org/3/library/threading.html#condition-objects
    https://docs.python.org/3/library/threading.html

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import concurrent.futures
import threading

from thread_helper import load_image, sign_in, timing_reset, tprint

from utils import print_function_header


@timing_reset
@print_function_header
def combine_notify_and_wait_careless():
    """ combine notify and wait """

    tprint(" 1| start")

    # A condition variable allows one or more threads to wait until they
    # are notified by another thread. It uses a Lock internally.
    signal = threading.Condition()

    def sender():
        sign_in(budget=0.05)
        with signal:                        # acquire() and release() around the block
            tprint(" a| - signed in -> notify")
            signal.notify()

    def receiver():
        load_image(budget=0.05)             # increase a little - why missed and how to solve?
        with signal:
            got = signal.wait(timeout=0.1)  # returns False on timeout
            tprint(f" b| - {'received' if got else 'missed'}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(receiver)
        executor.submit(sender)

    tprint(" 2| done")


@timing_reset
@print_function_header
def combine_notify_and_wait_reliable():
    """ combine notify and wait correctly """

    tprint(" 1| start")

    signal = threading.Condition()
    ready = False                           # shared state the receiver checks

    def sender():
        nonlocal ready
        sign_in(budget=0.05)                # even if we fire 'first', no signal is lost
        with signal:
            ready = True                    # set the state ...
            tprint(" a| - signed in -> notify")
            signal.notify()

    def receiver():
        load_image(budget=0.05)             # modify to see predicate guard in action
        with signal:
            while not ready:                # while because of spurious makeups;
                signal.wait()               # if 'ready' is already set, we never wait -> order-independent
            tprint(" b| - received")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(receiver)
        executor.submit(sender)

    tprint(" 2| done")


if __name__ == "__main__":
    combine_notify_and_wait_careless()
    combine_notify_and_wait_reliable()
