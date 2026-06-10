# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about starting and joining threads.

Teaching focus
  - start and join threads

new threads, not started
  - Until start a thread is only an object. Usually it is not cheap to create
    and/or start a thread, so this is the reason for using thread pools,
    which we will see later.

sleep
  - In the examples, 'sleep' always represents a task that takes some time
    to complete. This could be a calculation or a complex IO operation such
    as querying a database.

join
  - Now that the thread has been started, the question is how long will it
    run and do I have a need for the data that has been created there.
    This is where you need to think about the properties of the thread in
    terms of its life cycle. The 'join' command is waiting for the thread
    to finish its work. This is called a 'blocking call'.
  - By default, Python waits for non-daemon threads before the process exits.

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import threading

from utils import (
    connect_database,
    load_image,
    print_function_header,
    print_gil_info,
    query_database,
    reset_timing,
    sign_in,
    thread_info,
    tprint,
)

# Note:
# - tprint is a wrapper around print, that adds a timestamp and a thread name.
# - dt is a wrapper around time.time(), that gives the relative time.
# - timing_reset is a decorator that resets the relative time counter in dt.
# - load_image and query_database are blocking functions that simulate IO operations.
#   Both take a 'budget' parameter, which is the time in seconds that the function
#   should take to complete.
# - thread_info is a function that returns a string with thread info.
# - "!r" is a string formatting operator that prints the value of an object in a 'repr' style.

@reset_timing                               # reset relative times in output
@print_function_header
def start_a_thread_and_join():
    """ start a thread and join """

    # this is the code we want to run in a thread
    def load_job():
        tprint(f" a| - start of {threading.current_thread().name!r}")
        tprint(f" b| - thread info: {thread_info(threading.current_thread())}")
        tprint( " c| - load 5 images for 0.5s...")
        for no in range(1,6):
            load_image(budget=0.1)
            tprint(f" d| - image {no=} loaded")
        tprint(f" e| - work done, end of {threading.current_thread().name!r}")

    # tprint is basically this: print(f"{dt()}  1| current thread info...
    tprint(f" 1| current thread info: {thread_info(threading.current_thread())}")

    tprint( " 2| create new thread (not started yet) ")
    load = threading.Thread(target=load_job, name="load")                  # new thread, not started yet
    tprint(f" 3| new thread info: {thread_info(load)}")

    tprint( " 4| query database for 0.2s...")
    query_database(budget=0.2)                                  # blocks main thread for 0.2s

    tprint(f" 5| work done, start thread {load.name!r}")
    load.start()

    tprint( " 6| query database for 0.3s...")
    query_database(budget=0.3)

    tprint(f" 7| work done, wait for thread {load.name!r}")
    load.join()

    tprint( " 8| joined - done here")
    tprint(f" 9| thread info: {thread_info(load)}")


@reset_timing
@print_function_header
def start_two_threads_and_join():
    """ start two threads and join """

    def worker(action: str, attempts: int):
        tprint(f" a| - start of {threading.current_thread().name!r}, {action=}")
        tprint(f" b| - current thread info: {thread_info(threading.current_thread())}")
        match action:
            case "connect":
                for no in range(1,attempts+1):
                    tprint(f" c| - try {no=} to connect")
                    connect_database(budget=0.1)
                tprint(f" d| - connected, end of {threading.current_thread().name!r}")
            case "sign in":
                for no in range(1,attempts+1):
                    tprint(f" e| - try {no=} to sign in")
                    sign_in(budget=0.15)
                tprint(f" f| - signed in, end of {threading.current_thread().name!r}")

    tprint(" 1| create threads")
    t1 = threading.Thread(target=worker, name="conn", args=("connect", 4))
    t2 = threading.Thread(target=worker, name="sign", kwargs={'action':"sign in",'attempts':3})

    tprint(" 2| start threads")
    t1.start()
    t2.start()

    """
    remarks:
      - threads can be named
      - args can be given as a tuple, or as a dict
      - both threads use the same function, the code base, but they run independently
      - output can be different for each run, because of the randomness
    """

    tprint(" 3| wait for join...")
    t1.join()
    t2.join()

    tprint(" 4| joined - done here")


if __name__ == "__main__":
    start_a_thread_and_join()
    start_two_threads_and_join()
    print_gil_info()
