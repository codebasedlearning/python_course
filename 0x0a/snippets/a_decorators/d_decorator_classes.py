# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about classes as decorators.

Teaching focus
  - classes (instead of functions) as decorators
"""

import functools


def use_class_as_decorator():
    """ using a class as decorator """
    print("\nuse_class_as_decorator\n======================")

    def call_and_log(intro, some_f, *args):
        """ helper: log the call and return the result """
        print(f" {intro}| call {some_f.__name__}({" ".join(map(str, args))})", end=' ')
        z = some_f(*args)
        print(f"-> {z}")
        return z

    class LogCalls:
        def __init__(self, some_f):         # receives the function
            self.some_f = some_f

        def __call__(self, *args):          # invoked when function is called (skip **kwargs)
            return call_and_log("a", self.some_f, *args)

    @LogCalls
    def f(x):
        return x*7

    print(f" 1| call 'f': {f(3)}, {type(f)=}, {f=}")

    class LogCallsWithIntro:
        def __init__(self, intro:str):        # receives the parameters
            self.intro = intro

        def __call__(self, some_f):         # receives the function to decorate
            @functools.wraps(some_f)        # as before
            def wrapper(*args):
                return call_and_log(self.intro, some_f, *args)
            return wrapper

    @LogCallsWithIntro(intro="b")
    def g(x):
        return x*7

    print(f" 2| call 'g': {g(3)}, {type(g)=}, {g=}")

    class LogCallsFlexible:
        def __new__(cls, *args, **kwargs):
            if args and callable(args[0]):  # without parentheses
                instance = super().__new__(cls)
                instance.__init__()
                return instance.__call__(args[0])
            return super().__new__(cls)

        def __init__(self, doc:str="?"):
            self.doc = doc

        def __call__(self, some_f):
            @functools.wraps(some_f)
            def wrapper(*args):
                return call_and_log("c", some_f, *args)
            return wrapper

    @LogCallsFlexible(doc="333")
    def h1(x):
        return x*2
    @LogCallsFlexible
    def h2(x):
        return x*2

    print(f" 3| call 'h1': {h1(3)}, {type(h1)=}, {h1=}")
    print(f" 4| call 'h2': {h2(3)}, {type(h2)=}, {h2=}")


if __name__ == "__main__":
    use_class_as_decorator()

"""
Whether to use a decorator function or a decorator class depends on your use case. 
  - Decorator functions are more commonly used in day-to-day Python programming 
    because of their simplicity and readability.
      - Lightweight and concise.
      - Ideal for simple use cases where the decorator doesn’t need to manage 
        state or complex logic.

  - Decorator Classes
      - More flexible and powerful but involve more boilerplate code.
      - Classes allow decorators to maintain state (via instance attributes) or 
        implement complex logic (beyond what’s feasible with nested functions).
      - Slightly less common when a decorator function suffices, but 
        indispensable in advanced use cases.

wraps, update_wrapper
  - See https://docs.python.org/3/library/functools.html
"""
