# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Drift Pebble'

Topics
  - __eq__, __hash__
  - __lt__ and total_ordering
  - __add__
  - set/dict usage with custom objects
"""

from functools import total_ordering


@total_ordering
class Vec2:
    """A simple 2D vector supporting equality, hashing, ordering, and addition."""

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def length(self) -> float:
        return (self._x ** 2 + self._y ** 2) ** 0.5

    # --- equality and hashing ---

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2):
            return NotImplemented
        return self._x == other._x and self._y == other._y

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    # --- ordering (total_ordering fills in __gt__, __ge__, __le__) ---

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.length < other.length

    # --- arithmetic ---

    def __add__(self, other: "Vec2") -> "Vec2":
        if not isinstance(other, Vec2):
            return NotImplemented
        return Vec2(self._x + other._x, self._y + other._y)

    def __repr__(self) -> str:
        return f"Vec2({self._x}, {self._y})"


def solve():
    a = Vec2(1, 0)
    b = Vec2(0, 1)
    c = Vec2(1, 0)

    # Part 1: equality
    print(f" 1| {a == c = }")          # True  — same components
    print(f" 2| {a == b = }")          # False — different components
    print(f" 3| {a is c = }")          # False — different objects

    # Part 2: hashing — usable as dict key / set element
    vectors = {a, b, c}
    print(f" 4| {vectors = }")         # {Vec2(1, 0), Vec2(0, 1)} — c deduped
    print(f" 5| {len(vectors) = }")    # 2

    counts = {a: 1, b: 2}
    counts[c] = counts.get(c, 0) + 10
    print(f" 6| {counts = }")          # {Vec2(1, 0): 11, Vec2(0, 1): 2}

    # Part 3: ordering
    d = Vec2(3, 4)                     # length 5
    print(f" 7| {a < d = }")           # True  — length 1 < 5
    print(f" 8| {a >= c = }")          # True  — length 1 >= 1

    bag = [Vec2(3, 4), Vec2(1, 0), Vec2(0, 2), Vec2(1, 1)]
    print(f" 9| {sorted(bag) = }")

    # Part 4: addition
    s = a + b
    print(f"10| {a + b = }")           # Vec2(1, 1)
    print(f"11| {a + b + d = }")       # Vec2(4, 5)


if __name__ == "__main__":
    solve()
