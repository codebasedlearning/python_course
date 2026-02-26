# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 7 (Unit 0x07)

Refactored from Part 6: add decorators for retry, timing, validation,
and an analyzer registry.
"""

from __future__ import annotations

import functools
import random
import time
from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Reading:
    value: float
    timestamp: int
    sensor_id: str


# --- Decorator: @timed ---

def timed(func):
    """Print execution time of the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        dt = time.perf_counter() - t0
        print(f"    [@timed] {func.__name__} took {dt:.4f}s")
        return result
    return wrapper


# --- Decorator: @retry ---

def retry(max_attempts=3, delay=0.1):
    """Retry a function up to max_attempts times on exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"    [@retry] {func.__name__} attempt {attempt} failed: {e}")
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator


# --- Decorator: @validate_readings ---

def validate_readings(low: float = -40.0, high: float = 80.0):
    """Decorator that filters out invalid readings from a generator function."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for r in func(*args, **kwargs):
                if low <= r.value <= high:
                    yield r
                else:
                    print(f"    [@validate] dropped {r.sensor_id} t={r.timestamp} "
                          f"value={r.value:.1f}")
        return wrapper
    return decorator


# --- Decorator: @register for analyzer registry ---

ANALYZERS: dict[str, callable] = {}


def register(func):
    """Register a function in the global ANALYZERS dict."""
    ANALYZERS[func.__name__] = func
    return func


# --- Data source with retry (simulates flaky reads) ---

class FlakySource:
    """Simulates a data source that occasionally fails."""

    def __init__(self, data: list[float], fail_rate: float = 0.5, seed: int = 42):
        self._data = data
        self._rng = random.Random(seed)
        self._fail_rate = fail_rate

    @retry(max_attempts=5, delay=0.05)
    def read_all(self, sensor_id: str) -> list[Reading]:
        if self._rng.random() < self._fail_rate:
            raise ConnectionError("sensor timeout")
        return [Reading(v, i, sensor_id) for i, v in enumerate(self._data)]


# --- Validated generator ---

@validate_readings(low=15.0, high=30.0)
def stream_readings(readings: list[Reading]) -> Iterator[Reading]:
    yield from readings


# --- Registered analyzers ---

@register
def count_readings(readings: list[Reading]) -> int:
    return len(readings)


@register
def average_value(readings: list[Reading]) -> float:
    values = [r.value for r in readings]
    return sum(values) / len(values) if values else 0.0


@register
def max_value(readings: list[Reading]) -> float:
    return max(r.value for r in readings) if readings else 0.0


# --- Main ---

TEMPS = [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6]


@timed
def run_analysis():
    print("01| Reading from flaky source (with @retry):")
    source = FlakySource(TEMPS, fail_rate=0.6, seed=7)
    readings = source.read_all("temp_north")
    print(f"    got {len(readings)} readings\n")

    print("02| Streaming with @validate_readings:")
    valid = list(stream_readings(readings))
    print(f"    {len(valid)} valid out of {len(readings)} total\n")

    print("03| Running registered analyzers:")
    for name, fn in ANALYZERS.items():
        result = fn(valid)
        print(f"    {name}: {result}")

    print()


def main():
    run_analysis()

    print(f"04| Registered analyzers: {list(ANALYZERS.keys())}")
    print(f"05| average_value.__name__ = {average_value.__name__}  (wraps preserved)")


if __name__ == "__main__":
    main()
