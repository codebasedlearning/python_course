# (C) 2025 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses time measurement.

Teaching focus
  - time

Key differences between `time.time()` and `time.process_time()`
- time()
    - Returns wall-clock time (real-world time)
    - Includes time spent in sleep and waiting for I/O
    - Returns seconds since the epoch (January 1, 1970)
    - Higher resolution, includes fractions of seconds

- process_time()
    - Measures only CPU time used by the current process
    - Excludes sleep and I/O wait time
    - Returns relative value (not tied to epoch)
    - More accurate for pure CPU performance measurement
    - Includes both user and system CPU time (kernel code on behalf of the process)
"""

import time

def sum_up():
    """ benchmark function"""
    s = 0
    for i in range(1000000):
        s += i
    return s

def show_timing():
    """ show io stats """
    print("\nshow_timing\n===========")

    print(" 1| start...", end='')

    # current time (float) in seconds since the Epoch (00:00:00 UTC 1.1.1970)
    start_time = time.time()
    s = sum_up()
    dt = time.time()-start_time             # dt in seconds, *1000 in milliseconds
    print(f" done, {s=}, dt = {dt*1000:.3f} ms")

    print(" 2| start...", end='')
    start_time = time.process_time()
    s = sum_up()
    dt = time.process_time()-start_time     # dt in seconds, *1000 in milliseconds
    print(f" done, {s=}, dt = {dt*1000:.3f} ms")


if __name__ == "__main__":
    show_timing()
