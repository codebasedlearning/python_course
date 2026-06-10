# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This module contains helper functions for threads. """
import functools
import multiprocessing
import re
import sys
import sysconfig
import threading
import time

# compile the regular expression once
_thread_regex = re.compile(r"Thread-(\d+)")
_threadpool_regex = re.compile(r"ThreadPoolExecutor-(\d+)_(\d+)")
_process_regex = re.compile(r"Process-(\d+)")

def _thread_name_translation(name:str):
    if name=="MainThread":
        name="main"
    elif match:=_thread_regex.search(name):
            number = int(match.group(1))
            name = f"T-{number}"
    elif match:=_threadpool_regex.search(name):
            number1 = int(match.group(1))
            number2 = int(match.group(2))
            name = f"T-{number1}{number2}"
    return name

def _process_name_translation(name:str):
    if name=="MainProcess":
        name="MAIN"
    elif match:=_process_regex.search(name):
        number = int(match.group(1))
        name = f"P-{number}"
    # there is also SpawnPoolWorker - skip for now
    return name

def _timing_info(*, incl_proc=False):
    #if not hasattr(_timing_info, 't0'):
    #    _timing_info.t0 = time.perf_counter()  # ty:ignore[unresolved-attribute]
    t0 = vars(_timing_info).setdefault("t0", time.perf_counter())

    diff = time.perf_counter() - t0    # y:ignore[unresolved-attribute]
    tinfo = f"{_thread_name_translation(threading.current_thread().name):>4} | "
    if incl_proc:
        pinfo = f"{_process_name_translation(multiprocessing.current_process().name):>5}:"
    else:
        pinfo = ""
    return f"[{pinfo}{tinfo}{diff: >6.3f}]"

def _reset_timing_info():
    vars(_timing_info).pop("t0", None)      # bypassing the attribute protocol
    #if hasattr(_timing_info, 't0'):
    #    del _timing_info.t0                 # ty:ignore[unresolved-attribute]

def reset_timing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _reset_timing_info()
        return func(*args, **kwargs)
    return wrapper

def tprint(label, *args, **kwargs):
    print(f"{_timing_info()} {label}", *args, **kwargs)

def ptprint(label, *args, **kwargs):
    print(f"{_timing_info(incl_proc=True)} {label}", *args, **kwargs)

###

def thread_info(thread):
    # !r uses __repr__, ident is Python-specific, native_id is OS-native thread ID
    alive_info = f"{'alive' if thread.is_alive() else 'dead'}"
    ident_info = f"{thread.ident if thread.ident else '-'}"
    native_info = f"{thread.native_id if thread.native_id else '-'}"
    return f"[{thread.name!r},{ident_info}|{native_info},{alive_info!r}]"

def process_info(process):
    alive_info = f"{'alive' if process.is_alive() else 'dead'}"
    ident_info = f"{process.ident if process.ident else '-'}"
    return f"[{process.name!r},{ident_info},{alive_info!r}]" # ,native={process.native_id}

def gil_info():
    """ Detects GIL status, i.e. do we have a Free-Threading (`t` variant w.o. GIL) and is it active? """
    is_gil_removed = sysconfig.get_config_vars().get("Py_GIL_DISABLED") == 1
    removed = "removed" if is_gil_removed else "present"
    gil_active = not hasattr(sys, '_is_gil_enabled') or sys._is_gil_enabled()
    active = "active" if gil_active else "inactive"
    # pylint: disable=protected-access
    #return gil_removed, gil_active
    return f"[GIL:{removed!r},{active!r}]"

def print_gil_info():
    print(f"\n{gil_info()}\n")

# dummy load

def _time_boxed_worker(budget:float):
    time.sleep(budget)

load_image = _time_boxed_worker
query_database = _time_boxed_worker
connect_database = _time_boxed_worker
sign_in = _time_boxed_worker

