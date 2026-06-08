# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Corside Sands' """

import functools

# as decorator function

def debug(func):
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]     # !r means to use 'repr', !s means 'str'
        signature = ", ".join(args_repr + kwargs_repr)
        print(f">>> called {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"<<< result {value!r}")
        return value
    return wrapper_debug

def use_debug():

    @debug
    def concat(a: str, b: int) -> str:
        return f"{a}{b}"

    result = concat("and the answer is: ", 42)
    print(f" 1| concat: {result=}")


# as decorator class

class Debug:
    def __init__(self, func):
        self._func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f">>> called {self._func.__name__}({signature})")
        value = self._func(*args, **kwargs)
        print(f"<<< result {value!r}")
        return value

def use_Debug():

    @Debug
    def combine(a: str, b: int) -> str:
        return f"{a}{b}"

    result = combine("and the answer is: ", 99)
    print(f" 1| combine: {result=}")


if __name__ == "__main__":
    use_debug()
    use_Debug()
