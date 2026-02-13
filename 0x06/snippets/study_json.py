# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about JSON serialization and deserialization.

Teaching focus
  - json.dumps and json.loads
  - pretty printing with indent
  - custom serialization (default= parameter)
  - dataclass round-tripping
  - common gotchas (datetime, set, tuple)

json
  - JSON (JavaScript Object Notation) is the lingua franca of data exchange.
  - Python's json module handles the conversion between Python objects and
    JSON strings.
  - Only basic types are directly serializable: dict, list, str, int, float,
    bool, None. Everything else needs a custom serializer.

See also
  https://docs.python.org/3/library/json.html
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime, date

from utils import print_function_header


"""
Topic: Basic serialization
"""


@print_function_header
def basic_json():
    """ dumps and loads: the core operations """

    data = {
        "name": "Alice",
        "age": 30,
        "scores": [95, 87, 92],
        "active": True,
        "address": None,
    }

    # serialize: Python dict → JSON string
    json_str = json.dumps(data)
    print(f" 1| json string: {json_str}")
    print(f" 2| type: {type(json_str)}")

    # deserialize: JSON string → Python dict
    restored = json.loads(json_str)
    print(f" 3| restored: {restored}")
    print(f" 4| type: {type(restored)}")

    # pretty printing
    pretty = json.dumps(data, indent=2)
    print(f" 5| pretty:\n{pretty}")

    # sort keys for deterministic output (useful for diffs/tests)
    sorted_str = json.dumps(data, indent=2, sort_keys=True)
    print(f" 6| sorted keys:\n{sorted_str}")


"""
Topic: Custom serialization
"""


@print_function_header
def custom_serialization():
    """ handling types that json doesn't know about """

    data = {
        "event": "meeting",
        "date": date(2025, 6, 15),
        "timestamp": datetime(2025, 6, 15, 14, 30),
        "attendees": {"Alice", "Bob", "Charlie"},   # set!
        "coords": (52.52, 13.405),          # tuple!
    }

    # this would fail: json.dumps(data) → TypeError

    # solution 1: default= function for unknown types
    def json_default(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, set):
            return sorted(obj)              # convert set → sorted list
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    result = json.dumps(data, default=json_default, indent=2)
    print(f" 1| custom serialized:\n{result}")

    # gotcha: tuples become lists in JSON (JSON has no tuple concept)
    simple = json.dumps({"t": (1, 2, 3)})
    restored = json.loads(simple)
    print(f" 2| tuple→list gotcha: {restored['t']}, type={type(restored['t'])}")


"""
Topic: Dataclass round-tripping
"""


@dataclass
class Student:
    name: str
    grade: float
    courses: list


@print_function_header
def dataclass_json():
    """ dataclass → JSON → dataclass """

    alice = Student(name="Alice", grade=1.3, courses=["Python", "Algorithms"])

    # dataclass → dict → JSON
    json_str = json.dumps(asdict(alice), indent=2)
    print(f" 1| serialized:\n{json_str}")

    # JSON → dict → dataclass
    data = json.loads(json_str)
    restored = Student(**data)              # dict unpacking into constructor
    print(f" 2| restored: {restored}")
    print(f" 3| equal? {alice == restored}")

    # round-trip a list of students
    students = [
        Student("Alice", 1.3, ["Python"]),
        Student("Bob", 2.0, ["Algorithms", "Databases"]),
    ]
    json_list = json.dumps([asdict(s) for s in students])
    restored_list = [Student(**d) for d in json.loads(json_list)]
    print(f" 4| round-tripped {len(restored_list)} students")


"""
Topic: File I/O with json
"""


@print_function_header
def json_file_io():
    """ json.dump and json.load work directly with files """
    import tempfile
    import os

    data = {"language": "Python", "version": 3.12, "typed": True}

    # write to file
    path = os.path.join(tempfile.gettempdir(), "demo.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f" 1| written to {path}")

    # read from file
    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f" 2| loaded: {loaded}")

    # note the naming:
    # json.dumps / json.loads → string (the 's' stands for 'string')
    # json.dump  / json.load  → file

    os.remove(path)
    print(f" 3| cleaned up")


if __name__ == "__main__":
    basic_json()
    custom_serialization()
    dataclass_json()
    json_file_io()
