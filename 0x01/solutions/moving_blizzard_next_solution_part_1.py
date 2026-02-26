# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Project 'Moving Blizzard' — Part 1 (Unit 0x01)

A coastal research station monitors environmental sensors.
This first version uses plain functions and lists — no classes, no imports.
"""


# --- Sample sensor data (temperature readings in °C) ---

READINGS = [18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6]


def average(data):
    """Return the arithmetic mean of a list of numbers."""
    if not data:
        return 0.0
    total = 0.0
    for value in data:
        total += value
    return total / len(data)


def minimum(data):
    """Return the smallest value in data."""
    if not data:
        return None
    result = data[0]
    for value in data[1:]:
        if value < result:
            result = value
    return result


def maximum(data):
    """Return the largest value in data."""
    if not data:
        return None
    result = data[0]
    for value in data[1:]:
        if value > result:
            result = value
    return result


def detect_spikes(data, threshold=5.0):
    """Return indices where the reading jumps by more than `threshold` from the previous."""
    spikes = []
    for i in range(1, len(data)):
        if abs(data[i] - data[i - 1]) > threshold:
            spikes.append(i)
    return spikes


def summarize(data):
    """Print a summary of the readings."""
    print(f"01| Readings:  {data}")
    print(f"02| Count:     {len(data)}")
    print(f"03| Average:   {average(data):.2f}")
    print(f"04| Min:       {minimum(data)}")
    print(f"05| Max:       {maximum(data)}")
    spikes = detect_spikes(data)
    if spikes:
        print(f"06| Spikes at: {spikes} (indices where jump > 5.0)")
        for i in spikes:
            print(f"    index {i}: {data[i-1]:.1f} -> {data[i]:.1f} "
                  f"(delta {abs(data[i] - data[i-1]):.1f})")
    else:
        print(f"06| No spikes detected.")


def main():
    summarize(READINGS)


if __name__ == "__main__":
    main()
