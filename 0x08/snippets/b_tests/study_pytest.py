# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates pytest — the Python testing framework used in practice.

Teaching focus
  - basic test functions (no class required)
  - assert rewriting (pytest enhances plain assert)
  - @pytest.mark.parametrize for data-driven tests
  - fixtures for setup/teardown
  - pytest.raises for exception testing

pytest vs unittest
  - unittest follows the xUnit pattern (Java-style, class-based).
  - pytest uses plain functions and plain assert — less boilerplate.
  - pytest is the de facto standard in the Python ecosystem.

How to run
  - pip install pytest (or: uv add pytest)
  - pytest study_pytest.py -v
  - pytest study_pytest.py -v -k "test_add"    (run only matching tests)

See also
  https://docs.pytest.org/en/stable/
  https://docs.pytest.org/en/stable/how-to/parametrize.html
"""

import pytest


# ---- The code under test ---- #

def add(a, b):
    """Add two numbers."""
    return a + b

def divide(a, b):
    """Divide a by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

class Stack:
    """A minimal stack implementation."""
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


"""
Topic: Basic test functions
  - test function names must start with 'test_'
  - use plain 'assert' — pytest rewrites them for better error messages
"""


def test_add_integers():
    assert add(2, 3) == 5

def test_add_floats():
    assert add(0.1, 0.2) == pytest.approx(0.3)     # floating point comparison!

def test_add_strings():
    assert add("hello", " world") == "hello world"


"""
Topic: @pytest.mark.parametrize
  - run the same test with different inputs
  - reduces copy-paste test functions
"""


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -50, 50),
    (0.1, 0.2, pytest.approx(0.3)),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected


"""
Topic: Testing exceptions with pytest.raises
"""


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divide(10, 0)

def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError, match="pop from empty"):
        s.pop()


"""
Topic: Fixtures — setup and teardown
  - fixtures provide test dependencies (like setUp/tearDown in unittest)
  - they are injected by name into test function parameters
"""


@pytest.fixture
def empty_stack():
    """Provide a fresh empty stack for each test."""
    return Stack()

@pytest.fixture
def filled_stack():
    """Provide a stack with some items."""
    s = Stack()
    for item in [10, 20, 30]:
        s.push(item)
    return s


def test_push_to_empty(empty_stack):
    empty_stack.push(42)
    assert len(empty_stack) == 1
    assert empty_stack.peek() == 42

def test_pop_returns_last(filled_stack):
    assert filled_stack.pop() == 30
    assert len(filled_stack) == 2

def test_stack_is_lifo(filled_stack):
    values = [filled_stack.pop() for _ in range(3)]
    assert values == [30, 20, 10]
    assert filled_stack.is_empty()


"""
Topic: Fixture with teardown (yield fixtures)
"""


@pytest.fixture
def temp_file(tmp_path):                    # tmp_path is a built-in pytest fixture!
    """Create a temporary file, clean up after test."""
    path = tmp_path / "test_data.txt"
    path.write_text("hello pytest")
    yield path                              # test runs here
    # teardown: tmp_path is automatically cleaned up by pytest


def test_temp_file_content(temp_file):
    assert temp_file.read_text() == "hello pytest"
    assert temp_file.name == "test_data.txt"


# ---- Run info when executed directly ---- #

if __name__ == "__main__":
    print("This file is meant to be run with pytest:")
    print()
    print("  pytest study_pytest.py -v")
    print("  pytest study_pytest.py -v -k 'test_add'")
    print("  pytest study_pytest.py -v --tb=short")
    print()
    print("Running pytest programmatically...")
    print()
    exit_code = pytest.main([__file__, "-v", "--tb=short", "--no-header"])
    raise SystemExit(exit_code)
