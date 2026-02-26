# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 4 (Unit 0x04)

Refactored from Part 3: introduce protocols and composition.
DataSource protocol decouples data acquisition from analysis.
Station is composed of sensors + source — no inheritance.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from functools import total_ordering
from typing import Protocol
import random


# --- Domain types (carried forward from Part 3) ---

class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()
    WATER_LEVEL = auto()


@dataclass(frozen=True)
class Reading:
    value: float
    timestamp: int
    sensor_id: str


# --- DataSource protocol ---

class DataSource(Protocol):
    def read_all(self, sensor_id: str) -> list[Reading]: ...


class ListSource:
    """A data source backed by a hardcoded dict of value lists."""

    def __init__(self, raw: dict[str, list[float]]):
        self._raw = raw

    def read_all(self, sensor_id: str) -> list[Reading]:
        values = self._raw.get(sensor_id, [])
        return [Reading(v, i, sensor_id) for i, v in enumerate(values)]


class RandomSource:
    """A data source that generates random readings."""

    def __init__(self, n: int = 10, low: float = 15.0, high: float = 30.0, seed: int = 42):
        self._n = n
        self._low = low
        self._high = high
        self._rng = random.Random(seed)

    def read_all(self, sensor_id: str) -> list[Reading]:
        return [
            Reading(round(self._rng.uniform(self._low, self._high), 1), i, sensor_id)
            for i in range(self._n)
        ]


# --- Analyzer protocol ---

class Analyzer(Protocol):
    def analyze(self, readings: list[Reading]) -> dict: ...


class BasicAnalyzer:
    def analyze(self, readings: list[Reading]) -> dict:
        values = [r.value for r in readings]
        if not values:
            return {"count": 0, "avg": 0.0, "min": 0.0, "max": 0.0}
        return {
            "count": len(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }


# --- Station: composed of source + analyzer ---

class Station:
    def __init__(self, name: str, sensor_ids: list[str],
                 source: DataSource, analyzer: Analyzer):
        self.name = name
        self.sensor_ids = sensor_ids
        self.source = source
        self.analyzer = analyzer

    def report(self):
        print(f"=== Station: {self.name} ===")
        for sid in self.sensor_ids:
            readings = self.source.read_all(sid)
            stats = self.analyzer.analyze(readings)
            print(f"  {sid:12s}  count={stats['count']}  avg={stats['avg']:.2f}  "
                  f"min={stats['min']:.2f}  max={stats['max']:.2f}")


# --- Main ---

RAW_DATA = {
    "temp_north": [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6],
    "temp_south": [21.0, 20.5, 22.3, 21.8, 23.1, 22.0, 21.5, 20.9, 21.2, 22.7],
    "humidity":   [65.0, 68.2, 70.1, 72.5, 69.0, 67.3, 71.8, 74.0, 66.5, 63.9],
}


def main():
    # Version A: hardcoded data via ListSource
    station_a = Station(
        name="Tide Pool Alpha",
        sensor_ids=["temp_north", "temp_south", "humidity"],
        source=ListSource(RAW_DATA),
        analyzer=BasicAnalyzer(),
    )
    station_a.report()

    print()

    # Version B: random data — swap the source, nothing else changes
    station_b = Station(
        name="Tide Pool Beta (random)",
        sensor_ids=["probe_1", "probe_2"],
        source=RandomSource(n=20, low=10.0, high=35.0),
        analyzer=BasicAnalyzer(),
    )
    station_b.report()

    print()
    print("Note: Station did not change — only the DataSource was swapped.")
    print("      That is the Open/Closed Principle in action.")


if __name__ == "__main__":
    main()
