# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 8 (Unit 0x08)

Refactored from Part 7: concurrent sensor polling via ThreadPoolExecutor.
Thread-safe data collection. Compare serial vs. threaded performance.
"""

from __future__ import annotations

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass(frozen=True)
class Reading:
    value: float
    timestamp: int
    sensor_id: str


# --- Simulated sensor that takes time to respond ---

SENSOR_DATA = {
    "temp_north": [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6],
    "temp_south": [21.0, 20.5, 22.3, 21.8, 23.1, 22.0, 21.5, 20.9, 21.2, 22.7],
    "humidity":   [65.0, 68.2, 70.1, 72.5, 69.0, 67.3, 71.8, 74.0, 66.5, 63.9],
    "water_lvl":  [1.2, 1.3, 1.1, 1.5, 2.8, 1.4, 1.2, 1.3, 1.6, 1.1],
}


def poll_sensor(sensor_id: str, delay: float = 0.3) -> list[Reading]:
    """Simulate polling a remote sensor (IO-bound: network delay)."""
    time.sleep(delay)  # simulate network latency
    values = SENSOR_DATA.get(sensor_id, [])
    return [Reading(v, i, sensor_id) for i, v in enumerate(values)]


# --- Thread-safe collector ---

class SensorCollector:
    """Collects readings from multiple sensors, thread-safe."""

    def __init__(self):
        self._lock = threading.Lock()
        self._all_readings: dict[str, list[Reading]] = {}

    def add(self, sensor_id: str, readings: list[Reading]):
        with self._lock:
            self._all_readings[sensor_id] = readings

    @property
    def readings(self) -> dict[str, list[Reading]]:
        with self._lock:
            return dict(self._all_readings)


# --- Serial vs. threaded ---

def poll_serial(sensor_ids: list[str]) -> dict[str, list[Reading]]:
    result = {}
    for sid in sensor_ids:
        result[sid] = poll_sensor(sid)
    return result


def poll_threaded(sensor_ids: list[str]) -> dict[str, list[Reading]]:
    collector = SensorCollector()

    with ThreadPoolExecutor(max_workers=len(sensor_ids)) as pool:
        futures = {pool.submit(poll_sensor, sid): sid for sid in sensor_ids}
        for future in as_completed(futures):
            sid = futures[future]
            collector.add(sid, future.result())

    return collector.readings


def main():
    ids = list(SENSOR_DATA.keys())

    # Serial
    t0 = time.perf_counter()
    serial_result = poll_serial(ids)
    serial_time = time.perf_counter() - t0
    print(f"01| Serial:   {len(serial_result)} sensors in {serial_time:.2f}s")

    # Threaded
    t0 = time.perf_counter()
    threaded_result = poll_threaded(ids)
    threaded_time = time.perf_counter() - t0
    print(f"02| Threaded: {len(threaded_result)} sensors in {threaded_time:.2f}s")

    speedup = serial_time / threaded_time if threaded_time > 0 else 0
    print(f"03| Speedup:  {speedup:.1f}x")

    print()
    print("04| Results match:", end=" ")
    for sid in ids:
        s_vals = [r.value for r in serial_result[sid]]
        t_vals = [r.value for r in threaded_result[sid]]
        assert s_vals == t_vals, f"mismatch for {sid}"
    print("yes")

    print()
    print("05| This works because sensor polling is IO-bound (time.sleep).")
    print("    The GIL does not block threads that are waiting for IO.")


if __name__ == "__main__":
    main()
