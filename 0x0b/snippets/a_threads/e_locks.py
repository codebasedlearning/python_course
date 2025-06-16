# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about deadlocks and livelocks.

Teaching focus
  - deadlocks and livelocks

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import threading
import time
from thread_helper import dt


def discuss_deadlocks():
    """ discuss deadlocks """
    print("\ndiscuss_deadlocks\n=================")

    def thread_function(first_lock,second_lock):
        print(f"{dt()}  a|   thread starting, get locks")
        with first_lock:
            time.sleep(0.1)
            print(f"{dt()}  b|   got lock {id(first_lock)}, get lock {id(second_lock)}")
            with second_lock:
                print(f"{dt()}  c|   got lock {id(second_lock)}, do work")

    print(f"{dt()}  1| create locks, start threads")
    lock1 = threading.Lock()
    lock2 = threading.Lock()

    t1 = threading.Thread(target=thread_function, args=(lock1,lock2))
    t2 = threading.Thread(target=thread_function, args=(lock2,lock1))
    t1.start()
    t2.start()

    print(f"{dt()}  2| wait for threads...")
    t1.join()
    t2.join()
    print(f"{dt()}  3| done")


def discuss_livelocks():
    """ discuss deadlocks """
    print("\ndiscuss_livelocks\n=================")

    def thread_function(first_lock,second_lock):
        print(f"{dt()}  a|   thread starting, get locks")
        while True:
            print(f"{dt()}  b|   lock status: {first_lock.locked()},{second_lock.locked()}")
            with first_lock:
                time.sleep(1)
                print(f"{dt()}  c|   got lock {id(first_lock)}, get lock {id(second_lock)}")
                if second_lock.locked():
                    print(f"{dt()}  d|   lock {id(second_lock)} not avail., try again later")
                else:
                    with second_lock:
                        print(f"{dt()}  e|   got lock {id(second_lock)}, do work")

    print(f"{dt()}  1| create locks, start threads")
    lock1 = threading.Lock()
    lock2 = threading.Lock()

    t1 = threading.Thread(target=thread_function, args=(lock1,lock2))
    t2 = threading.Thread(target=thread_function, args=(lock2,lock1))
    t1.start()
    t2.start()

    print(f"{dt()}  2| wait for threads...")
    t1.join()
    t2.join()
    print(f"{dt()}  3| done")


def main():
    pass
    # discuss_deadlocks()
    discuss_livelocks()


if __name__ == "__main__":
    main()

"""
deadlocks
  - The basic problem here is that threads have already acquired some 
    resources and are waiting for others, which in turn are being blocked 
    by other threads.
  - See
    https://superfastpython.com/threading-in-python/
    
livelocks
  - In this situation, no thread is blocking, but by continually blocking 
    one resource and asking for the second, no thread is making any progress.
"""
