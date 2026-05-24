# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet shows how Python supports functional programming (FP).

Teaching focus
  - what counts as 'functional': first-class functions, purity, immutability,
    higher-order functions, recursion, lazy evaluation, composition,
    pattern matching, point-free style
  - which tools Python ships for it: functools, itertools, operator, lambdas,
    comprehensions, generator expressions, match/case, @dataclass(frozen=True)

Honest disclaimer
  - Python is not a functional language. It is multi-paradigm with a polite
    nod toward FP. Guido famously dislikes 'reduce'. We use it anyway.
  - No tail-call optimization. No persistent data structures in stdlib.
    Mutability is the default. Treat FP here as a *style*, not a religion.

See
  - https://docs.python.org/3/howto/functional.html
  - https://docs.python.org/3/library/functools.html
  - https://docs.python.org/3/library/itertools.html
  - https://docs.python.org/3/library/operator.html
"""

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods, unnecessary-lambda

import functools
import itertools
import operator
import sys
from dataclasses import FrozenInstanceError, dataclass
from types import MappingProxyType

from utils import print_function_header

# ----------------------------------------------------------------------------
# functions are first-class citizens
# ----------------------------------------------------------------------------

@print_function_header
def functions_are_first_class_citizens():
    """ functions as values: assign, store, pass, return """

    def square(x): return x * x
    def cube(x):   return x * x * x

    f = square                              # assign a function to a variable
    print(f" 1| f(5) = {f(5)}")

    ops = [square, cube, abs]               # list of functions
    print(f" 2| applied:   {[op(-3) for op in ops]}")

    def apply_twice(g, x): return g(g(x))   # pass a function as argument
    print(f" 3| twice sq:  {apply_twice(square, 3)}")

    def make_adder(n):                      # return a function (closure)
        def adder(x): return x + n
        return adder
    add10 = make_adder(10)
    print(f" 4| add10(5) = {add10(5)}")


# ----------------------------------------------------------------------------
# pure vs. impure functions
# ----------------------------------------------------------------------------

CART = []                                   # a module-level mutable

@print_function_header
def pure_vs_impure_functions():
    """ same input -> same output, no side effects, testable """

    def add_tax(price, rate):               # pure: only depends on its inputs
        return price * (1 + rate)

    def add_to_cart(item):                  # impure: mutates CART, no return
        CART.append(item)

    print(f" 1| pure twice: {add_tax(100, 0.19)}, {add_tax(100, 0.19)}")
    add_to_cart("apple")
    add_to_cart("apple")
    print(f" 2| impure CART grows: {CART}")


# ----------------------------------------------------------------------------
# immutability in practice
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Point:
    x: int
    y: int


@print_function_header
def immutability_in_practice():
    """ tuples, frozenset, frozen dataclasses, read-only dict views """

    t = (1, 2, 3)                           # tuple is immutable
    print(f" 1| tuple: {t}")
    try:
        t[0] = 9                            # ty:ignore[unsupported-operation]
    except TypeError as e:
        print(f" 2| tuple assignment -> TypeError: {e}")

    fs = frozenset({1, 2, 3})               # frozenset is hashable
    print(f" 3| frozenset: {fs}, hashable: {hash(fs) is not None}")

    p = Point(1, 2)                         # frozen dataclass
    print(f" 4| point: {p}")
    try:
        p.x = 99                            # ty:ignore[invalid-assignment]
    except FrozenInstanceError as e:
        print(f" 5| frozen point -> FrozenInstanceError: {e}")

    raw = {"a": 1, "b": 2}                  # read-only view onto a dict
    view = MappingProxyType(raw)
    print(f" 6| view['a'] = {view['a']}")
    try:
        view["a"] = 99                      # ty:ignore[unsupported-operation]
    except TypeError as e:
        print(f" 7| view assignment -> TypeError: {e}")

    # note: 'immutable' in Python is sometimes more a polite request than a law
    # in 3.15 a frozendict is announced


# ----------------------------------------------------------------------------
# lambdas — and when not to use them
# ----------------------------------------------------------------------------

@print_function_header
def avoid_named_lambdas():
    """ small lambdas are fine, big lambdas should have been 'def' """

    people = [("Alice", 30), ("Bob", 25), ("Carol", 35)]
    by_age = sorted(people, key=lambda p: p[1])     # tiny, clear, fine
    print(f" 1| by age: {by_age}")

    # PEP 8: 'always use a def statement instead of an assignment statement
    # that binds a lambda expression directly to an identifier'.
    add = lambda a, b: a + b                # pylint: disable=unnecessary-lambda-assignment
    print(f" 2| add(2,3) = {add(2, 3)}")

    # rule of thumb: if your lambda needs a comment, it should be a 'def'.


# ----------------------------------------------------------------------------
# higher-order classics: map, filter, zip, enumerate, reduce
# ----------------------------------------------------------------------------

@print_function_header
def higher_order_classics():
    """ the FP starter pack — and its Pythonic competitor: comprehensions """

    nums = [1, 2, 3, 4, 5]

    # three ways to write 'square the evens'
    way1 = list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums)))
    way2 = [x * x for x in nums if x % 2 == 0]      # comprehension
    way3 = list(x * x for x in nums if x % 2 == 0)  # generator expression
    print(f" 1| map+filter:    {way1}")
    print(f" 2| comprehension: {way2}")
    print(f" 3| gen expr:      {way3}")

    # most Pythonistas reach for the comprehension; map/filter survive when
    # the callable already exists by name (no lambda needed): map(str, nums).

    names = ["Alice", "Bob", "Carol"]
    ages = [30, 25, 35]
    print(f" 4| zip:        {list(zip(names, ages))}")
    print(f" 5| enumerate:  {list(enumerate(names, start=1))}")

    s = functools.reduce(operator.add, nums)        # sum
    p = functools.reduce(operator.mul, nums)        # product
    m = functools.reduce(max, nums)                 # max
    print(f" 6| reduce sum:  {s}")
    print(f" 7| reduce prod: {p}")
    print(f" 8| reduce max:  {m}")

    # for these, Python already has dedicated builtins — prefer them:
    print(f" 9| sum/prod/max builtins: {sum(nums)}, "
          f"{functools.reduce(operator.mul, nums)}, {max(nums)}")
    # use reduce when the operation has no dedicated builtin.

    # flatten: cursed vs. civilized
    nested = [[1, 2], [3, 4], [5]]
    cursed = sum(nested, [])                # works, O(n^2) — please do not
    civil = list(itertools.chain.from_iterable(nested))     # the right way
    print(f"10| cursed flatten:    {cursed}")
    print(f"11| chain.from_iter:   {civil}")


# ----------------------------------------------------------------------------
# function composition
# ----------------------------------------------------------------------------

@print_function_header
def function_composition():
    """ (f ∘ g)(x) = f(g(x)) — manually and via reduce """

    def compose2(f, g):
        return lambda x: f(g(x))            # two-function compose

    clean = compose2(str.strip, str.lower)
    print(f" 1| clean('  HELLO  ') = {clean('  HELLO  ')!r}")

    def compose(*funcs):                    # variadic, right-to-left
        return functools.reduce(compose2, funcs)

    pipeline = compose(str.title, str.strip, str.lower)
    print(f" 2| pipeline('  hello WORLD  ') = "
          f"{pipeline('  hello WORLD  ')!r}")


# ----------------------------------------------------------------------------
# partial application (currying-lite)
# ----------------------------------------------------------------------------

@print_function_header
def partial_application():
    """ pre-bake arguments with functools.partial """

    def log(level, msg): return f"[{level}] {msg}"

    log_warn = functools.partial(log, "WARNING")
    log_err  = functools.partial(log, "ERROR")
    print(f" 1| {log_warn('disk almost full')}")
    print(f" 2| {log_err('disk on fire')}")

    # true currying (one arg at a time) is rare in Python; partial is the
    # everyday tool. example: convert a binary op into a unary callable.

    times3 = functools.partial(operator.mul, 3)
    print(f" 3| times3 over 1..5: {list(map(times3, range(1, 6)))}")


# ----------------------------------------------------------------------------
# lazy pipelines with generators
# ----------------------------------------------------------------------------

@print_function_header
def lazy_pipelines():
    """ generator expressions + itertools = streaming computation """

    # an 'infinite' stream of naturals, processed lazily
    naturals = itertools.count(1)                   # 1, 2, 3, ...
    squares = (n * n for n in naturals)             # 1, 4, 9, ...
    big = itertools.dropwhile(lambda x: x < 100, squares)
    first5 = list(itertools.islice(big, 5))
    print(f" 1| first 5 squares >= 100: {first5}")

    words = ["apple", "banana", "cherry", "date", "elderberry"]
    short = itertools.takewhile(lambda w: len(w) <= 6, words)
    print(f" 2| takewhile len<=6: {list(short)}")

    data = [("a", 1), ("a", 2), ("b", 3), ("b", 4), ("c", 5)]
    grouped = {k: [v for _, v in g]
               for k, g in itertools.groupby(data, key=lambda t: t[0])}
    print(f" 3| groupby: {grouped}")

    # nothing is materialized until 'list(...)' or 'for' consumes it.


# ----------------------------------------------------------------------------
# recursion and its limits
# ----------------------------------------------------------------------------

@print_function_header
def recursion_and_its_limits():
    """ recursion is fine; just remember Python has no TCO """

    def fact(n):
        return 1 if n <= 1 else n * fact(n - 1)

    print(f" 1| fact(5)  = {fact(5)}")
    print(f" 2| fact(10) = {fact(10)}")

    # naive Fibonacci is exponential — unless you memoize:
    @functools.lru_cache(maxsize=None)
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    print(f" 3| fib(30) = {fib(30)} (cached: {fib.cache_info()})")

    print(f" 4| recursion limit: {sys.getrecursionlimit()}")

    # no tail-call optimization. Guido refused to add it on purpose
    # (better tracebacks, simpler model). for deep recursion: rewrite
    # as a loop, or use an explicit stack.


# ----------------------------------------------------------------------------
# pattern matching (PEP 634)
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Circle: radius: float
@dataclass(frozen=True)
class Square: side: float
@dataclass(frozen=True)
class Rect:   w: float; h: float


@print_function_header
def pattern_matching():
    """ match/case — the most FP-flavored feature added in years """

    def area(shape):
        match shape:
            case Circle(radius=r):  return 3.14159 * r * r
            case Square(side=s):    return s * s
            case Rect(w=w, h=h):    return w * h
            case _:                 return 0.0      # default / wildcard

    for sh in [Circle(2), Square(3), Rect(2, 4)]:
        print(f" 1| area({sh}) = {area(sh)}")

    # sequence + literal patterns
    def describe(seq):
        match seq:
            case []:               return "empty"
            case [x]:              return f"one: {x}"
            case [x, y]:           return f"two: {x}, {y}"
            case [x, *rest]:       return f"head {x}, tail {rest}"
            case _:                return "weird"

    for s in [[], [1], [1, 2], [1, 2, 3, 4]]:
        print(f" 2| describe({s}) = {describe(s)}")


# ----------------------------------------------------------------------------
# point-free style with the operator module
# ----------------------------------------------------------------------------

@print_function_header
def point_free_with_operator():
    """ operator.itemgetter, attrgetter, methodcaller — no lambdas needed """

    people = [
        {"name": "Alice", "age": 30},
        {"name": "Bob",   "age": 25},
        {"name": "Carol", "age": 35},
    ]
    by_age = sorted(people, key=operator.itemgetter("age"))
    print(f" 1| by age (itemgetter): {[p['name'] for p in by_age]}")

    points = [Point(1, 5), Point(3, 1), Point(2, 3)]
    by_y = sorted(points, key=operator.attrgetter("y"))
    print(f" 2| by y (attrgetter): {by_y}")

    words = ["alpha", "beta", "gamma"]
    upper = list(map(operator.methodcaller("upper"), words))
    print(f" 3| methodcaller('upper'): {upper}")

    # tally with reduce + operator.add
    total = functools.reduce(operator.add, [p["age"] for p in people])
    print(f" 4| total age: {total}")


# ----------------------------------------------------------------------------
# singledispatch — polymorphism without classes
# ----------------------------------------------------------------------------

@print_function_header
def singledispatch_polymorphism():
    """ dispatch on the type of the first argument """

    @functools.singledispatch
    def describe(obj):                      # default fallback
        return f"unknown: {obj!r}"

    @describe.register
    def _(obj: int):    return f"int {obj}, even={obj % 2 == 0}"

    @describe.register
    def _(obj: str):    return f"str of length {len(obj)}"

    @describe.register
    def _(obj: list):   return f"list of {len(obj)} items"

    for x in [42, "hello", [1, 2, 3], 3.14]:
        print(f" 1| {describe(x)}")

    # the FP-flavored alternative to isinstance-chains and method overrides.
    # closest stdlib cousin of 'pattern matching on type'.


# ----------------------------------------------------------------------------
# functional core, imperative shell
# ----------------------------------------------------------------------------

@print_function_header
def functional_core_imperative_shell():
    """ keep computation pure; push I/O to the edges """

    # pure core: no I/O, no globals
    def analyze(numbers):
        n = len(numbers)
        return {
            "n": n,
            "sum": sum(numbers),
            "avg": sum(numbers) / n if n else 0.0,
            "max": max(numbers) if numbers else None,
        }

    # imperative shell: gets data, prints results, the only impure bit
    # see also IPO-framework

    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    result = analyze(data)                  # easy to unit-test
    for k, v in result.items():
        print(f" 1| {k:>3}: {v}")

    # this pattern dominates codebases that 'feel' functional: 95% pure transformations


# ----------------------------------------------------------------------------
# where Python stops being functional (examples/topics)
# ----------------------------------------------------------------------------

@print_function_header
def where_python_stops_being_functional():
    """ a short tour of the leaks in the FP abstraction """

    # mutable default arguments — the classic foot-gun,
    # the default list is shared across calls
    def append_to(item, target=[]):         # pylint: disable=dangerous-default-value
        target.append(item)
        return target
    print(f" 1| append_to(1) = {append_to(1)}")
    print(f" 2| append_to(2) = {append_to(2)}  # surprise!")

    # no tail-call optimization — deep recursion crashes
    print(f" 3| recursion limit: {sys.getrecursionlimit()}")

    # exceptions as control flow are very imperative

    # 'for' is a statement, not an expression

    # the GIL serializes pure-Python execution; map() does not automatically parallelize

    # no persistent (structurally-shared) data structures in stdlib; every 'immutable update' allocates a fresh copy.

    print(" 4| use FP where it makes code clearer; drop it where it makes "
          "code clever-but-unreadable.")


if __name__ == "__main__":
    functions_are_first_class_citizens()
    pure_vs_impure_functions()
    immutability_in_practice()
    avoid_named_lambdas()
    higher_order_classics()
    function_composition()
    partial_application()
    lazy_pipelines()
    recursion_and_its_limits()
    pattern_matching()
    point_free_with_operator()
    singledispatch_polymorphism()
    functional_core_imperative_shell()
    where_python_stops_being_functional()
