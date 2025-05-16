# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is a _first_ introduction to Python's match statement..

Teaching focus
  - match
"""

from enum import Enum, auto
from dataclasses import dataclass


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


def classical_switch():                     # match like a switch
    """ classical_switch """
    print("\nclassical_switch\n================")

    print(f" 1| switch-case-structure: color:", end='')
    color = Color.GREEN
    match color:
        case Color.RED:
            print("red")
        case Color.GREEN:
            print("green")
        case Color.BLUE:
            print("blue")


def command_example():                      # match with structure
    """ command_example """
    print("\ncommand_example\n===============")

    match "look here".split():              # try "look", "look here !" etc
        case [action]:
            print(f" 1| split: '{action}'")
        case [action, obj]:
            print(f" 2| split: '{action}', '{obj}'")
        case _:                             # default or wildcard
            print(f" 3| unknown")

    match "run S".split():                  # try other cases
        case ["quit"]:
            print(f" 4| quit")
        case ["look"]:
            print(f" 5| look")
        case ["get", obj]:                  # 'structure' and binding
            print(f" 6| get obj='{obj}'")
        case ["drop", *objs]:               # multiple objs
            print(f" 7| drop objs='{objs}'")
        case ["north"] | ["go", "north"]:   # OR pattern
            print(f" 8| north")
        case ["go", ("east" | "west") as direction]:    # sub-patterns, with binding
            print(f" 9| go direction={direction}")
        case ["run", direction] if direction in ["N", "S"]: # with condition
            print(f"10| run direction={direction}")
        case ["run", _]:
            print(f"11| run unknown direction")

    match {'index': 1, 'name': "Ben"}:                  # try; extra keys in the subject will be ignored
        case {"index": index, "name": name}:            # keys need to be literals
            print(f"12| index={index}, name='{name}'")
        case {"sleep": duration}:
            print(f"13| sleep={duration}")
        case {"text": str() as message}:                # check for types
            print(f"14| text={message}")

    @dataclass
    class Point:
        x: int
        y: int

    point = Point(0, 1)
    match point:                            # match with type and value
        case Point(x=0, y=0):
            print(f"15| origin")
        case Point(x=0, y=y):
            print(f"16| y={y}")
        case Point(x=x, y=0):
            print(f"17| x={x}")
        case Point():
            print("18| somewhere")
        case _:
            print("19| not a point")


class Formatter:
    ...


class JsonFormatter(Formatter):
    ...


class XmlFormatter(Formatter):
    ...


def from_chat(text: str | None = None, force_json: bool = False, force_xml: bool = False) -> Formatter | None:
    # Classical! Implement a matching variation in the 'Eastern Rye' task.
    if force_json or "json" in text:
        return JsonFormatter()
    elif force_xml or "xml" in text:
        return XmlFormatter()
    else:
        return None


def formatter_example():
    """ command_example """
    print("\nformatter_example\n=================")

    # the 'Eastern Rye' task provides unit tests for this
    print()
    print(f" 1| None? {from_chat('Lorem Ipsum')}")
    print(f" 2| json? {from_chat('Lorem json Ipsum')}")
    print(f" 3| json? {from_chat('Lorem Ipsum', force_json=True)}")
    print(f" 4| None? {from_chat('Lorem json', force_json=True, force_xml=True)}")
    print(f" 5| xml? {from_chat('Lorem xml Ipsum')}")
    print(f" 6| xml? {from_chat('Lorem Ipsum', force_xml=True)}")
    print(f" 7| None? {from_chat('Lorem xml', force_xml=True, force_json=True)}")


def main():
    classical_switch()
    command_example()
    formatter_example()


if __name__ == "__main__":
    main()

"""
match with structure
From https://peps.python.org/pep-0636/
    match 'subject', e.g. [action, obj]
      - Verify that the subject has certain structure. In your case, the [action, obj] pattern matches any sequence of 
        exactly two elements. This is called matching.
      - It will bind some names in the pattern to component elements of your subject. In this case, if the list has 
        two elements, it will bind action = subject[0] and obj = subject[1].
    If there’s no match, nothing happens and the statement after match is executed next.

match with type and value
  - A match is valid if the type and values match.

The topic is not that easy. You can imagine that because of the number of PEPs: 
PEP 634 – Structural Pattern Matching: Specification
    https://peps.python.org/pep-0634
PEP 635 – Structural Pattern Matching: Motivation and Rationale
    https://peps.python.org/pep-0635
PEP 636 – Structural Pattern Matching: Tutorial
    https://peps.python.org/pep-0636
"""
