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

---

decision guide: threads vs processes vs async

    IO-bound (network, disk, database):
      - threading or asyncio
        threads: simpler, good for blocking IO
        asyncio: better for many concurrent connections

    CPU-bound (math, image processing, parsing):
      - multiprocessing or ProcessPoolExecutor
        bypasses the GIL, uses all CPU cores

    mixed workloads:
      - combine: async for IO + ProcessPoolExecutor for CPU
        asyncio.to_thread() bridges sync IO into async code

---

Note for processes:

    Futures also work, i.e. same interface for thread and process pools.

    Everything must pickle (being serializable). The function, its args, and
    the return value are serialized and shipped to the child.
    So lambdas, local/nested functions, and closures fail to submit — the function
    must be top-level/importable.

    Exceptions cross the boundary by pickling too. A raised exception is pickled
    in the child and re-raised in the parent at future.result() — so the mechanic
    looks identical, but if the exception object itself isn't picklable (rare),
    you get a confusing serialization error instead of your real exception.

    A dead worker poisons the pool. If a child process is killed (segfault in
    a C extension, ...), the pool raises BrokenProcessPool and every pending
    future fails. Threads can't do this — a thread can't take down its siblings
    the way a crashing process can.
"""

import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from utils import print_function_header, print_gil_info, process_info, ptprint, reset_timing


def busy_worker(budget):
    """A CPU-bound worker function (runs in a child process)."""
    ptprint(f" a| - start, working for {budget}s, current process info: {process_info(multiprocessing.current_process())}")

    # simulate CPU work (not sleep — actual computation)
    total = 0
    end = time.perf_counter() + budget
    while time.perf_counter() < end:
        total += 1

    ptprint(f" b| - done ({total:,} iterations)")
    return total


@reset_timing
@print_function_header
def basic_process():
    """ spawn separate processes """

    ptprint(f" 1| current process: {process_info(multiprocessing.current_process())}")

    p1 = multiprocessing.Process(name="ALICE", target=busy_worker, args=(0.3,))
    p2 = multiprocessing.Process(name="BOB", target=busy_worker, args=(0.2,))

    start = time.perf_counter()
    p1.start()
    p2.start()

    p1.join()                               # wait for completion
    p2.join()
    elapsed = time.perf_counter() - start

    ptprint(f" 2| both done in {elapsed:.2f}s (< 0.5s = truly parallel)")


@print_function_header
def executor_comparison():
    """ threads vs processes for CPU-bound work """

    #  multiprocessing.Pool is the older, lower-level pool.
    #  ProcessPoolExecutor is built on top of multiprocessing

    num_workers = 8
    max_workers = 4
    tasks = [0.1]*num_workers               # identical CPU tasks
    ptprint(f" 1| {num_workers} CPU-bound tasks, {max_workers} max., {multiprocessing.cpu_count()} CPUs")

    # ThreadPoolExecutor: maybe 'limited' by GIL for CPU work
    ptprint( " 2| start threads from ThreadPoolExecutor")
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(busy_worker, tasks)

    thread_time = time.perf_counter() - start
    ptprint(f" 3| done:  {thread_time:.3f}s\n")

    # ProcessPoolExecutor: true parallelism but with overhead
    ptprint( " 4| start processes from ProcessPoolExecutor")
    start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(busy_worker, tasks)

    process_time = time.perf_counter() - start
    ptprint(f" 5| done: {process_time:.3f}s")


if __name__ == "__main__":
    basic_process()
    executor_comparison()
    print_gil_info()
