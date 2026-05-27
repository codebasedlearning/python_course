# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates advanced typing features.

Teaching focus
  - Literal for restricting string/int values
  - Final for preventing reassignment
  - TypeGuard for type narrowing

Advanced typing
  - Python's type system is gradually typed: you opt in where you want
    static checking (mypy, pyright) without losing dynamic flexibility.
  - Literal restricts a parameter to specific constant values.
  - Final marks variables as not-to-be-reassigned.

See also
  https://docs.python.org/3/library/typing.html
  https://peps.python.org/pep-0484/
  https://mypy.readthedocs.io/en/stable/more_types.html
"""

from typing import Final, Literal, TypeGuard, overload

from utils import print_function_header

"""
Topic: Literal — restrict to specific values
"""


def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> str:
    """Only accepts specific string values (enforced by type checker)."""
    return f"Log level set to {level}"


@print_function_header
def using_literal():
    """ Literal restricts parameter values at type-check time """

    print(f" 1| {set_log_level('DEBUG')}")
    print(f" 2| {set_log_level('ERROR')}")

    # this would be a type error (caught by mypy/pyright, not at runtime):
    # set_log_level("TRACE")  # error: "TRACE" is not in Literal[...]
    print(f" 3| set_log_level('TRACE') would be a mypy error")

    # Literal works with int too
    def roll_dice() -> Literal[1, 2, 3, 4, 5, 6]:
        import random
        return random.randint(1, 6)

    print(f" 4| dice roll: {roll_dice()}")

    # practical use: mode parameters
    def open_mode(mode: Literal["r", "w", "a"]) -> str:
        return f"Opening in mode '{mode}'"

    print(f" 5| {open_mode('r')}")


"""
Topic: Final — constants and non-overridable methods
"""


MAX_RETRIES: Final = 3                      # type checker prevents reassignment
API_BASE: Final[str] = "https://api.example.com"


@print_function_header
def using_final():
    """ Final prevents reassignment (enforced by type checker) """

    print(f" 1| MAX_RETRIES = {MAX_RETRIES}")
    print(f" 2| API_BASE = {API_BASE}")

    # these would be type errors:
    # MAX_RETRIES = 5     # error: Cannot assign to final name "MAX_RETRIES"
    # API_BASE = "other"  # error: Cannot assign to final name "API_BASE"
    print(f" 3| reassignment would be a mypy error")

    # Final in classes
    class Config:
        TIMEOUT: Final = 30
        NAME: Final[str] = "myapp"

    config = Config()
    print(f" 4| Config.TIMEOUT = {config.TIMEOUT}")
    print(f" 5| note: Final is checked statically, not enforced at runtime")


"""
Topic: TypeGuard — type narrowing in conditionals
"""


def is_string_list(val: list) -> TypeGuard[list[str]]:
    """Check if all elements are strings. Narrows the type for the checker."""
    return all(isinstance(item, str) for item in val)


@print_function_header
def using_typeguard():
    """ TypeGuard tells the type checker about narrowed types """

    data: list = ["hello", "world", "python"]

    if is_string_list(data):
        # after this check, the type checker knows: data is list[str]
        joined = " ".join(data)             # no type error
        print(f" 1| joined: {joined}")

    mixed: list = ["hello", 42, "world"]
    if is_string_list(mixed):
        print(f" 2| this won't print (mixed has non-strings)")
    else:
        print(f" 2| mixed is not all strings: {mixed}")

    print(f" 3| TypeGuard is the return type of a 'type narrowing' function")
    print(f" 4| the function returns bool, but the type checker uses it")
    print(f"    to narrow the argument's type in the if-branch")


if __name__ == "__main__":
    using_literal()
    using_final()
    using_typeguard()
