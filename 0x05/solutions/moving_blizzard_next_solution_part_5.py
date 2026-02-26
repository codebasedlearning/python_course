# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 5 (Unit 0x05)

Refactored from Part 4: data sources now yield lazily via generators.
Build a pipeline: stream → filter_valid → moving_average → detect_anomalies.
Nothing is loaded into memory all at once.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol


@dataclass(frozen=True)
class Reading:
    value: float
    timestamp: int
    sensor_id: str


# --- Lazy DataSource protocol ---

class DataSource(Protocol):
    def stream(self, sensor_id: str) -> Iterator[Reading]: ...


class ListSource:
    def __init__(self, raw: dict[str, list[float]]):
        self._raw = raw

    def stream(self, sensor_id: str) -> Iterator[Reading]:
        for i, v in enumerate(self._raw.get(sensor_id, [])):
            yield Reading(v, i, sensor_id)


# --- Generator pipeline stages ---

def filter_valid(readings: Iterator[Reading],
                 low: float = -40.0, high: float = 80.0) -> Iterator[Reading]:
    """Drop readings outside the valid sensor range."""
    for r in readings:
        if low <= r.value <= high:
            yield r


def moving_average(readings: Iterator[Reading],
                   window: int = 3) -> Iterator[tuple[Reading, float]]:
    """Yield (reading, moving_avg) pairs using a sliding window."""
    buf: list[float] = []
    for r in readings:
        buf.append(r.value)
        if len(buf) > window:
            buf.pop(0)
        avg = sum(buf) / len(buf)
        yield r, avg


def detect_anomalies(stream: Iterator[tuple[Reading, float]],
                     deviation: float = 5.0) -> Iterator[tuple[Reading, float, float]]:
    """Yield readings where the value deviates from the moving average."""
    for r, avg in stream:
        diff = abs(r.value - avg)
        if diff > deviation:
            yield r, avg, diff


# --- Orchestration ---

RAW_DATA = {
    "temp_north": [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6],
    "temp_south": [21.0, 20.5, 22.3, 21.8, 23.1, 22.0, 21.5, 20.9, 21.2, 22.7],
    "humidity":   [65.0, 68.2, 70.1, 72.5, 69.0, 67.3, 71.8, 74.0, 66.5, 63.9],
    "water_lvl":  [1.2, 1.3, 1.1, 1.5, 2.8, 1.4, 1.2, 1.3, 1.6, 1.1],
}


def run_pipeline(source: DataSource, sensor_id: str):
    """Full lazy pipeline: stream → filter → moving_avg → anomalies."""
    raw = source.stream(sensor_id)
    valid = filter_valid(raw)
    smoothed = moving_average(valid, window=3)
    anomalies = detect_anomalies(smoothed, deviation=3.0)
    return anomalies


def main():
    source = ListSource(RAW_DATA)

    print("01| Full pipeline — anomalies in temp_north:")
    for r, avg, diff in run_pipeline(source, "temp_north"):
        print(f"    t={r.timestamp:2d}  value={r.value:5.1f}  "
              f"moving_avg={avg:5.1f}  deviation={diff:4.1f}")

    print()
    print("02| Full pipeline — anomalies in water_lvl:")
    for r, avg, diff in run_pipeline(source, "water_lvl"):
        print(f"    t={r.timestamp:2d}  value={r.value:5.1f}  "
              f"moving_avg={avg:5.1f}  deviation={diff:4.1f}")

    print()
    print("03| Demonstrating laziness:")
    print("    All pipeline stages are generators — no list is ever fully materialized.")
    raw_gen = source.stream("temp_north")
    print(f"    type(raw_gen) = {type(raw_gen).__name__}")


if __name__ == "__main__":
    main()
