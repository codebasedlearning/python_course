# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about condition variables and locks.

Teaching focus
  - condition variables

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import concurrent.futures
import threading
import time
from thread_helper import dt


def sender(signal):
    print(f"{dt()}  a|   - sender start")
    time.sleep(0.2)
    with signal:                            # acquires the lock
        print(f"{dt()}  b|   - with signal")
        signal.notify()                     # or notify_all()
    print(f"{dt()}  c|   - signal sent")


def receiver(signal):
    print(f"{dt()}  d|   - receiver start")
    time.sleep(0.1)
    with signal:                            # where is the problem?
        print(f"{dt()}  e|   - with signal")
        signal.wait()                       # frees lock (we skip the traditional while loop here)
    print(f"{dt()}  f|   - signal received")


def run_messages():
    print(f"{dt()}  1| start")

    signal = threading.Condition()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(sender, signal)
        executor.submit(receiver, signal)

    print(f"{dt()}  2| main done")


if __name__ == "__main__":
    run_messages()

"""
The objects used here are discussed here:
    https://docs.python.org/3/library/threading.html

But we will leave that out:
    Semaphore, Timer, Barrier
"""
