# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Butterfly Hops - Part 1'

Topics
  - compositions
"""

from typing import Type

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods
# pylint: disable=too-many-arguments, too-many-positional-arguments, invalid-name


def id_hex(obj):
    return hex(id(obj))[-4:]

def extract_class_names(cls: Type[object]):
    return [item.__name__ for item in cls.__mro__]

def assertEqual(first, second):
    if first != second:
        raise AssertionError(f"{first} != {second}")


class Cabin:
    def __init__(self, seats):
        self.seats = seats
        print(f" a| - {self}")

    def __str__(self):
        return f"cabin{{seats={self.seats}|id={id_hex(self)}}}"


class Engine:
    def __init__(self, max_speed):
        self.max_speed = max_speed
        print(f" b| - {self}")

    def __str__(self):
        return f"engine{{max_speed={self.max_speed}|id={id_hex(self)}}}"


class Car:
    def __init__(self, wheels, max_speed_car, cabin=None, seats=None):
        self.cabin = cabin if cabin is not None else Cabin(seats if seats is not None else 1)
        self.wheels = wheels
        self.engine_car = Engine(max_speed_car)
        print(f" c| - {self}")

    def __str__(self):
        return f"car{{wheels={self.wheels},{self.engine_car},{self.cabin}}}"


class Boat:
    def __init__(self, hovercraft, max_speed_boat, cabin=None, seats=None):
        self.cabin = cabin if cabin is not None else Cabin(seats if seats is not None else 1)
        self.hovercraft = hovercraft
        self.engine_boat = Engine(max_speed_boat)
        print(f" d| - {self}")

    def __str__(self):
        return f"boat{{hovercraft={self.hovercraft},{self.engine_boat},{self.cabin}}} "


class Amphibian:
    def __init__(self, seats, max_speed_car, max_speed_boat, wheels, hovercraft):
        self._cabin = Cabin(seats)
        self.car = Car(wheels=wheels, max_speed_car=max_speed_car, cabin=self._cabin)
        self.boat = Boat(hovercraft=hovercraft, max_speed_boat=max_speed_boat, cabin=self._cabin)
        print(f" e| - {self}")

    @property
    def cabin(self): return self._cabin

    def __str__(self):
        return f"amphibian{{{self.car},{self.boat}}}"


def test_car():
    print(f"\n 1| {extract_class_names(Car)}")
    car = Car(seats=3, max_speed_car=350, wheels=4)

    assertEqual(car.cabin.seats, 3)
    assertEqual(car.engine_car.max_speed, 350)
    assertEqual(car.wheels, 4)

def test_boat():
    print(f"\n 2| {extract_class_names(Boat)}")
    boat = Boat(seats=2, max_speed_boat=75, hovercraft=True)

    assertEqual(boat.cabin.seats, 2)
    assertEqual(boat.engine_boat.max_speed, 75)
    assertEqual(boat.hovercraft, True)

def test_amphibian():
    print(f"\n 3| {extract_class_names(Amphibian)}")
    amphibian = Amphibian(seats=4, max_speed_car=250, max_speed_boat=50, wheels=4, hovercraft=True)

    assertEqual(amphibian.cabin.seats, 4)
    assertEqual(amphibian.car.engine_car.max_speed, 250)
    assertEqual(amphibian.car.wheels, 4)
    assertEqual(amphibian.boat.engine_boat.max_speed, 50)
    assertEqual(amphibian.boat.hovercraft, True)

    assertEqual(id(amphibian.car.cabin)==id(amphibian.boat.cabin),True)
    assertEqual(id(amphibian.car.engine_car)==id(amphibian.boat.engine_boat),False)

if __name__ == "__main__":
    test_car()
    test_boat()
    test_amphibian()
