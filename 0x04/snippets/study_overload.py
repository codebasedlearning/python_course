# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates advanced typing features.

Teaching focus
  - @overload for type-safe function signatures
  - @overload tells the type checker about different call signatures,
    but only one implementation runs at runtime.

See also
  https://docs.python.org/3/library/typing.html
  https://peps.python.org/pep-0484/
  https://mypy.readthedocs.io/en/stable/more_types.html
"""

from typing import Final, Literal, TypeGuard, overload

from utils import print_function_header

"""
Topic: @overload — multiple signatures, one implementation
"""


# overload signatures (for the type checker only, never executed)
@overload
def get_item(index: int) -> str: ...
@overload
def get_item(index: str) -> list[str]: ...

# actual implementation (must handle all overloaded cases)
def get_item(index):
    items = ["alpha", "bravo", "charlie", "delta"]
    if isinstance(index, int):
        return items[index]
    elif isinstance(index, str):
        return [item for item in items if index.lower() in item.lower()]
    raise TypeError(f"Expected int or str, got {type(index).__name__}")


@print_function_header
def using_overload():
    """ @overload gives the type checker precise return types """

    # the type checker knows:
    # get_item(int) → str
    # get_item(str) → list[str]

    result_int = get_item(0)                # type checker infers: str
    print(f" 1| get_item(0) = {result_int!r} (type: {type(result_int).__name__})")

    result_str = get_item("a")              # type checker infers: list[str]
    print(f" 2| get_item('a') = {result_str} (type: {type(result_str).__name__})")

    # without @overload, the type checker would only know: str | list[str]
    # with @overload, it narrows based on the argument type

    print(f" 3| note: @overload is for the type checker, not runtime dispatch")
    print(f" 4| for runtime dispatch by type, use @functools.singledispatch")


if __name__ == "__main__":
    using_overload()
