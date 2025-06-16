# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about a producer-consumer pattern with two threads and locks.

Teaching focus
  - producer-consumer pattern

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import concurrent.futures
import threading
import random
from thread_helper import dt, name_translation


class MessageSlot:
    neutral_message = 0
    poison_pill = -1

    def __init__(self):
        self.message_slot = MessageSlot.neutral_message
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()        # blocks any consumer
        print(f"{dt()}  a|   - init, {self._status()}")

    @property
    def message(self):
        self.consumer_lock.acquire()        # wait for message; read exclusively
        message = self.message_slot
        self.producer_lock.release()        # allow producer writing
        print(f"{dt()}  b|   - red slot from {name_translation(threading.current_thread().name)}, {self._status()}")
        return message

    @message.setter
    def message(self, message):
        self.producer_lock.acquire()        # wait for free slot (or signal)
        self.message_slot = message
        self.consumer_lock.release()        # allow consumer reading
        print(f"{dt()}  c|   - wrote slot from {name_translation(threading.current_thread().name)}, {self._status()}")

    def _status(self):
        slot = f"{self.message_slot}" if self.message_slot > 0 else "-"
        cons = "Locked" if self.consumer_lock.locked() else "Free"
        prod = "Locked" if self.producer_lock.locked() else "Free"
        return f"slot:{slot}, producer:{prod}, consumer:{cons}"


def producer(pipeline):
    for _ in range(3):
        message = random.randint(1, 10)     # our 'message'
        print(f"{dt()}  2|   write message: {message}")
        pipeline.message = message

    print(f"{dt()}  3|   write poison pill")
    pipeline.message = MessageSlot.poison_pill
    print(f"{dt()}  4|   producer done")


def consumer(pipeline):
    message = MessageSlot.neutral_message
    while message != MessageSlot.poison_pill:
        message = pipeline.message
        print(f"{dt()}  5|   got message: {message}")
    print(f"{dt()}  6|   consumer done")


def run_messages():
    pipeline = MessageSlot()
    print(f"{dt()}  1|   start threads")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)

    print(f"{dt()}  7| main done")


if __name__ == "__main__":
    run_messages()

"""
The objects used here are discussed here:
    https://docs.python.org/3/library/threading.html

But we will leave that out:
    Semaphore, Timer, Barrier
"""
