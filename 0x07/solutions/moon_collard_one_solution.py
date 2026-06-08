# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Moon Collard' """

import random

EXAMPLES = dict()

def example(func):
    EXAMPLES[func.__name__] = func
    # def wrapper():
    #     func()
    # return wrapper
    return func

@example
def case1(): return 23

# @example                                  # skip this
def case2(): return -1

@example
def case3(): return 42

def call_random_examples():
    print(f" 1| call a random case: test value={random.choice(list(EXAMPLES.values()))()}")
    print(f" 2| {EXAMPLES.items()}")


class Example:
    registry = {}                           # shared across all instances

    def __new__(cls, func):                 # no-params: return func directly
        cls.registry[func.__name__] = func
        return func

@Example
def case4(): return 99

# @Example                                  # skip this
def case5(): return -1

@Example
def case6(): return 101

def call_random_Examples():
    print(f" 1| call a random case: test value={random.choice(list(Example.registry.values()))()}")
    print(f" 2| {Example.registry.items()}")


if __name__ == "__main__":
    call_random_examples()
    call_random_Examples()
