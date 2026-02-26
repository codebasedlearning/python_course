# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 2 (Unit 0x02)

Multiple sensors, stored as dicts of lists.
Refactored from Part 1: comprehensions replace verbose loops.
"""


# --- Multi-sensor data ---

SENSORS = {
    "temp_north": [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6],
    "temp_south": [21.0, 20.5, 22.3, 21.8, 23.1, 22.0, 21.5, 20.9, 21.2, 22.7],
    "humidity":   [65.0, 68.2, 70.1, 72.5, 69.0, 67.3, 71.8, 74.0, 66.5, 63.9],
    "water_lvl":  [1.2, 1.3, 1.1, 1.5, 2.8, 1.4, 1.2, 1.3, 1.6, 1.1],
}


def average(data):
    return sum(data) / len(data) if data else 0.0


def detect_spikes(data, threshold=5.0):
    return [i for i in range(1, len(data)) if abs(data[i] - data[i - 1]) > threshold]


def filter_by_range(data, low, high):
    """Return only values within [low, high]."""
    return [v for v in data if low <= v <= high]


def per_sensor_stats(sensors):
    """Compute stats per sensor using comprehensions."""
    return {
        name: {
            "count": len(readings),
            "avg": average(readings),
            "min": min(readings),
            "max": max(readings),
            "spikes": detect_spikes(readings),
        }
        for name, readings in sensors.items()
    }


def sorted_by_average(sensors):
    """Return sensor names sorted by average reading, descending."""
    averages = {name: average(readings) for name, readings in sensors.items()}
    return sorted(averages, key=averages.get, reverse=True)


def main():
    stats = per_sensor_stats(SENSORS)
    for name, s in stats.items():
        print(f"01| {name:12s}  avg={s['avg']:6.2f}  min={s['min']:6.2f}  "
              f"max={s['max']:6.2f}  spikes={s['spikes']}")

    print()
    ranking = sorted_by_average(SENSORS)
    print(f"02| Sensors by avg (desc): {ranking}")

    print()
    normal_temps = filter_by_range(SENSORS["temp_north"], 17.0, 25.0)
    print(f"03| temp_north in [17, 25]: {normal_temps}")
    print(f"    filtered out {len(SENSORS['temp_north']) - len(normal_temps)} outlier(s)")


if __name__ == "__main__":
    main()
