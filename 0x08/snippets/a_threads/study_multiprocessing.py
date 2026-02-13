# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates multiprocessing — true parallelism beyond the GIL.

Teaching focus
  - multiprocessing.Process for spawning processes
  - multiprocessing.Pool for parallel map
  - ProcessPoolExecutor vs ThreadPoolExecutor
  - when to use threads vs processes (IO-bound vs CPU-bound)

multiprocessing
  - Threads share memory but are limited by the GIL for CPU work.
  - Processes have separate memory and bypass the GIL entirely.
  - Trade-off: process creation is slower and data must be serialized
    (pickle!) to communicate between processes.
  - Rule of thumb: threads for IO-bound, processes for CPU-bound.

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.

See also
  https://docs.python.org/3/library/multiprocessing.html
  https://docs.python.org/3/library/concurrent.futures.html
"""

import os
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from utils import print_function_header


"""
Topic: Basic Process usage
"""


def worker(name, duration):
    """A CPU-bound worker function (runs in a child process)."""
    pid = os.getpid()
    print(f" a|  [{name}] started in process {pid}, working for {duration}s")
    # simulate CPU work (not sleep — actual computation)
    total = 0
    end = time.perf_counter() + duration
    while time.perf_counter() < end:
        total += 1
    print(f" b|  [{name}] done ({total:,} iterations)")
    return total


@print_function_header
def basic_process():
    """ spawn separate processes """

    print(f" 1| main process: {os.getpid()}")

    p1 = multiprocessing.Process(target=worker, args=("A", 0.3))
    p2 = multiprocessing.Process(target=worker, args=("B", 0.2))

    start = time.perf_counter()
    p1.start()
    p2.start()

    p1.join()                               # wait for completion
    p2.join()
    elapsed = time.perf_counter() - start

    print(f" 2| both done in {elapsed:.2f}s (< 0.5s = truly parallel)")


"""
Topic: Pool for parallel map
"""


def is_prime(n):
    """Check if n is prime (deliberately slow for demonstration)."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


@print_function_header
def pool_parallel_map():
    """ multiprocessing.Pool maps work across processes """

    numbers = list(range(100_000, 101_000))

    # serial
    start = time.perf_counter()
    serial_result = list(map(is_prime, numbers))
    serial_time = time.perf_counter() - start

    # parallel with Pool
    start = time.perf_counter()
    with multiprocessing.Pool() as pool:
        parallel_result = pool.map(is_prime, numbers)
    parallel_time = time.perf_counter() - start

    serial_count = sum(serial_result)
    parallel_count = sum(parallel_result)

    print(f" 1| found {serial_count} primes (serial:   {serial_time:.3f}s)")
    print(f" 2| found {parallel_count} primes (parallel: {parallel_time:.3f}s)")
    print(f" 3| speedup: {serial_time/parallel_time:.1f}x "
          f"(with {multiprocessing.cpu_count()} CPUs)")


"""
Topic: ProcessPoolExecutor vs ThreadPoolExecutor
"""


def cpu_work(n):
    """Simulate CPU-bound work."""
    total = sum(i * i for i in range(n))
    return total


@print_function_header
def executor_comparison():
    """ threads vs processes for CPU-bound work """

    tasks = [500_000] * 8                   # 8 identical CPU tasks
    print(f" 1| {len(tasks)} CPU-bound tasks, {multiprocessing.cpu_count()} CPUs")

    # ThreadPoolExecutor: limited by GIL for CPU work
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(cpu_work, tasks))
    thread_time = time.perf_counter() - start

    # ProcessPoolExecutor: true parallelism
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        list(ex.map(cpu_work, tasks))
    process_time = time.perf_counter() - start

    print(f" 2| ThreadPoolExecutor:  {thread_time:.3f}s (GIL limits parallelism)")
    print(f" 3| ProcessPoolExecutor: {process_time:.3f}s (true parallel)")
    print(f" 4| speedup: {thread_time/process_time:.1f}x")


"""
Topic: When to use what
"""


@print_function_header
def when_to_use_what():
    """ decision guide: threads vs processes vs async """

    print(f" 1| IO-bound (network, disk, database):")
    print(f"    → threading or asyncio")
    print(f"    → threads: simpler, good for blocking IO")
    print(f"    → asyncio: better for many concurrent connections")
    print()
    print(f" 2| CPU-bound (math, image processing, parsing):")
    print(f"    → multiprocessing or ProcessPoolExecutor")
    print(f"    → bypasses the GIL, uses all CPU cores")
    print()
    print(f" 3| mixed workloads:")
    print(f"    → combine: async for IO + ProcessPoolExecutor for CPU")
    print(f"    → asyncio.to_thread() bridges sync IO into async code")


if __name__ == "__main__":
    basic_process()
    pool_parallel_map()
    executor_comparison()
    when_to_use_what()
