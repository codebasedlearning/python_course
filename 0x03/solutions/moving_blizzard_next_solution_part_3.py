# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 3 (Unit 0x03)

Refactored from Part 2: dicts become proper classes.
Introduces dataclass, enum, __repr__, __eq__, __lt__.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from functools import total_ordering


class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()
    WATER_LEVEL = auto()


@dataclass(frozen=True)
class Reading:
    value: float
    timestamp: int          # simple integer index for now
    sensor_id: str


@total_ordering
class Sensor:
    def __init__(self, sensor_id: str, sensor_type: SensorType,
                 readings: list[Reading] | None = None):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.readings: list[Reading] = readings or []

    def add(self, value: float, timestamp: int):
        self.readings.append(Reading(value, timestamp, self.sensor_id))

    @property
    def values(self) -> list[float]:
        return [r.value for r in self.readings]

    @property
    def average(self) -> float:
        v = self.values
        return sum(v) / len(v) if v else 0.0

    def detect_spikes(self, threshold: float = 5.0) -> list[int]:
        v = self.values
        return [i for i in range(1, len(v)) if abs(v[i] - v[i - 1]) > threshold]

    def __repr__(self):
        return (f"Sensor({self.sensor_id!r}, {self.sensor_type.name}, "
                f"{len(self.readings)} readings, avg={self.average:.2f})")

    def __eq__(self, other):
        if not isinstance(other, Sensor):
            return NotImplemented
        return self.sensor_id == other.sensor_id

    def __lt__(self, other):
        if not isinstance(other, Sensor):
            return NotImplemented
        return self.average < other.average

    def __hash__(self):
        return hash(self.sensor_id)


# --- Build sensors from the old raw data ---

RAW = {
    "temp_north": (SensorType.TEMPERATURE,
                   [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6]),
    "temp_south": (SensorType.TEMPERATURE,
                   [21.0, 20.5, 22.3, 21.8, 23.1, 22.0, 21.5, 20.9, 21.2, 22.7]),
    "humidity":   (SensorType.HUMIDITY,
                   [65.0, 68.2, 70.1, 72.5, 69.0, 67.3, 71.8, 74.0, 66.5, 63.9]),
    "water_lvl":  (SensorType.WATER_LEVEL,
                   [1.2, 1.3, 1.1, 1.5, 2.8, 1.4, 1.2, 1.3, 1.6, 1.1]),
}


def build_sensors() -> list[Sensor]:
    sensors = []
    for sid, (stype, values) in RAW.items():
        s = Sensor(sid, stype)
        for i, v in enumerate(values):
            s.add(v, timestamp=i)
        sensors.append(s)
    return sensors


def main():
    sensors = build_sensors()

    for s in sensors:
        print(f"01| {s}")
        spikes = s.detect_spikes()
        if spikes:
            print(f"    spikes at indices: {spikes}")

    print()
    ranked = sorted(sensors, reverse=True)
    print("02| Ranked by average (desc):")
    for s in ranked:
        print(f"    {s.sensor_id:12s}  avg={s.average:.2f}")

    print()
    north, south = sensors[0], sensors[1]
    print(f"03| {north.sensor_id} == {south.sensor_id}? {north == south}")
    print(f"04| {north.sensor_id} <  {south.sensor_id}? {north < south}")

    print()
    sensor_set = {sensors[0], sensors[0], sensors[1]}
    print(f"05| Set of sensors: {sensor_set}  (dedup works via __hash__)")


if __name__ == "__main__":
    main()
