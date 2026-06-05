# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is a _first_ introduction to Python's match statement..

Teaching focus
  - match

match with structure
From https://peps.python.org/pep-0636/
    match 'subject', e.g. [action, obj]
      - Verify that the subject has certain structure. In your case, the [action, obj] pattern matches any sequence of
        exactly two elements. This is called matching.
      - It will bind some names in the pattern to component elements of your subject. In this case, if the list has
        two elements, it will bind action = subject[0] and obj = subject[1].
    If there's no match, nothing happens and the statement after match is executed next.

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

from dataclasses import dataclass
from enum import Enum, auto

from utils import print_function_header


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


@print_function_header
def classical_switch():                     # match like a switch
    """ classical_switch """

    print(" 1| switch-case-structure: color:", end='')
    color = Color.GREEN
    match color:
        case Color.RED:
            print("red")
        case Color.GREEN:
            print("green")
        case Color.BLUE:
            print("blue")


"""
    Think of a cli-role playing game. The player can enter commands like:
        - look
        - look here
        - run S
"""

@print_function_header
def match_with_structure():
    """ match with structure """

    print(" 1| match structure only")
    for line in ["look", "look here", "oops"]:
        match line.split():
            case [action]:                  # bind name
                print(f" a| - {line=} -> {action=}")
            case [action, info]:            # bind names
                print(f" b| - {line=} -> {action=}, {info=}")
            case _:                         # default or wildcard
                print(f" c| - {line=} -> unknown")

@print_function_header
def match_with_structure_and_value():
    """ match with structure and value """

    print(" 1| match both, value and structure, bind names")
    for line in [
        "quit", "get candy", "drop candy shield",
        "north", "go north", "go east", "go west",
        "run S", "run X",
    ]:
        match line.split():
            case ["quit"]:
                print(f" a| - {line=} -> 'quit'")
            case ["get", obj]:
                print(f" b| - {line=} -> 'get', {obj=}")
            case ["drop", *objs]:                               # multiple objs
                print(f" c| - {line=} -> 'drop', {objs=}")
            case ["north"] | ["go", "north"]:                   # OR pattern
                print(f" d| - {line=} -> 'north'")
            case ["go", ("east" | "west") as direction]:        # sub-patterns, with binding
                print(f" e| - {line=} -> 'go', {direction=}")
            case ["run", direction] if direction in ["N", "S"]: # with condition
                print(f" f| - {line=} -> 'run', {direction=}")
            case ["run", _]:                                    # '_' wildcard, no '_' variable
                print(f" g| - {line=} -> 'run' unknown direction")

@print_function_header
def match_with_content():
    """ match with content """

    print(" 1| match according to content")
    for d in [                              # keys need to be literals
        {"index": 1, "name": "Ben", "city": "Berlin", "sleep": 12},
        {"sleep": 12},
        {"text": 23},                       # not a string
        {"text": "this is a text"},         # a string
    ]:
        match d:
            case {"index": index, "name": name}:                # extra keys will be ignored, first fits
                print(f" a| - {d=} -> {index=}, {name=}")
            case {"sleep": duration}:
                print(f" b| - {d=} -> 'sleep', {duration=}")
            case {"text": str(message)}:                        # check for types, same as str() as message or if isinstance(message, str)
                print(f" c| - {d=} -> 'text', {message=}")

@print_function_header
def match_with_attributes():
    """ match with attributes """

    @dataclass
    class Point:
        x: int
        y: int
        def __repr__(self): return f"({self.x}, {self.y})"

    print(" 1| match according to attributes")
    for point in [
        Point(0, 0),
        Point(0, 1),
        (1,2,3)
    ]:
        match point:
            case Point(x=0, y=0):
                print(f" a| - {point=} -> origin")
            case Point(x=0, y=y):
                print(f" b| - {point=} -> y-axis, {y=}")
            case Point(x=x, y=0):
                print(f" c| - {point=} -> x-axis, {x=}")
            case Point():
                print(f" d| - {point=} -> somewhere")
            case _:
                print(f" e| - {point=} -> not a point")


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


@print_function_header
def formatter_example():
    """ command_example """

    # the 'Eastern Rye' task provides unit tests for this
    print()
    print(f" 1| None? {from_chat('Lorem Ipsum')}")
    print(f" 2| json? {from_chat('Lorem json Ipsum')}")
    print(f" 3| json? {from_chat('Lorem Ipsum', force_json=True)}")
    print(f" 4| None? {from_chat('Lorem json', force_json=True, force_xml=True)}")
    print(f" 5| xml? {from_chat('Lorem xml Ipsum')}")
    print(f" 6| xml? {from_chat('Lorem Ipsum', force_xml=True)}")
    print(f" 7| None? {from_chat('Lorem xml', force_xml=True, force_json=True)}")


if __name__ == "__main__":
    classical_switch()
    match_with_structure()
    match_with_structure_and_value()
    match_with_content()
    match_with_attributes()
    formatter_example()
