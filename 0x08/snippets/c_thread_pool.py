# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about thread pooling.

Teaching focus
  - start and join multiple threads
  - use thread pools
  - where exceptions surface in a pool (see 'threads_with_exceptions')

ThreadPoolExecutor
From https://realpython.com/intro-to-python-threading/
  - Using a ThreadPoolExecutor can cause some confusing errors. For example,
    if you call a function that takes no parameters, but you pass it parameters
    in .map(), the thread will throw an exception. Unfortunately, ThreadPoolExecutor
    will hide that exception, and (in the case above) the program terminates
    with no output. This can be quite confusing to debug at first.
    See 'threads_with_exceptions' below for a live demo of where exceptions
    surface (submit/.result(), as_completed, map) and how map silently
    swallows them when the iterator is never consumed.

See also
  - https://superfastpython.com/threadpoolexecutor-map-vs-submit/
  - https://superfastpython.com/threadpoolexecutor-map/
  - https://superfastpython.com/threadpool-python/#Common_Objections_to_Using_ThreadPool

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import concurrent.futures
import threading
import time

from thread_helper import thread_info, timing_reset, tprint

from utils import print_function_header


def general_worker(budget:float):
    tprint(f" a|  - start of {threading.current_thread().name!r}, work for {budget=}s")
    time.sleep(budget)
    tprint(f" b|  - end of {thread_info(threading.current_thread())}")


@timing_reset
@print_function_header
def start_multiple_threads():
    """ start multiple threads """

    n = 3
    threads = list()

    tprint(" 1| create new threads")
    for no in range(1, n+1):
        thread = threading.Thread(target=general_worker, args=(no/10.0,))
        threads.append(thread)
        thread.start()

    tprint(" 2| wait for threads")
    for thread in threads:
        thread.join()

    tprint(" 3| joined - done here")


@timing_reset
@print_function_header
def start_multiple_threads_from_pool():
    """ start multiple threads from a thread pool """

    num_threads = 3

    # play with it; if it is smaller than the number of threads, they queue up
    max_workers = 4                         

    tprint(" 1| create new threads")
    
    # context manager (calls shutdown(wait=True) at the end)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # schedules one task immediately, non-blocking, returns a Future
        executor.submit(general_worker, 0.5)
        
        # schedules n tasks, one per value, also non-blocking in submission;
        # map returns a lazy iterator, i.e. if you don't consume it, the tasks are submitted but results are discarded
        executor.map(general_worker, (n/10.0 for n in range(1, num_threads+1)))
        tprint(" 2| all started")

    tprint(" 3| joined - done here")


@timing_reset
@print_function_header
def threads_with_results():
    """ start multiple threads and get a result """

    def sum_up(n):
        time.sleep(n/10.0)
        return n

    tprint(" 1| create new threads")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future1 = executor.submit(sum_up, 2)
        future2 = executor.submit(sum_up, 3)
        tprint(f" 2| threads started {future1=}, {future2=}")

        res1 = future1.result()             # this may block
        res2 = future2.result()
        tprint(f" 3| results available: {res1=}, {res2=}")

    tprint(" 4| joined - done here")


@timing_reset
@print_function_header
def threads_with_exceptions():
    """ show where exceptions surface for submit vs. map """

    def flaky_worker(budget):
        tprint(f" a|  - start of {threading.current_thread().name!r}, work for {budget=}s")
        if budget > 0.2:
            raise ValueError(f"budget {budget} too high")
        time.sleep(budget)
        return budget

    max_workers = 5

    tprint(" 1| submit")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # exception is parked in the future, re-raised on .result()
        future = executor.submit(flaky_worker, 0.5)
        try:
            res = future.result()           # the ValueError surfaces here
            tprint(f" 2| result: {res}")
        except ValueError as e:
            tprint(f" 2| caught: {e}")
    print()

    tprint(" 3| as_completed")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # handle each task as it finishes, errors and all
        futures = [executor.submit(flaky_worker, n/10.0) for n in range(1, 5)]
        for future in concurrent.futures.as_completed(futures):
            try:
                tprint(f" 4| result: {future.result()}")
            except ValueError as e:
                tprint(f" 4| caught: {e}")
    print()
    
    tprint(" 5| map")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # exception surfaces only while consuming the iterator
        results = executor.map(flaky_worker, (n/10.0 for n in range(1, 5)))
        try:
            # map stops at the _first_ exception (in submit order), so we never reach the rest
            for res in results:             # the ValueError surfaces here
                tprint(f" 6| result: {res}")
        except ValueError as e:
            tprint(f" 6| caught: {e}")
    print()

    tprint(" 7| lost")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # if you never consume the map iterator, the exception is silently lost
        executor.map(flaky_worker, (n/10.0 for n in range(1, 5)))
        tprint(" 8| submitted, iterator ignored - no error shown")

    tprint(" 9| done here")


if __name__ == "__main__":
    start_multiple_threads()
    start_multiple_threads_from_pool()
    threads_with_results()
    threads_with_exceptions()
