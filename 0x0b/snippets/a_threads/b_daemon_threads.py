# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about deamon threads and atexit.

Teaching focus
  - start threads as daemons
  - register atexit functions

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import threading
import time
import atexit
from thread_helper import dt


def start_a_thread_without_join(as_daemon: bool):       # daemons and threads
    """ start a thread without a join """
    print("\nstart_a_thread_without_join\n=====================")

    def runnable():
        print(f"{dt()}  a|  - start of {threading.current_thread().name!r}")
        time.sleep(0.5)
        print(f"{dt()}  b|  - end of {threading.current_thread().name!r}")

    print(f"{dt()}  1| start thread")
    thread = threading.Thread(target=runnable, daemon=as_daemon)  # new thread, not started
    thread.start()
    time.sleep(0.3)


if __name__ == "__main__":
    atexit.register(lambda: print(f"{dt()}  2| end of script"))
    start_a_thread_without_join(as_daemon=False)         # try to start as daemon
    print(f"{dt()}  3| end of 'main-guard'")


"""
daemons and threads
From https://realpython.com/intro-to-python-threading/#daemon-threads
  - If a program is running Threads that are not daemons, then the program 
    will wait for those threads to complete before it terminates. 
  - Threads that are daemons, however, are just killed wherever they are 
    when the program is exiting.

atexit
From https://docs.python.org/3/library/atexit.html
  - The 'atexit' module defines functions to register and unregister cleanup 
    functions. 
  - Functions thus registered are automatically executed upon normal 
    interpreter termination.
  - 'atexit' runs these functions in the reverse order in which they were 
    registered [...].
"""
