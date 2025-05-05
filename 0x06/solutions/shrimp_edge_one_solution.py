# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Shrimp Edge'

Topics
  - Protocol
  - runtime_checkable
"""

from typing import Protocol, runtime_checkable

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods


class User:
    def __init__(self, name):
        self.name = name
    def log_message(self): return f"User: {self.name}"

class Server:
    def __init__(self, ip):
        self.ip = ip
    def log_message(self): return f"Server IP: {self.ip}"

class Rock:
    pass


def part1():
    print("\npart1\n=====")

    def log(obj):
        print(f" 1| - {obj.log_message()}")

    log(User("Alice"))
    log(Server("192.168.0.1"))
    try:
        log(Rock())
    except AttributeError:
        print(" 2| - AttributeError")


def part2():
    print("\npart2\n=====")

    class Loggable(Protocol):
        def log_message(self) -> str: ...

    def log(obj: Loggable):
        print(f" 1| - {obj.log_message()}")

    log(User("Alice"))
    log(Server("192.168.0.1"))
    try:
        log(Rock())                         # mypy: incompatible type
    except AttributeError:
        print(" 2| - AttributeError")


def part3():
    print("\npart3 / Optional\n================")

    @runtime_checkable
    class Loggable(Protocol):
        def log_message(self) -> str: ...

    def log(obj: Loggable):
        if not isinstance(obj, Loggable):
            raise TypeError("Object does not implement log_message()")
        print(f" 1| - {obj.log_message()}")

    log(User("Alice"))
    log(Server("192.168.0.1"))
    try:
        log(Rock())                         # mypy: incompatible type
    except TypeError as e:
        print(f" 2| - TypeError: {e}")

if __name__ == '__main__':
    part1()
    part2()
    part3()
