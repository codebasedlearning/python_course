# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 9 (Unit 0x09)

Final version: async sensor polling with asyncio.gather.
Bounded descriptor for sensor value validation (ties into Cobalt Reef).
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass


# --- Bounded descriptor (same pattern as Cobalt Reef) ---

class Bounded:
    """Data descriptor that enforces min/max bounds on a numeric attribute."""

    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.public_name} must be numeric, got {type(value).__name__}")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"{self.public_name}={value} out of range "
                f"[{self.min_value}, {self.max_value}]"
            )
        setattr(obj, self.private_name, value)


# --- Sensor config with descriptors ---

class SensorConfig:
    """Configuration for a sensor with descriptor-validated bounds."""
    poll_interval = Bounded(0.01, 60.0)
    min_valid = Bounded(-100.0, 100.0)
    max_valid = Bounded(-100.0, 200.0)

    def __init__(self, sensor_id: str, poll_interval: float,
                 min_valid: float, max_valid: float):
        self.sensor_id = sensor_id
        self.poll_interval = poll_interval
        self.min_valid = min_valid
        self.max_valid = max_valid


@dataclass(frozen=True)
class Reading:
    value: float
    timestamp: int
    sensor_id: str


# --- Simulated sensor data ---

SENSOR_DATA = {
    "temp_north": [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6],
    "temp_south": [21.0, 20.5, 22.3, 21.8, 23.1, 22.0, 21.5, 20.9, 21.2, 22.7],
    "humidity":   [65.0, 68.2, 70.1, 72.5, 69.0, 67.3, 71.8, 74.0, 66.5, 63.9],
    "water_lvl":  [1.2, 1.3, 1.1, 1.5, 2.8, 1.4, 1.2, 1.3, 1.6, 1.1],
}


# --- Async sensor polling ---

async def poll_sensor(config: SensorConfig) -> list[Reading]:
    """Simulate async sensor polling with network delay."""
    await asyncio.sleep(config.poll_interval)  # non-blocking!
    values = SENSOR_DATA.get(config.sensor_id, [])
    readings = []
    for i, v in enumerate(values):
        if config.min_valid <= v <= config.max_valid:
            readings.append(Reading(v, i, config.sensor_id))
    return readings


async def poll_all(configs: list[SensorConfig]) -> dict[str, list[Reading]]:
    """Poll all sensors concurrently."""
    tasks = [poll_sensor(cfg) for cfg in configs]
    results = await asyncio.gather(*tasks)
    return {cfg.sensor_id: readings for cfg, readings in zip(configs, results)}


# --- Main ---

def main():
    configs = [
        SensorConfig("temp_north", poll_interval=0.3, min_valid=-40.0, max_valid=25.0),
        SensorConfig("temp_south", poll_interval=0.3, min_valid=-40.0, max_valid=80.0),
        SensorConfig("humidity",   poll_interval=0.3, min_valid=0.0,   max_valid=100.0),
        SensorConfig("water_lvl",  poll_interval=0.3, min_valid=0.0,   max_valid=5.0),
    ]

    # Async polling
    t0 = time.perf_counter()
    results = asyncio.run(poll_all(configs))
    dt = time.perf_counter() - t0

    print(f"01| Polled {len(results)} sensors concurrently in {dt:.2f}s")
    print(f"    (serial would take ~{0.3 * len(configs):.1f}s)")

    print()
    for sid, readings in results.items():
        values = [r.value for r in readings]
        avg = sum(values) / len(values) if values else 0.0
        print(f"02| {sid:12s}  readings={len(readings):2d}  avg={avg:.2f}")

    # Descriptor validation demo
    print()
    print("03| Descriptor validation:")
    try:
        bad = SensorConfig("broken", poll_interval=0.1, min_valid=-40.0, max_valid=80.0)
        bad.poll_interval = 999.0  # exceeds Bounded(0.01, 60.0)
    except ValueError as e:
        print(f"    Caught: {e}")

    try:
        SensorConfig("broken", poll_interval="fast", min_valid=0, max_valid=100)
    except TypeError as e:
        print(f"    Caught: {e}")

    print()
    print("04| temp_north filtered out readings > 25.0 via config bounds.")
    print("    The Bounded descriptor ensures these bounds are always valid.")


if __name__ == "__main__":
    main()
