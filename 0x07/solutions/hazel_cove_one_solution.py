# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Hazel Cove' """

import functools
import warnings

# basic version

def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is deprecated",
            DeprecationWarning,
            stacklevel=2,                   # points to the caller, not this wrapper
        )
        return func(*args, **kwargs)
    return wrapper


def use_deprecated():

    @deprecated
    def old_api(x):
        """Old way of doing things."""
        return x * 2

    warnings.simplefilter("always")         # show every warning, not just the first
    result = old_api(5)
    print(f" 1| result: {result}")


# with optional message

def deprecated_msg(func=None, *, message: str | None = None):
    def decorator(func):
        msg = message or f"{func.__name__} is deprecated"
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper

    if func is not None:                    # @deprecated — no params
        return decorator(func)
    return decorator                        # @deprecated(message=...) — with params


def use_deprecated_msg():

    @deprecated_msg
    def old_api(x):
        return x * 2

    @deprecated_msg(message="use new_api instead")
    def also_old(x):
        return x + 1

    warnings.simplefilter("always")
    print(f" 2| {old_api(5)}")
    print(f" 3| {also_old(5)}")


if __name__ == "__main__":
    use_deprecated()
    use_deprecated_msg()
