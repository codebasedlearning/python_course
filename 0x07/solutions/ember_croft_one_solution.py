# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Ember Croft' """

import functools
import inspect


def typecheck(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        print(f" a| {sig}")
        bound = sig.bind(*args, **kwargs)
        print(f" b| {bound}")
        bound.apply_defaults()
        print(f" c| {bound}")
        for name, value in bound.arguments.items():
            param = sig.parameters[name]
            if param.annotation is inspect.Parameter.empty:
                continue
            if not isinstance(value, param.annotation):
                raise TypeError(
                    f"arg '{name}' expected {param.annotation.__name__}, got {type(value).__name__}"
                )
        result = func(*args, **kwargs)
        ret = sig.return_annotation
        if ret is not inspect.Signature.empty:
            if not isinstance(result, ret):
                raise TypeError(
                    f"return expected {ret.__name__}, got {type(result).__name__}"
                )
        return result
    return wrapper


def use_typecheck():

    @typecheck
    def add(a: int, b: int) -> int:
        return a + b

    @typecheck
    def greet(name: str, times: int = 1):
        return (f"Hello, {name}! " * times).strip()

    print(f" 1| {add(1, 2)}")
    print(f" 2| {greet('Alice', 3)}")
    print(f" 3| {greet('Bob')}")             # default arg, no annotation check issue

    try:
        add(1, "2")
    except TypeError as e:
        print(f" 4| TypeError: {e}")

    try:
        greet(42)
    except TypeError as e:
        print(f" 5| TypeError: {e}")


if __name__ == "__main__":
    use_typecheck()
