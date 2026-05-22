# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev
#
# Reference solution for RSA-Task, see 0x05/README.md.

from __future__ import annotations

from collections.abc import Iterable
from typing import Generic, Protocol, Self

# ---------------------------------------------------------------------------
# A1
# ---------------------------------------------------------------------------

# (a)
class EgcdResult:
    """3-tuple (g, s, t) returned by the extended Euclidean algorithm."""

    # (a)
    def __init__(self, g: int, s: int, t: int) -> None:
        self._data: tuple[int, int, int] = (g, s, t)

    # (b)
    @property
    def g(self) -> int: return self._data[0]
    @property
    def s(self) -> int: return self._data[1]
    @property
    def t(self) -> int: return self._data[2]

    # (c)
    def __str__(self) -> str:  return f"({self.g},{self.s},{self.t})"
    def __repr__(self) -> str: return f"EgcdResult(g={self.g}, s={self.s}, t={self.t})"

    # (d)
    @classmethod
    def egcd(cls, a: int, b: int) -> Self:
        if b == 0:
            return cls(a, 1, 0)
        sub = cls.egcd(b, a % b)
        return cls(sub.g, sub.t, sub.s - sub.t * (a // b))

    # (e)
    def __getitem__(self, ab: tuple[int, int]) -> int:
        a, b = ab
        return self.s * a + self.t * b - self.g

# (f)
class EgcdResultGen[T]: # or with T = TypeVar("T") and Generic
    def __init__(self, g: T, s: T, t: T) -> None:
        self._data: tuple[T, T, T] = (g, s, t)
    @property
    def g(self) -> T: return self._data[0]


# ---------------------------------------------------------------------------
# A2
# ---------------------------------------------------------------------------

# (a)
class CryptoText(list[int]):
    """A list of integers representing a cryptographic text."""

    # (a)
    def __init__(self, *args) -> None:
        if len(args) == 0:                                      # empty
            super().__init__()
        elif len(args) == 1 and isinstance(args[0], Iterable):  # list and tuple
            super().__init__(args[0])
        else:
            super().__init__(args)                              # multiple ints

# (b)
class ICryptoSystem(Protocol):
    def encrypt(self, text: CryptoText) -> CryptoText: ...
    def decrypt(self, text: CryptoText) -> CryptoText: ...

# (c)
class RSA:
    def __init__(self, p: int, q: int, e: int, d: int) -> None:
        self.p = p
        self.q = q
        self.e = e
        self.d = d
        self.N = p * q

    # (d) (e)
    def encrypt(self, text: CryptoText) -> CryptoText:
        return CryptoText(pow(m, self.e, self.N) for m in text)

    def decrypt(self, text: CryptoText) -> CryptoText:
        return CryptoText(pow(c, self.d, self.N) for c in text)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def A1() -> None:
    print("\n--A1--\n")
    # (a) (b) (c)
    r = EgcdResult(1, 47, -9)
    print(f" 1| r={r}, {r=}, {r.g=}, {r.s=}, {r.t=}") # (b)

    # (d)
    res = EgcdResult.egcd(23, 120)
    print(f" 2| egcd(23, 120) = {res}")

    # (e)
    print(f" 3| residual res[23, 120] = {res[23, 120]}")


def A2() -> None:
    print("\n--A2--\n")

    # (a)
    print(f" 1| empty:      {CryptoText()}")
    print(f" 2| from int:   {CryptoText(7)}")
    print(f" 3| from_args:  {CryptoText(1, 2, 3)}")
    print(f" 4| from_list:  {CryptoText([23, 42])}")
    print(f" 5| from tuple: {CryptoText((99, 100, 101))}")

    # (d)
    rsa = RSA(p=11, q=13, e=23, d=47)
    c = rsa.encrypt(CryptoText(7,23))
    m = rsa.decrypt(c)
    print(f" 6| RSA encrypt {c=}")
    print(f" 7| RSA decrypt {m=}")


# ---------------------------------------------------------------------------
# main-guard
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    A1()
    A2()
