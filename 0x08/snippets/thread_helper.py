# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This module contains helper functions for threads. """
import functools
import re
import sys
import sysconfig
import threading
import time

thread_regex = re.compile(r"Thread-(\d+)")  # compile the regular expression once
threadpool_regex = re.compile(r"ThreadPoolExecutor-(\d+)_(\d+)")  # compile the regular expression once

def name_translation(name:str):
    if name=="MainThread":
        name="main"
    elif match:=thread_regex.search(name):
            number = int(match.group(1))    # extract and convert to integer
            name = f"T-{number}"
    elif match:=threadpool_regex.search(name):
            number1 = int(match.group(1))
            number2 = int(match.group(2))
            name = f"T-{number1}{number2}"
    return name

def dt(reset=False):
    if not hasattr(dt, 't0') or reset:
        dt.t0 = time.perf_counter()         # ty:ignore[unresolved-attribute]
    diff = time.perf_counter() - dt.t0      # ty:ignore[unresolved-attribute]
    name = name_translation(threading.current_thread().name)
    return f"[{name:>4} | {diff: >6.3f}]"

def timing_reset(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dt(reset=True)
        return func(*args, **kwargs)
    return wrapper

###

def thread_info(thread):
    # !r uses __repr__, ident is Python-specific, OS-native thread ID
    return f"[{thread.name!r},ident={thread.ident},native={thread.native_id}|alive={thread.is_alive()}]"
    #return f"{{name='{thread.name}',ident={thread.ident},native_id={thread.native_id}}}"

def tprint(label, *args, **kwargs):
    print(f"{dt()} {label}", *args, **kwargs)

# dummy load

def _time_boxed_worker(budget:float):
    time.sleep(budget)

load_image = _time_boxed_worker
query_database = _time_boxed_worker
connect_database = _time_boxed_worker
sign_in = _time_boxed_worker


def gil_info():
    """ Detects GIL status, i.e. do we have a Free-Threading (`t` variant w.o. GIL) and is it active? """
    gil_removed = sysconfig.get_config_vars().get("Py_GIL_DISABLED") == 1
    gil_active = not hasattr(sys, '_is_gil_enabled') or sys._is_gil_enabled()   # pylint: disable=protected-access
    return gil_removed, gil_active
