# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses inheritance vs. composition.

Teaching focus
  - inheritance vs. composition
  - see https://realpython.com/inheritance-composition-python
"""

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods

from utils import print_function_header


class Vehicle:
    def __init__(self, name):
        self.name = name

    def drive(self):
        return " a| - Driving... what ever"


# Car 'is a' Vehicle
class Car(Vehicle):
    def drive(self):
        return " b| - Driving a car"


# Bike 'is a' Vehicle
class Bike(Vehicle):
    def drive(self):
        return " c| - Riding a bike"


@print_function_header
def show_inheritance():

    print(" 1| inheritance")
    for v in [Vehicle("Vehicle"), Car("Car"), Bike("Bike")]:
        print(v.drive())


class Engine:
    def __init__(self, power):
        self.power = power

    def start(self):
        return f"Generic Engine ({self.power})"

class VolvoPenta(Engine):
    def start(self):
        return f"Volvo Penta engine ({self.power})"


class Boat:
    def __init__(self, name: str, engine: Engine):       # inject engine
        self.name = name
        self.engine = engine

    def drive(self):
        return " a| - Driving a boat with " + self.engine.start()


@print_function_header
def show_composite():

    print(" 2| composite")
    engine = VolvoPenta("V8")
    boat = Boat("Boat", engine)
    print(boat.drive())


if __name__ == "__main__":
    show_inheritance()
    show_composite()
