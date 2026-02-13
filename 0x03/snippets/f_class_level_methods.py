# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses class level methods.

Teaching focus
  - use cases for class level methods
  - factory methods as alternative constructors

Static Methods
  - `celsius_to_fahrenheit` and `fahrenheit_to_celsius` convert temperature
    values but don't depend on any class or instance.
  - These are utility methods grouped logically within the `Temperature` class.
  - Use `@staticmethod` for utility/helper methods that don't need class or
    instance context (e.g., mathematical functions, converters, etc.).

Class Methods
  - `from_celsius` creates a `Temperature` instance using Celsius instead
    of Fahrenheit.
  - It uses the `cls` parameter to create the class instance and calls the
    static method `celsius_to_fahrenheit` for conversion.
  - Use `@classmethod` for methods that need class-level context (e.g.,
    factory methods, altering class variables, polymorphic behavior).
  - If you replace `cls` with the hard-coded class name (`Temperature`),
    the method will always use `Temperature` for instantiation, even when
    invoked from a subclass. This breaks the principle of polymorphism and
    can lead to incorrect behavior in multiple inheritance scenarios.

Factory methods
  - A common pattern is providing multiple @classmethod constructors for
    different input formats (from_string, from_dict, from_json, etc.).
  - This avoids overloading __init__ with complex conditional logic and
    makes the code more readable and explicit.

See also
  - https://docs.python.org/3/library/functions.html
  - https://de.wikipedia.org/wiki/Grad_Celsius
"""

from typing import Self  # from Python 3.11

from utils import print_function_header

"""
Topic: Static and class methods
"""


class Temperature:
    """ temperature class with class level methods """
    def __init__(self, fahrenheit: float) -> None:
        self.fahrenheit = fahrenheit

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """ converts Celsius to Fahrenheit """
        return celsius * 9 / 5 + 32

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """ converts Fahrenheit to Celsius """
        return (fahrenheit - 32) * 5 / 9

    @classmethod
    def from_celsius(cls, celsius: float) -> Self:     # Temperature not defined yet
        """ factory method to create Temperature instance from Celsius """
        fahrenheit = cls.celsius_to_fahrenheit(celsius)
        return cls(fahrenheit)

    def __str__(self):
        return f"{self.fahrenheit}°F"


class OptimizedTemperature(Temperature):
    pass                                    # a nop


@print_function_header
def show_class_level_functions():
    """ show class level functions """

    # using static methods for conversion
    freeze_c = 0
    freeze_f = Temperature.celsius_to_fahrenheit(freeze_c)
    body_f = 98.6
    body_c = Temperature.fahrenheit_to_celsius(body_f)
    print(f" 1| Freeze: {freeze_c}°C={freeze_f}°F")
    print(f" 2| Body:   {body_f}°F={body_c}°C")

    # using class method to create an instance from Celsius
    boil_f = Temperature.from_celsius(100)
    print(f" 3| Boil:   {boil_f}, {boil_f.__dict__}")
    print(f" 4| {Temperature.__dict__=}")

    # note the type
    boil_opt = OptimizedTemperature.from_celsius(100)
    print(f" 5| {boil_opt}, {type(boil_opt)=}")


"""
Topic: Factory methods
"""


class Color:
    """ color class with multiple factory methods """
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def from_hex(cls, hex_str: str) -> Self:
        """ create Color from hex string like '#FF8800' """
        hex_str = hex_str.lstrip('#')
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return cls(r, g, b)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """ create Color from a dictionary """
        return cls(r=data['r'], g=data['g'], b=data['b'])

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"


@print_function_header
def show_factory_methods():
    """ multiple ways to create instances """

    c1 = Color(255, 136, 0)
    c2 = Color.from_hex("#FF8800")
    c3 = Color.from_dict({'r': 255, 'g': 136, 'b': 0})

    print(f" 1| direct:    {c1=}")
    print(f" 2| from_hex:  {c2=}")
    print(f" 3| from_dict: {c3=}")
    print(f" 4| {(c1.r == c2.r == c3.r)=}")


if __name__ == '__main__':
    # Static and class methods
    show_class_level_functions()

    # Factory methods
    show_factory_methods()
