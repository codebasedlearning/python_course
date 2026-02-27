# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet introduces basic testing with `pytest`.

Teaching focus
  - Testing is not an afterthought; it is part of writing code. The earlier you
    start, the fewer bugs survive into the next unit.
  - We keep it minimal here: run a few tests, see green/red, understand why.
    Unit 0x08 will revisit testing in depth.

Summary

Topics
  - assert statements
  - pytest basics (discovery, naming, running)
  - testing pure functions from previous tasks
  - boundary and error cases

Why test early?
  - A function without a test is a function you *hope* works.
  - Writing a test forces you to think about inputs, outputs, and edge cases
    *before* you move on.
  - pytest discovers any function whose name starts with `test_` in any file
    whose name starts with `test_` — no boilerplate required.

Running tests
  - From the project root:
        uv run pytest 0x02/snippets/study_testing.py -v
  - Or, to run a single test:
        uv run pytest 0x02/snippets/study_testing.py::test_counter_add_banana -v

See also
  - https://docs.pytest.org/en/stable/getting-started.html
  - https://docs.python.org/3/library/unittest.html
"""

from typing import TypeVar

T = TypeVar("T")

# ---------------------------------------------------------------------------
# Functions under test (copied from 0x01 solutions for self-containment)
# In your own code, you would import from your solution module instead.
# ---------------------------------------------------------------------------

def counter_add(counter: dict, item):
    """Increments the count of an item in the provided counter dictionary."""
    counter[item] = counter.get(item, 0) + 1


def counter_sub(counter: dict, item):
    """Decrements the count of an item in the provided counter dictionary."""
    if (count := counter.get(item, 0)) > 1:
        counter[item] = count - 1
    elif item in counter:
        del counter[item]


def counter_most_common[T](counter: dict[T, int]) -> T | None:
    """Returns the key of the most common item in the provided counter dictionary."""
    if not counter:
        return None
    return max(counter.items(), key=lambda kv: kv[1])[0]
    # return max(counter, key=counter.get)


def fib_itr(n: int) -> int:
    """Iterative Fibonacci function."""
    if n == 0:
        return 0
    n1, n2 = 0, 1
    for _ in range(n - 1):
        n1, n2 = n2, n1 + n2
    return n2


# ---------------------------------------------------------------------------
# Part 1 — plain assert (no framework needed)
# ---------------------------------------------------------------------------
# The simplest test is a bare `assert`. It fails with AssertionError if the
# condition is False. Good for quick sanity checks, but the error messages
# are not very informative.

def demo_plain_assert():
    """Show that plain assert works but gives poor diagnostics."""
    assert fib_itr(0) == 0
    assert fib_itr(1) == 1
    assert fib_itr(10) == 55
    print(" 1| plain asserts passed (no output on success — that's the point)")

    # Uncomment to see what a failure looks like:
    # assert fib_itr(10) == 56, "expected 56 but Fibonacci disagrees"


# ---------------------------------------------------------------------------
# Part 2 — pytest: just name your function test_* and you are done
# ---------------------------------------------------------------------------
# pytest discovers functions named test_* in files named test_* (or here,
# because we run the file explicitly). Each function is one test case.
# A test passes if it finishes without raising an exception.

def test_fib_known_values():
    """Fibonacci: check the first few values against a known sequence."""
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    for n, want in enumerate(expected):
        assert fib_itr(n) == want, f"fib_itr({n}) should be {want}"


def test_fib_large():
    """Fibonacci: make sure the iterative version handles larger n."""
    assert fib_itr(50) == 12586269025


def test_counter_add_banana():
    """Counter: adding all chars of 'banana' should give {'b':1, 'a':3, 'n':2}."""
    c: dict = {}
    for ch in "banana":
        counter_add(c, ch)
    assert c == {"b": 1, "a": 3, "n": 2}


def test_counter_sub_removes_at_zero():
    """Counter: subtracting the last occurrence should remove the key entirely."""
    c = {"x": 1}
    counter_sub(c, "x")
    assert "x" not in c, "key should be gone when count reaches zero"


def test_counter_sub_nonexistent():
    """Counter: subtracting a key that was never added should not crash."""
    c: dict = {}
    counter_sub(c, "ghost")       # should be a no-op
    assert c == {}


def test_counter_most_common_empty():
    """Counter: most_common on an empty dict should return None, not crash."""
    assert counter_most_common({}) is None


def test_counter_most_common_tie():
    """Counter: when counts are tied, any winner is acceptable."""
    c = {"a": 3, "b": 3}
    result = counter_most_common(c)
    assert result in ("a", "b"), f"expected 'a' or 'b', got {result!r}"


# ---------------------------------------------------------------------------
# Part 3 — testing for expected exceptions with pytest.raises
# ---------------------------------------------------------------------------

def to_positive_int(text: str) -> int:
    """Convert text to a positive integer or raise ValueError."""
    n = int(text)
    if n <= 0:
        raise ValueError(f"expected positive, got {n}")
    return n


def test_to_positive_int_valid():
    assert to_positive_int("42") == 42


def test_to_positive_int_rejects_negative():
    import pytest
    with pytest.raises(ValueError):
        to_positive_int("-5")


def test_to_positive_int_rejects_garbage():
    import pytest
    with pytest.raises(ValueError):
        to_positive_int("abc")


# ---------------------------------------------------------------------------
# main — run the plain-assert demo; pytest handles the rest
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo_plain_assert()

    print(" 2| To run all tests, execute:")
    print("      uv run pytest 0x02/snippets/study_testing.py -v")
    print(" 3| Green lines = passed, red lines = failed. That's it.")
