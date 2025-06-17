# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about thread pooling.

Teaching focus
  - start and join multiple threads
  - use thread pools

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import threading
import time
import concurrent.futures
from thread_helper import dt, thread_info


def thread_function(secs):
    print(f"{dt()}  a|  - start of {threading.current_thread().name!r}, work for {secs=}s")
    print(f"{dt()}  b|  - thread info: {thread_info(threading.current_thread())}")
    time.sleep(secs)
    print(f"{dt()}  c|  - end of {threading.current_thread().name!r}")


def start_multiple_threads():
    """ start multiple threads """
    print("\nstart_multiple_threads\n======================")

    n = 3
    threads = list()

    print(f"{dt()}  1| create new threads")
    for i in range(1, n+1):
        t_i = threading.Thread(target=thread_function, args=(i,))
        threads.append(t_i)
        t_i.start()

    print(f"{dt()}  2| wait for threads")
    for t_i in threads:
        t_i.join()
    print(f"{dt()}  3| joined - done here")


def start_multiple_threads_from_pool():
    """ start multiple threads from a thread pool """
    print("\nstart_multiple_threads_from_pool\n================================")

    n = 3

    print(f"{dt()}  1| create new threads")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:  # context manager!
        executor.submit(thread_function, 1.5)
        executor.map(thread_function, range(1, n+1))                # maps range -> threads
        print(f"{dt()}  2| all started")

    print(f"{dt()}  3| joined - done here")


def threads_with_results():
    """ start multiple threads and get a result """
    print("\nthreads_with_results\n====================")

    def added(n):
        time.sleep(1)
        return n+1

    print(f"{dt()}  1| create new threads")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future1 = executor.submit(added, 23)
        future2 = executor.submit(added, 42)
        res1 = 1 #future1.result()  # this may block
        res2 = 2 #future2.result()
        print(f"{dt()}  2| threads started {future1=}, {future2=}")
        print(f"{dt()}  3| {res1} {res2}")
    print(f"{dt()}  4| joined - done here")


if __name__ == "__main__":
    #start_multiple_threads()
    #start_multiple_threads_from_pool()
    threads_with_results()

"""
ThreadPoolExecutor
From https://realpython.com/intro-to-python-threading/
  - Using a ThreadPoolExecutor can cause some confusing errors. For example, 
    if you call a function that takes no parameters, but you pass it parameters 
    in .map(), the thread will throw an exception. Unfortunately, ThreadPoolExecutor 
    will hide that exception, and (in the case above) the program terminates 
    with no output. This can be quite confusing to debug at first.

See also
  - https://superfastpython.com/threadpoolexecutor-map-vs-submit/
  - https://superfastpython.com/threadpoolexecutor-map/
  - https://superfastpython.com/threadpool-python/#Common_Objections_to_Using_ThreadPool
"""
