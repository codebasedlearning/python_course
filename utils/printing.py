# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

import functools


def print_function_header(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__
        print(f"\n{name}\n{'=' * len(name)}")
        return func(*args, **kwargs)
    return wrapper
