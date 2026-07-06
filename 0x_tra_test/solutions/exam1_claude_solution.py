# exam_000000_Claude.py
# Name: Claude, MatrNr: 000000
# (test-run solution to exam1.md, written independently from the task text)

import functools
import random
import threading
import time
from abc import ABC
from typing import Protocol

# ------------------------------------------------------------------ A1

# A1.a
class PasswordPolicy(Protocol):
    def is_valid(self, password: str) -> bool:
        ...

    @staticmethod
    def name() -> str:
        ...


# A1.b
class PolicyBase(ABC):
    def __init__(self, data: tuple):
        """A leading underscore marks an attribute as internal ('protected'
        by convention): it is not part of the public API, tools and linters
        respect that, but the language does not enforce it."""
        self._data = data


# A1.c, A1.d, A1.e
class PolicyNSA(PolicyBase):
    def __init__(self, min_count: int, max_count: int, letter: str):
        super().__init__((min_count, max_count, letter))

    @property
    def min_count(self) -> int:
        return self._data[0]

    @property
    def max_count(self) -> int:
        return self._data[1]

    @property
    def letter(self) -> str:
        return self._data[2]

    def is_valid(self, password: str) -> bool:
        return self.min_count <= password.count(self.letter) <= self.max_count

    @staticmethod
    def name() -> str:
        return "NSA"


class PolicyMAD(PolicyBase):
    def __init__(self, pos1: int, pos2: int, letter: str):
        super().__init__((pos1, pos2, letter))

    @property
    def pos1(self) -> int:
        return self._data[0]

    @property
    def pos2(self) -> int:
        return self._data[1]

    @property
    def letter(self) -> str:
        return self._data[2]

    def is_valid(self, password: str) -> bool:
        # 'exactly once' at the two 1-based positions -> XOR
        return (password[self.pos1 - 1] == self.letter) != (password[self.pos2 - 1] == self.letter)

    @staticmethod
    def name() -> str:
        return "MAD"


# A1.f
class PasswordEntry:
    def __init__(self, policy: PasswordPolicy, password: str):
        self.policy = policy
        self.password = password

    @classmethod
    def from_string(cls, line: str, policy_type: type) -> "PasswordEntry":  # typing.Self needs 3.11+
        # guaranteed format: "Zahl1-Zahl2 Buchstabe: Passwort", e.g. "1-3 a: abcde"
        numbers, letter_colon, password = line.split()
        num1, num2 = (int(part) for part in numbers.split('-'))
        policy = policy_type(num1, num2, letter_colon.rstrip(':'))
        return cls(policy, password)


# A1.g
class PasswordValidator:
    def __init__(self, lines: list[str], policy_type: type):
        self.entries = [PasswordEntry.from_string(line, policy_type)
                        for line in lines if line.strip()]

    def count_valid_passwords(self) -> int:
        return sum(entry.policy.is_valid(entry.password) for entry in self.entries)


# A1.h
def solve():
    data = """
    1-3 a: abcde
    1-3 b: cdefg
    2-11 c: cccccccccccd
    """
    lines = data.splitlines()

    # A1.e test
    policy = PolicyNSA(1, 3, 'a')
    print(f"{policy.name()=}, {policy.min_count=}, {policy.max_count=}, "
          f"{policy.letter=}, {policy.is_valid('abcde')=}")

    # A1.f test
    entry = PasswordEntry.from_string("1-3 a: abcde", PolicyNSA)
    print(f"{entry.password=}, {entry.policy.is_valid(entry.password)=}")

    # A1.h
    for policy_type in (PolicyNSA, PolicyMAD):
        validator = PasswordValidator(lines, policy_type)
        print(f"{policy_type.name()}: valid passwords = {validator.count_valid_passwords()}")


# ------------------------------------------------------------------ A2

# A2.a
def sensor_a(n: int):
    for _ in range(n):
        yield 'a', random.randint(0, 100)


# A2.c
def profiler_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # wrapper is itself a generator: the clock starts at the first value
        start = time.time()
        yield from func(*args, **kwargs)
        print(f"dt: {time.time() - start} s")
    return wrapper


@profiler_decorator
def sensor_b(n: int):
    for _ in range(n):
        yield 'b', random.randint(0, 100)


# A2.e
class MeasuredRegion:
    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dt = time.time() - self.t0
        print(f"dt: {self.dt} s")
        return False


# A2.f — copy of sensor_a, extended for shared logging across threads
def sensor_c(n: int, log_numbers: list, lock: threading.Lock):
    for _ in range(n):
        item = ('a', random.randint(0, 100))
        with lock:                # critical region kept as small as possible
            log_numbers.append(item)
        yield item


def sensors():
    # A2.b
    random.seed(0)
    n = 10
    numbers_a = list(sensor_a(n))
    print(f"{numbers_a[:5]}")

    # A2.c
    numbers_b = list(sensor_b(n))
    print(f"{numbers_b[:5]}")

    # A2.d
    values = [('a', 23), ('a', 28), ('a', 42), ('b', 48), ('b', 45), ('c', 25)]

    def filter_data(vals, limiter):
        return {sensor: hits for sensor in {s for s, _ in vals}
                if (hits := [(s, v) for s, v in vals if s == sensor and limiter(v)])}

    print(filter_data(values, lambda v: 10 <= v <= 30))

    # A2.e
    with MeasuredRegion():
        _ = list(sensor_a(100_000))

    # A2.f
    log_numbers = []
    lock = threading.Lock()
    results = [[], []]
    threads = [threading.Thread(target=lambda out=out: out.extend(sensor_c(n, log_numbers, lock)))
               for out in results]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"thread 1: {results[0][:5]}")
    print(f"thread 2: {results[1][:5]}")
    print(f"{len(log_numbers)=} (expected {2 * n})")


if __name__ == "__main__":
    solve()
    sensors()
