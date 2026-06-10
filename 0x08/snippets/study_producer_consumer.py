# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about the producer-consumer problem, solved three ways.

Teaching focus
  - the same producer/consumer (checking primes) driven by three channels:
    1) a paired-Lock turnstile - strictly 1:1, capacity 1
    2) a hand-rolled Condition queue - bounded buffer, supports N:M
    3) queue.Queue - which is exactly (2) from the stdlib

Note: the producer/consumer functions are identical across all three runs -
only the channel object passed in changes. That interchangeability is the point.
"""

import concurrent.futures
import queue
import threading
from collections import deque

from utils import (
    print_function_header,
    print_gil_info,
    reset_timing,
    tprint,
)


def is_prime(n: int) -> bool:               # the task - check for prime
    """ check if n is prime """
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True


"""
producer, consumer, run_variant are identical across all three variants.
"""

POISON = object()                           # sentinel: end of stream

def producer(channel, numbers, num_consumers):
    """ check all numbers with num_consumers concurrent consumers """
    for n in numbers:                       # put all numbers into the channel for checking
        tprint(f" P| - put {n}")
        channel.put(n)
    for _ in range(num_consumers):          # one poison pill per consumer to end the stream
        channel.put(POISON)
    tprint(" P| - producer done")


def consumer(channel):
    """ check numbers from the channel until poison pill """
    while (item := channel.get()) is not POISON:
        tprint(f" C| - {item} is prime? {is_prime(item)}")
    tprint(" C| - consumer done")


def run_variant(channel, numbers, num_consumers):
    """ run the producer/consumer; channel is an instance with put/get protocol """
    max_workers = 1 + num_consumers         # one producer + N consumers
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.submit(producer, channel, numbers, num_consumers)
        for _ in range(num_consumers):
            executor.submit(consumer, channel)


class LockTurnstile:
    """ turnstile with two locks - one for producer, one for consumer """

    def __init__(self):
        self.slot = None
        self.producer_lock = threading.Lock()   # free, i.e., producer may write
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()            # held, i.e., consumer must wait

    def put(self, item):
        self.producer_lock.acquire()        # wait for a free slot
        self.slot = item
        self.consumer_lock.release()        # hand off to the consumer

    def get(self):
        self.consumer_lock.acquire()        # wait for an item
        item = self.slot
        self.producer_lock.release()        # free the slot for the producer
        return item

@reset_timing
@print_function_header
def use_paired_lock_turnstile(numbers):
    """ run the producer/consumer with a turnstile """
    run_variant(LockTurnstile(), numbers, num_consumers=1)


class ConditionQueue:
    """ a buffer guarded by one lock and two conditions (explicit queue.Queue) """

    def __init__(self, maxsize):
        self.items = deque()
        self.maxsize = maxsize
        self.mutex = threading.Lock()
        self.not_full = threading.Condition(self.mutex)     # producers wait here
        self.not_empty = threading.Condition(self.mutex)    # consumers wait here

    def put(self, item):
        with self.not_full:
            while len(self.items) >= self.maxsize:          # predicate guards the wait
                self.not_full.wait()
            self.items.append(item)
            self.not_empty.notify()                         # wake one consumer (not producers)

    def get(self):
        with self.not_empty:
            while not self.items:
                self.not_empty.wait()
            item = self.items.popleft()
            self.not_full.notify()                          # wake one producer (not consumers)
            return item


@reset_timing
@print_function_header
def use_condition_queue(numbers):
    """ run the producer/consumer with a condition queue """
    run_variant(ConditionQueue(maxsize=2), numbers, num_consumers=3)


@reset_timing
@print_function_header
def use_queue_queue(numbers):
    """ run the producer/consumer with stdlib queue.Queue """
    run_variant(queue.Queue(maxsize=2), numbers, num_consumers=3)


if __name__ == "__main__":
    maybe_primes = [7, 10, 13, 17, 20, 23]

    use_paired_lock_turnstile(maybe_primes)
    use_condition_queue(maybe_primes)
    use_queue_queue(maybe_primes)
    print_gil_info()
