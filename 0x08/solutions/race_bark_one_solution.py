# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Race Bark'

Count primes in a range with a pool of worker threads, three ways:
  1) a shared counter WITHOUT a lock        -> race condition (flaky count)
  2) a shared counter WITH threading.Lock   -> correct, but contended
  3) no shared state, partial counts via Futures -> correct and lock-free

Note: on the standard (GIL) build the race in (1) often hides - the GIL rarely
switches threads inside the tiny read-modify-write window. Run on the
free-threading build ('uv run --python 3.14t ...') to see it break reliably.
"""

import concurrent.futures
import threading
import time


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


# --- shared state for variants 1 and 2 ---------------------------------------

prime_count = 0
lock = threading.Lock()


def worker_racy(n0: int, n1: int):
    """ increment a shared counter - the increment is the critical region """
    global prime_count
    for n in range(n0, n1):
        if is_prime(n):
            current = prime_count           # read  ... another thread may write here
            current = current + 1           # modify (on a now-stale value)
            prime_count = current           # write  -> lost updates


def worker_locked(n0: int, n1: int):
    """ same, but the critical region is serialized by a mutex """
    global prime_count
    for n in range(n0, n1):
        if is_prime(n):
            with lock:                      # lock only the increment, not the prime check
                prime_count += 1


# --- variant 3: no shared state ----------------------------------------------

def count_in_range(n0: int, n1: int) -> int:
    """ pure function: returns its own partial count, shares nothing """
    return sum(1 for n in range(n0, n1) if is_prime(n))


# --- drivers ------------------------------------------------------------------

def chunks(n0: int, n1: int, workers: int):
    step = (n1 - n0) // workers
    bounds = [n0 + k * step for k in range(workers)] + [n1]
    return list(zip(bounds, bounds[1:]))


def run_shared(title: str, worker, n0: int, n1: int, workers: int, expected: int):
    global prime_count
    prime_count = 0
    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for a, b in chunks(n0, n1, workers):
            executor.submit(worker, a, b)
    dt = time.perf_counter() - t0
    ok = "OK" if prime_count == expected else f"WRONG (lost {expected - prime_count})"
    print(f" a| {title:<23} -> {prime_count} [{ok}], {dt:.3f}s")


def run_lockfree(n0: int, n1: int, workers: int, expected: int):
    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(count_in_range, a, b) for a, b in chunks(n0, n1, workers)]
        total = sum(f.result() for f in futures)   # collect partial counts
    dt = time.perf_counter() - t0
    ok = "OK" if total == expected else f"WRONG (off by {expected - total})"
    print(f" b| {'lock-free (Futures)':<23} -> {total} [{ok}], {dt:.3f}s")


if __name__ == "__main__":
    n0, n1, workers = 2, 200000, 8

    expected = count_in_range(n0, n1)       # ground truth (serial)
    print(f" 1| primes in [{n0}, {n1}) = {expected} (serial truth), {workers=}\n")

    print(" 2| run a few times - the racy count may drift (esp. on a no-GIL build):")
    for _ in range(3):
        run_shared("racy (no lock)", worker_racy, n0, n1, workers, expected)
    print()

    print(" 3| with a mutex and lock-free - both stable and correct:")
    run_shared("locked (threading.Lock)", worker_locked, n0, n1, workers, expected)
    run_lockfree(n0, n1, workers, expected)
