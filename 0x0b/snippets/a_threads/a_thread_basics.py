# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about starting and joining threads.

Teaching focus
  - start and join threads

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import threading
import time
from thread_helper import dt, thread_info


def start_a_thread_and_join():
    """ start a thread and join """
    print("\nstart_a_thread_and_join\n=======================")

    dt(reset=True)                          # reset relative times in output

    # this is the code we want to run in a thread
    def runnable():
        print(f"{dt()}  a|  - start of {threading.current_thread().name!r}")
        print(f"{dt()}  b|  - thread info: {thread_info(threading.current_thread())}")
        print(f"{dt()}  c|  - doing work for 0.5s...")
        time.sleep(0.5)
        print(f"{dt()}  d|  - end of {threading.current_thread().name!r}")

    print(f"{dt()}  1| current thread info: {thread_info(threading.current_thread())}")
    print(f"{dt()}  2| create new thread (not started yet) ")

    thread = threading.Thread(target=runnable)  # new thread, not started
    print(f"{dt()}  3| new thread info: {thread_info(thread)}")

    time.sleep(0.2)

    print(f"{dt()}  4| start thread {thread.name!r}")
    thread.start()

    print(f"{dt()}  5| doing work for 0.3s...")
    time.sleep(0.3)

    print(f"{dt()}  6| wait for thread {thread.name!r}")
    thread.join()

    print(f"{dt()}  7| joined - done here")


def start_two_threads_and_join():
    """ start two threads and join """
    print("\nstart_two_threads_and_join\n==========================")

    dt(reset=True)

    def do_work(connect_or_signin: int, message: str):
        print(f"{dt()}  a|  - start of {threading.current_thread().name!r}, {message=}")
        print(f"{dt()}  b|  - thread info: {thread_info(threading.current_thread())}")
        if connect_or_signin:
            for i in range(1,4):
                print(f"{dt()}  c|  - try {i} to connect")
                time.sleep(0.1)
            print(f"{dt()}  d|  - connected, end of {threading.current_thread().name!r}")
        else:
            time.sleep(0.2)
            print(f"{dt()} -e|  - signed in, end of {threading.current_thread().name!r}")

    print(f"{dt()}  1| create threads")
    t1 = threading.Thread(target=do_work, name="conn", args=(True,"connect"))
    t2 = threading.Thread(target=do_work, name="sign", kwargs={'connect_or_signin':False,'message':"read"})

    time.sleep(0.2)

    print(f"{dt()}  2| start threads")
    t1.start()
    t2.start()

    """
    remarks:
      - threads can be named
      - args can be given as a tuple, or as a dict
      - both threads use the same function, the code base, but they run independently
      - output can be different for each run, because of the randomness
    """

    print(f"{dt()}  3| wait for join...")
    t1.join()
    t2.join()

    print(f"{dt()}  4| joined - done here")


if __name__ == "__main__":
    start_a_thread_and_join()
    start_two_threads_and_join()


"""
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
"""
