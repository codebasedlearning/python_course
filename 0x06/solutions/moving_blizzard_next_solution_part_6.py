# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 6 (Unit 0x06)

Refactored from Part 5: add file I/O with context managers,
alert thresholds via closures, and sensor type dispatch via match.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class Reading:
    value: float
    timestamp: int
    sensor_id: str


# --- CSV file source with context manager ---

class CSVDataSource:
    """Reads sensor data from a CSV file (sensor_id, timestamp, value)."""

    def __init__(self, path: Path):
        self._path = path

    @contextmanager
    def open_stream(self, sensor_id: str):
        """Context manager that yields a generator of Readings for one sensor."""
        def _gen(f):
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3 and parts[0].strip() == sensor_id:
                    yield Reading(
                        value=float(parts[2]),
                        timestamp=int(parts[1]),
                        sensor_id=parts[0].strip(),
                    )

        fh = open(self._path)
        try:
            yield _gen(fh)
        finally:
            fh.close()


# --- Alert thresholds via closures ---

def make_alert(label: str, min_val: float, max_val: float):
    """Return a closure that checks whether a reading is within bounds."""
    def check(reading: Reading) -> str | None:
        if reading.value < min_val:
            return f"ALERT [{label}]: {reading.sensor_id} t={reading.timestamp} " \
                   f"value={reading.value:.1f} < {min_val}"
        if reading.value > max_val:
            return f"ALERT [{label}]: {reading.sensor_id} t={reading.timestamp} " \
                   f"value={reading.value:.1f} > {max_val}"
        return None
    return check


# --- Sensor type dispatch via match ---

def describe_sensor(sensor_id: str) -> str:
    """Use pattern matching to classify sensors by naming convention."""
    match sensor_id.split("_")[0]:
        case "temp":
            return "Temperature sensor (°C)"
        case "humidity":
            return "Humidity sensor (%)"
        case "water":
            return "Water level sensor (m)"
        case other:
            return f"Unknown sensor type: {other}"


# --- Report writer as a context manager ---

@contextmanager
def report_file(path: Path):
    """Context manager for writing a text report."""
    fh = open(path, "w")
    try:
        fh.write("=== Tide Pool Report ===\n\n")
        yield fh
    finally:
        fh.write("\n=== End of Report ===\n")
        fh.close()


# --- Demo with in-memory data (writes a CSV, then reads it back) ---

RAW_DATA = {
    "temp_north": [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6],
    "humidity":   [65.0, 68.2, 70.1, 72.5, 69.0, 67.3, 71.8, 74.0, 66.5, 63.9],
}


def write_demo_csv(path: Path):
    """Write sample data as CSV so we can read it back."""
    with open(path, "w") as f:
        for sid, values in RAW_DATA.items():
            for i, v in enumerate(values):
                f.write(f"{sid},{i},{v}\n")


def main():
    csv_path = Path("blizzard_data.csv")
    report_path = Path("blizzard_report.txt")

    # 1. Write demo CSV
    write_demo_csv(csv_path)
    print(f"01| Wrote demo data to {csv_path}")

    # 2. Read back via CSVDataSource + context manager
    source = CSVDataSource(csv_path)
    temp_alert = make_alert("Temperature", min_val=16.0, max_val=25.0)
    humidity_alert = make_alert("Humidity", min_val=60.0, max_val=72.0)

    print()
    print("02| Sensor descriptions (match):")
    for sid in ["temp_north", "humidity", "water_lvl"]:
        print(f"    {sid}: {describe_sensor(sid)}")

    print()
    print("03| Alerts for temp_north:")
    with source.open_stream("temp_north") as readings:
        for r in readings:
            msg = temp_alert(r)
            if msg:
                print(f"    {msg}")

    print()
    print("04| Alerts for humidity:")
    with source.open_stream("humidity") as readings:
        for r in readings:
            msg = humidity_alert(r)
            if msg:
                print(f"    {msg}")

    # 3. Write a report via context manager
    with report_file(report_path) as out:
        out.write("Sensor: temp_north\n")
        with source.open_stream("temp_north") as readings:
            for r in readings:
                out.write(f"  t={r.timestamp:2d}  value={r.value:.1f}\n")

    print(f"\n05| Report written to {report_path}")


if __name__ == "__main__":
    main()
