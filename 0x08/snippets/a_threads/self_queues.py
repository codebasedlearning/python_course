# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about a producer-consumer pattern, queues and events.

Teaching focus
  - producer-consumer pattern with queues
  - threading events

From https://docs.python.org/3/library/threading.html#threading.Event
  Event class implements event objects. An event manages a flag that can be
  set to true with the set() method and reset to false with the clear() method.
  The wait() method blocks until the flag is true. The flag is initially false.

The objects used here are discussed here:
    https://docs.python.org/3/library/threading.html

But we will leave that out:
    Semaphore, Timer, Barrier

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import concurrent.futures
import queue
import random
import threading
import time
from thread_helper import dt


def producer(queue, event):
    while not event.is_set():
        message = random.randint(1, 101)
        print(f"[main{dt()}] -a| got data, put {message=}")
        queue.put(message)                  # may block if full
    print(f"[main{dt()}] -b| producer, end")


def consumer(queue, event):
    while not event.is_set() or not queue.empty():                  # runs if active or remaining messages
        message = queue.get()               # may block
        print(f"[main{dt()}] -c| got {message=}, size:{queue.qsize()}")
    print(f"[main{dt()}] -d| consumer, end")


def main():
    print(f"[main{dt()}] 01| create pipeline, event and threads")
    pipeline = queue.Queue(maxsize=10)
    stop_event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, stop_event)
        executor.submit(consumer, pipeline, stop_event)

        time.sleep(0.0001)
        print(f"[main{dt()}] 02| set event")
        stop_event.set()
    print(f"[main{dt()}] 03| done")


if __name__ == "__main__":
    main()
