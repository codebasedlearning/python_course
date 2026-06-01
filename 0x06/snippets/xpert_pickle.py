# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about Python's pickle module for object serialization.

Teaching focus
  - pickle.dumps / pickle.loads (binary serialization)
  - pickling custom objects
  - security risks (arbitrary code execution!)
  - pickle vs json: when to use which

pickle
  - pickle serializes Python objects into a byte stream and back.
  - Unlike json, pickle can handle almost any Python object: classes,
    functions, nested structures, circular references.
  - DANGER: unpickling untrusted data can execute arbitrary code.
    Never unpickle data from an untrusted source.

See also
  https://docs.python.org/3/library/pickle.html
  https://owasp.org/www-project-web-security-testing-guide/
"""

import pickle
import tempfile
import os

from utils import print_function_header


"""
Topic: Basic pickling
"""


@print_function_header
def basic_pickling():
    """ serialize and deserialize Python objects """

    # pickle works with bytes, not strings
    data = {"name": "Alice", "scores": [95, 87, 92], "active": True}
    pickled = pickle.dumps(data)
    print(f" 1| pickled type: {type(pickled)}, size: {len(pickled)} bytes")
    print(f" 2| first 40 bytes: {pickled[:40]}")

    restored = pickle.loads(pickled)        # noqa: S301 — educational use
    print(f" 3| restored: {restored}")
    print(f" 4| equal? {data == restored}")

    # pickle handles types that json cannot
    mixed = {
        "tuple": (1, 2, 3),                 # stays a tuple (json: becomes list)
        "set": {4, 5, 6},                   # stays a set (json: TypeError)
        "bytes": b"hello",                  # binary data (json: TypeError)
        "complex": 3 + 4j,                  # complex numbers
    }
    restored_mixed = pickle.loads(pickle.dumps(mixed))  # noqa: S301
    print(f" 5| tuple type preserved: {type(restored_mixed['tuple'])}")
    print(f" 6| set type preserved: {type(restored_mixed['set'])}")


"""
Topic: Pickling custom objects
"""


class Sensor:
    def __init__(self, name, readings):
        self.name = name
        self.readings = readings

    def average(self):
        return sum(self.readings) / len(self.readings)

    def __repr__(self):
        return f"Sensor({self.name!r}, readings={len(self.readings)})"


@print_function_header
def pickling_custom_objects():
    """ pickle handles custom classes automatically """

    sensor = Sensor("temp-01", [20.1, 20.5, 19.8, 21.0])
    print(f" 1| original: {sensor}, avg={sensor.average():.1f}")

    # round-trip
    data = pickle.dumps(sensor)
    restored = pickle.loads(data)           # noqa: S301
    print(f" 2| restored: {restored}, avg={restored.average():.1f}")

    # file I/O with pickle
    path = os.path.join(tempfile.gettempdir(), "sensor.pkl")
    with open(path, "wb") as f:             # binary mode!
        pickle.dump(sensor, f)

    with open(path, "rb") as f:
        from_file = pickle.load(f)          # noqa: S301
    print(f" 3| from file: {from_file}")

    os.remove(path)


"""
Topic: Security risks
"""


@print_function_header
def pickle_security():
    """ why you should NEVER unpickle untrusted data """

    # pickle can execute arbitrary code during deserialization.
    # the __reduce__ method controls how an object is reconstructed:

    class HarmlessLooking:
        def __reduce__(self):
            # this runs os.system("echo hacked!") when unpickled
            return (print, ("DANGER: this ran during unpickle!",))

    malicious_bytes = pickle.dumps(HarmlessLooking())
    print(f" 1| pickled {len(malicious_bytes)} bytes of 'HarmlessLooking'")

    # unpickling executes the code:
    pickle.loads(malicious_bytes)           # noqa: S301
    # in a real attack, this could be: os.system("rm -rf /")

    print(f" 2| lesson: an attacker controls __reduce__")
    print(f" 3| rule: NEVER unpickle data from the network, a file you")
    print(f"    didn't create, or any untrusted source")
    print(f" 4| alternative: use json for data exchange (safe, portable)")


"""
Topic: pickle vs json
"""


@print_function_header
def pickle_vs_json():
    """ when to use which """

    print(f" 1| pickle: binary, Python-only, handles any object, UNSAFE")
    print(f" 2| json:   text, cross-language, basic types only, safe")
    print()
    print(f" 3| use pickle for:")
    print(f"    - caching computed results locally")
    print(f"    - saving/loading ML models (sklearn, etc.)")
    print(f"    - temporary serialization within your own code")
    print()
    print(f" 4| use json for:")
    print(f"    - API communication")
    print(f"    - config files")
    print(f"    - any data exchange with external systems")
    print(f"    - anything a human might read")


if __name__ == "__main__":
    basic_pickling()
    pickling_custom_objects()
    pickle_security()
    pickle_vs_json()
