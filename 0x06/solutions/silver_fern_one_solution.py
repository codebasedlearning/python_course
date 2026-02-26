# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Silver Fern'

Topics
  - lambdas
  - closures
  - nonlocal
  - higher-order functions
  - LEGB in action
"""


# Part 1 — lambda as a sorting key

def sort_by_second():
    pairs = [(1, "banana"), (3, "apple"), (2, "cherry")]
    by_name = sorted(pairs, key=lambda p: p[1])
    by_index_desc = sorted(pairs, key=lambda p: -p[0])
    print(f" 1| {by_name = }")
    print(f" 2| {by_index_desc = }")


# Part 2 — closure: make_multiplier

def make_multiplier(factor: int):
    """Return a function that multiplies its argument by factor."""
    def multiplier(x):
        return x * factor
    return multiplier


def use_multiplier():
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f" 3| {double(5) = }")       # 10
    print(f" 4| {triple(5) = }")       # 15
    print(f" 5| {list(map(double, range(1, 6))) = }")


# Part 3 — closure: make_accumulator (nonlocal)

def make_accumulator(start: int = 0):
    """Return a function that accumulates values across calls."""
    total = start
    def add(n: int) -> int:
        nonlocal total
        total += n
        return total
    return add


def use_accumulator():
    acc = make_accumulator()
    print(f" 6| {acc(10) = }")         # 10
    print(f" 7| {acc(5)  = }")         # 15
    print(f" 8| {acc(20) = }")         # 35

    acc100 = make_accumulator(100)
    print(f" 9| {acc100(1) = }")       # 101
    print(f"10| {acc(0)    = }")       # still 35 — independent state


# Part 4 — pipeline: compose simple transforms

def make_pipeline(*functions):
    """Return a function that applies each function in order."""
    def pipeline(value):
        for fn in functions:
            value = fn(value)
        return value
    return pipeline


def use_pipeline():
    add1   = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x ** 2

    pipe = make_pipeline(add1, double, square)
    # for x=3: add1 -> 4, double -> 8, square -> 64
    print(f"11| {pipe(3) = }")         # 64
    print(f"12| {pipe(0) = }")         # 4

    # same but in different order
    pipe2 = make_pipeline(square, add1, double)
    # for x=3: square -> 9, add1 -> 10, double -> 20
    print(f"13| {pipe2(3) = }")        # 20


if __name__ == "__main__":
    sort_by_second()
    use_multiplier()
    use_accumulator()
    use_pipeline()
