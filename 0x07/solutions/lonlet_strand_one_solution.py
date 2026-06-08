# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Lonlet Strand' """

import functools
import time


def use_timer():
    class Timer:
        def __new__(cls, *args, **kwargs):
            if args and callable(args[0]):
                self = super().__new__(cls)
                cls.__init__(self)          # default label=None
                return self(args[0])
            return super().__new__(cls)

        def __init__(self, label=None):
            self.label = label

        def __call__(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start
                name = self.label or func.__name__
                print(f"{name} took {duration:.4f} seconds")
                return result
            return wrapper

    @Timer
    def quick():
        time.sleep(0.3)

    @Timer(label="slow!")
    def slow():
        time.sleep(0.5)

    print(" 1| quick() start")
    quick()                                 # ty:ignore[missing-argument]
    print(" 2| stop")

    print(" 3| slow() start")
    slow()
    print(" 4| stop")


if __name__ == "__main__":
    use_timer()
