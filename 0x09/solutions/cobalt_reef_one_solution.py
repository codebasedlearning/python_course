# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Cobalt Reef'

Topics
  - descriptor protocol (__get__, __set__, __delete__)
  - data descriptors vs non-data descriptors
  - reusable validation logic
"""


# Part 1 — Bounded descriptor

class Bounded:
    """A data descriptor that enforces min/max bounds on numeric attributes."""

    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.public_name} must be numeric, got {type(value).__name__}")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"{self.public_name} must be between {self.min_value} and {self.max_value}, got {value}"
            )
        setattr(obj, self.private_name, value)

    def __delete__(self, obj):
        delattr(obj, self.private_name)


# Part 2 — Using the descriptor

class Sensor:
    """A sensor reading with validated temperature and humidity."""

    temperature = Bounded(-40.0, 80.0)
    humidity = Bounded(0.0, 100.0)

    def __init__(self, name: str, temperature: float, humidity: float):
        self.name = name
        self.temperature = temperature     # goes through Bounded.__set__
        self.humidity = humidity

    def __repr__(self) -> str:
        return f"Sensor({self.name!r}, t={self.temperature}, h={self.humidity})"


def test_sensor():
    s = Sensor("outdoor", temperature=22.5, humidity=60.0)
    print(f" 1| {s = }")

    s.temperature = 35.0
    print(f" 2| {s.temperature = }")

    # Boundary tests
    try:
        s.temperature = 100.0
    except ValueError as e:
        print(f" 3| expected: {e}")

    try:
        s.humidity = -5.0
    except ValueError as e:
        print(f" 4| expected: {e}")

    try:
        s.temperature = "warm"
    except TypeError as e:
        print(f" 5| expected: {e}")


# Part 3 — Logged descriptor

class Logged:
    """A data descriptor that logs every get/set access."""

    def __init__(self, default=None):
        self.default = default

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = getattr(obj, self.private_name, self.default)
        print(f"      [LOG] get {self.public_name} -> {value!r}")
        return value

    def __set__(self, obj, value):
        print(f"      [LOG] set {self.public_name} = {value!r}")
        setattr(obj, self.private_name, value)


class Config:
    debug = Logged(default=False)
    language = Logged(default="en")

    def __init__(self, debug: bool = False, language: str = "en"):
        self.debug = debug
        self.language = language


def test_logged():
    print(f" 6| creating Config:")
    cfg = Config(debug=True, language="de")
    print(f" 7| reading back:")
    _ = cfg.debug
    _ = cfg.language


if __name__ == "__main__":
    test_sensor()
    test_logged()
