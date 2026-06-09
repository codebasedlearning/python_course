# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about daemon threads and atexit.

Teaching focus
  - start threads as daemons
  - register atexit functions

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

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import atexit
import threading

from thread_helper import load_image, sign_in, timing_reset, tprint

from utils import print_function_header


@timing_reset
@print_function_header
def start_a_thread_without_join(as_daemon: bool):
    """ start a thread without a join """

    def load_job():
        tprint(f" a| - start of {threading.current_thread().name!r}")
        load_image(budget=0.5)
        tprint(f" b| - end of {threading.current_thread().name!r}")

    tprint(" 1| start thread")
    thread = threading.Thread(target=load_job, daemon=as_daemon)
    thread.start()
    # sign in is shorter than loading the image, so
    sign_in(budget=0.3)                     
    tprint(" 2| end of 'start_a_thread_without_join'")


atexit.register(lambda: tprint(" c| - end of script"))

if __name__ == "__main__":
    # start as daemon or not
    # -> as deamon: do not wait for it, end script immediately
    # -> not a daemon: wait for it, end script only after it is done
    start_a_thread_without_join(as_daemon=False)
    tprint(" 3| end of 'main-guard'")
