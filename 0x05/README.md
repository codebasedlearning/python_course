[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x05` – Recap & Roadmap, Iterators, and Generators


## Overview

This unit covers iterators and generators, with exercises that build lazy sequences and reimplement
common iterator utilities.
We start with a recap of the topics covered in previous units and mark them on a scale from 0 to 3
 to prioritize the learning.
We end this with a task that is very similar to an 80% exam to check your understanding.

### Focus

Practice lazy evaluation and custom iteration patterns to control performance and memory usage.


## Topics

- Recap
- Iterator protocol
- Generators and generator expressions
- Lazy evaluation and memory usage
- Reimplementing iterator utilities (itertools/builtins)
- 80%-Exam


## Recap & Roadmap

### Recap – Topics from Units `0x01`–`0x05`

Compact map of everything we touched so far. The rightmost column rates how
"standard" a topic is, on a four-tier scale — most "advanced" Python topics
are *not* actually niche; you'll meet them in any real codebase, so they
deserve their own tier:

- **0** = standard — every introductory course covers it
- **1** = intermediate — common, but not day-one stuff
- **2** = professional — daily in real codebases, must-know once you ship;
  this is where most of the eye-openers live
- **3** = esoteric — genuinely niche, library-author territory, or a
  stylistic flourish you can live without

| Python Topic                                                                                                                  | Std/Niche |
|-------------------------------------------------------------------------------------------------------------------------------|-----------|
| Program structure: comments, imports, docstrings, indentation                                                                 | 0         |
| `__name__ == "__main__"` guard                                                                                                | 0         |
| Scalar types: `int`, `float`, `bool`, `str` (immutability, no real primitives)                                                | 0         |
| Console I/O: `input`, `print`, f-strings, `format`                                                                            | 0         |
| Control flow: `if`/`while`/`for`, `try`/`except`, `ValueError`                                                                | 0         |
| Functions, default args, named/keyword args, `*args`/`**kwargs`                                                               | 0         |
| Unpacking (tuple/list, `*`, `**`)                                                                                             | 0         |
| Collections: `list`, `tuple`, `dict`, `set`, `frozenset`, `range`                                                             | 0         |
| Slicing, `is` vs `==`, short-circuiting                                                                                       | 0         |
| Shallow vs deep copy, default-argument pitfalls                                                                               | 2         |
| List / dict / set comprehensions, generator expressions                                                                       | 0         |
| `any` / `all` / `sum` / `len` / `min` / `max` (with `key=`)                                                                   | 0         |
| Counter pattern on `dict` (`counter_add/sub/most_common`)                                                                     | 0         |
| Fibonacci: iterative, recursive, memoised                                                                                     | 0         |
| Graph as dict-of-dicts, Dijkstra w/ `heapq`                                                                                   | 1         |
| Testing with `pytest`, `pytest.raises`, `-v` flag                                                                             | 2         |
| Debugging: `breakpoint()` / `pdb` (`p`, `n`, `c`)                                                                             | 1         |
| Tooling: `uv`, `pyproject.toml`, virtual envs, Python version                                                                 | 2         |
| Lint / typecheck workflow: `pylint`, `mypy`                                                                                   | 2         |
| Classes, `__init__`, attributes, "Pythonic" instantiation                                                                     | 0         |
| `@property` (read/write, computed), encapsulation, "protected" `_x`                                                           | 0         |
| Class vs instance attributes (shadowing)                                                                                      | 2         |
| Instance / `@classmethod` / `@staticmethod`                                                                                   | 0         |
| Dunder methods: `__str__`, `__repr__`, `__eq__`, `__hash__`, `__lt__`, `__add__`, `__contains__`, `__getitem__`, `__iter__`   | 2         |
| `@functools.total_ordering`                                                                                                   | 3         |
| `@dataclass` (incl. `frozen=True`)                                                                                            | 2         |
| `enum` / `Enum`                                                                                                               | 2         |
| `enum` / flags                                                                                                                | 3         |
| Single inheritance, method overriding ("virtual"-style)                                                                       | 0         |
| Custom exceptions                                                                                                             | 2         |
| `__slots__`, named tuples                                                                                                     | 3         |
| Type hints / annotations, `Optional`, `list[T]`                                                                               | 2         |
| Static analysis: `mypy`, `pyright`, IDE checks                                                                                | 2         |
| Duck typing vs nominal vs structural typing                                                                                   | 2         |
| `typing.Protocol`, structural subtyping (PEP 544)                                                                             | 2         |
| `@runtime_checkable` on Protocols                                                                                             | 2         |
| Abstract base classes (`abc.ABC`, `@abstractmethod`)                                                                          | 2         |
| Mixins, multiple inheritance                                                                                                  | 2         |
| MRO, `super()` with cooperative `kwargs`                                                                                      | 2         |
| C3 linearisation                                                                                                              | 3         |
| Composition vs inheritance trade-offs                                                                                         | 2         |
| Generics: `TypeVar`, variance                                                                                                 | 2         |
| PEP 695 generic class syntax (`class Box[T]:`, Python 3.12+)                                                                  | 1         |
| Covariant / contravariant `TypeVar` declarations (`covariant=True`, `contravariant=True`)                                     | 3         |
| `Callable[[X], Y]` variance (contravariant in input, covariant in output)                                                     | 3         |
| Generic `Protocol[T]` (parameterised structural typing)                                                                       | 2         |
| `Iterable[T]` typing                                                                                                          | 2         |
| `iter()` / `next()` built-ins, manual iteration, `StopIteration` handling                                                     | 0         |
| Iterator vs iterable distinction; iterator-exhaustion / reuse bug                                                             | 1         |
| Iterator protocol (`__iter__` + `__next__`, `StopIteration`)                                                                  | 0         |
| Generator functions, `yield`, generator expressions                                                                           | 0         |
| `isinstance(x, Iterable)` via `collections.abc` (runtime structural check)                                                    | 1         |
| Using `itertools` from the stdlib (`count`, `islice`, `chain`, …)                                                             | 1         |
| Re-implementing `itertools`/built-ins (`count`, `chain`, `dropwhile`, `takewhile`, `zip`, `compress`, `product`, `enumerate`) | 1         |
| Lazy evaluation, memory profiling (`sys.getsizeof`, `tracemalloc`)                                                            | 2         |
| Fluent / LINQ-style chained API (`PINQ`)                                                                                      | 3         |
| Cross-cutting project: streaming pipeline (`filter → moving avg → anomaly`)                                                   | 1         |

### Roadmap — Topics from Units `0x06`–`0x09 + 0x_tra_unit`

What lies ahead, on the same four-tier scale. Most of it sits at tier 2, reading
"you'll write this in week one on the job." (professional).
Tier 3 here is more the genuine library-author corner.

| Python Topic | Std/Niche |
|---|-----------|
| LEGB scope rule, name resolution | 1         |
| `global` / `nonlocal` | 1         |
| Closures (capture by reference, late-binding gotcha) | 2         |
| Lambdas (and when *not* to use them) | 0         |
| Context managers: `with`, `__enter__` / `__exit__` | 2         |
| `contextlib.@contextmanager` (generator-based CMs) | 2         |
| `contextlib.closing` | 1         |
| File I/O: `open`, modes, encodings | 0         |
| `match` / `case` pattern matching (literal, sequence, class patterns) | 2         |
| Module imports, packages, `__init__.py`, relative imports | 0         |
| `argparse` (CLI parsing, subcommands, type conversion) | 3         |
| `json` (dumps/loads, `default=`, dataclass round-tripping) | 3         |
| `pickle` (binary serialization, arbitrary-code-execution caveat) | 3         |
| `re` (regex: `search`, `match`, `findall`, `sub`, named groups, `VERBOSE`) | 3         |
| `subprocess` (`run`, capture, `shell=True` security) | 3         |
| `map` / `filter` / `functools.reduce` revisited | 1         |
| Function decorators (basic `def wrapper(*a, **kw)` pattern) | 2         |
| Parameterized decorators (decorator factories: `@retry(3)`) | 2         |
| `functools.wraps` (preserving `__name__`, `__doc__`, `__wrapped__`) | 2         |
| Decorator classes (callable instances with `__call__`) | 2         |
| Class decorators (decorating the class itself) | 2         |
| Registration pattern via decorators (plugin/route registries) | 2         |
| `functools.lru_cache` / `@cache` (memoization) | 2         |
| `functools.singledispatch` (type-based dispatch) | 2         |
| Cache introspection (`cache_info()`, `cache_clear()`) | 1         |
| Threading: `threading.Thread`, `start` / `join` | 1         |
| `threading.Lock`, mutexes, race conditions | 2         |
| `threading.Condition` (condition variables) | 2         |
| `concurrent.futures.ThreadPoolExecutor`, `as_completed` | 3         |
| The GIL and its implications for CPU- vs IO-bound work | 2         |
| `multiprocessing.Pool` (CPU-bound parallelism) | 3         |
| `queue.Queue` (thread-safe producer/consumer) | 2         |
| `logging` (loggers, handlers, levels, `basicConfig`) | 2         |
| `sqlite3` / SQL basics from Python | 3         |
| NumPy / SciPy (vectorized numerics) | 3         |
| Microsoft Exchange / mail-calendar integration | 3         |
| OpenAI / ChatGPT API usage | 3         |
| Packaging & distribution (`pyproject.toml` for wheels) | 2         |
| Timing & profiling (`time.perf_counter`, `timeit`, `cProfile`) | 2         |
| `async` / `await`, coroutines | 2         |
| Event loop, `asyncio.run` | 2         |
| `asyncio.gather`, `asyncio.sleep` | 2         |
| `asyncio.TaskGroup` (Python 3.11+) | 2         |
| Common async pitfalls (`time.sleep` in `async def`, hidden blocking I/O) | 2         |
| Awaitable protocol (`__await__`) | 3         |
| Free-threaded Python (PEP 703, Python 3.13+ no-GIL) | 2         |
| Descriptor protocol (`__get__`, `__set__`, `__delete__`, `__set_name__`) | 3         |
| Data vs non-data descriptors | 3         |
| Reusable validation via descriptors (`Bounded`, `Logged`) | 3         |
| Method binding via descriptors, `types.MethodType` | 3         |
| `ast` (parse source into syntax tree, `eval`) | 3         |
| `dis` (bytecode disassembler) | 3         |
| Metaclasses (custom `type` subclasses, class-creation hooks) | 3         |


## Tasks

### 👉 Task 'Self-Study'

- Review all snippets from the lecture.
- Run and understand all content from scripts that start with `study_` (if any). 
- Ask if there are any outstanding questions, or if you miss an idea.


### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do
  or have questions about?


### 👉 Task 'Rash Annie' 

- Implement a 'generator function' `factorial` (n!). It should generate this:
```
    list(factorial(8))
        => [1, 1, 2, 6, 24, 120, 720, 5040, 40320]
```
- This example yields 0! through 8! (9 values).
- Same task for `fibonacci`. Its result is:
``` 
    list(fibonacci(8))
        => [1, 1, 2, 3, 5, 8, 13, 21]
```


### 👉 Task 'Duck Corn' 

> Reprogram some existing functions/iterators/generators. Most of them come from `itertools` or
`builtins`.

Remarks:
- To get a specific number of values from a generator you can use `list(islice(iterable,number))`,
  returning 
a list with `number` elements from `iterable`.
- Most functions are described in `itertools`, along with the task description and a "roughly
  equivalent" implementation.
Don't spoil yourself, try it first.

Tasks:

- Implement `count(start=0)`
  - Make a generator function that returns evenly spaced (+1) values starting with number `start`.
```
    list(islice(my_count(10), 6)) 
        => [10, 11, 12, 13, 14, 15]
```

- `repeat(object[, times])`
  - Make a generator function that returns `object` over and over again. Runs indefinitely unless
    the times argument 
is specified.
```
    list(my_repeat(10, 3)) 
        => [10, 10, 10]
    list(map(pow, range(10), my_repeat(2))) 
        => [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

- `chain(*iterables)`
  - Make a generator function that returns elements from the first iterable until it is exhausted,
    then proceeds to the 
next iterable, until all the iterables are exhausted. Used for treating consecutive sequences as a
single sequence.
```
    def f_gen(): return (i*i for i in range(6))
    rg = range(2,5,2)
    list(my_chain(rg,f_gen())) 
        => [2, 4, 0, 1, 4, 9, 16, 25]
```

- `dropwhile(predicate, iterable)`
  - Make a generator function that drops elements from the iterable as long as the predicate is
    true; afterwards, 
returns every element. 
``` 
    data = [1, 4, 9, 16, 25]
    pred = lambda x: x < 10
    list(my_dropwhile(pred, data)) 
        => [16, 25]
```

- `takewhile(predicate, iterable)`
  - Make a generator function that returns elements from the iterable as long as the predicate is
    true. 
``` 
    data = [1, 4, 9, 16, 25]
    pred = lambda x: x < 10
    list(my_takewhile(pred, data)) 
        => [1, 4, 9]
```

- `zip(iterable1, iterable2)`
  - Make a generator function that returns tuples from both iterables, one at a time - see example. 
For different lengths, use the minimum.
```
    chars = ['A', 'B', 'C']
    numbers = [1, 2, 3]
    list(my_zip(chars, numbers)) 
        => [('A', 1), ('B', 2), ('C', 3)]
```

- `class cross(Iterator)`
  - Make an iterator class that can be used in a similar way to `zip`, but taking elements from the
    second iterable 
in reverse order.
```
    chars = ['A', 'B', 'C']
    numbers = [1, 2, 3]
    list(cross(chars, numbers)) 
        => [('A', 3), ('B', 2), ('C', 1)]
```

- `compress(data, selectors)`
  - Make a generator function that filters elements from data returning only those that have a
    corresponding element in 
selectors that evaluates to True. Stops when either the data or selectors iterables has been
exhausted 
(remember 'Sieve-Prime'-Task).
```
    sieve = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    numbers = range(0, len(sieve))
    list(my_compress(numbers, (1-i for i in sieve))) 
        => [2, 3, 5, 7, 11]
```

- ⭐`product(*iterables)`
  - Create a generator function that iterates the Cartesian product of input iterables. This is
    roughly equivalent 
to nested for-loops in a generator expression, e.g.
`product(A, B)` returns the same as `((x,y) for x in A for y in B)`.
  - It is allowed to consume the iterables first.
  - Can you implement a 'real' generator function that avoids consumption?
```
    major = [1, 2]
    minor = [5, 6]
    sub = ["alpha", "beta"]
    list(my_product(major, minor, sub))
        => [(1, 5, 'alpha'), (1, 5, 'beta'), (1, 6, 'alpha'), (1, 6, 'beta'),
            (2, 5, 'alpha'), (2, 5, 'beta'), (2, 6, 'alpha'), (2, 6, 'beta')]
```

- `enumerate(iterable)`
  - Create a generator function that simulates the built-in `enumerate` function.
```
    numbers = ['A', 'B', 'C']
    list(my_enumerate(numbers)) 
        => [(0, 'A'), (1, 'B'), (2, 'C')]
```

- `splitlines(text: str)`
  - Create a generator function that simulates the `string.splitlines` function.
```
  text = """Lorem ipsum... 
    At vero eos et accusam... 
    Stet clita kasd ..."""
 
    list(my_splitlines(text))
        => ['Lorem ipsum... ', 'At vero eos et accusam... ', 'Stet clita kasd ...']
```

- Create generator expressions `select_from(operation, iterable)` and `where(predicate, iterable)`
  such that 
this code works as expected:
```
    data = [1, 2, 3]
    list(where(lambda x: x > 11, select_from(lambda x: (x + 10), data)))
        => [12, 13]
```


### ⭐ Task 'Red Berry' 

- Implement a `class PINQ(iterator)` so that the following code works as expected.
- **Avoid any creation of data containers until the final evaluation, e.g. by `list`.**
- Remember `select_from` and `where` from Task 'Duck Corn'.
- 'PINQ' is inspired by
  [LINQ](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) 😉.

```
    data = [1, 2, 3]
    
    gen = PINQ().From(data).Select(lambda x: (x+10)).Where(lambda x: x > 11).to_generator()
    list(gen)
        => [12, 13]

    gen = PINQ().From(data).Select(lambda x: (x+10)).Where(lambda x: x > 11).to_list()
    gen
        => [12, 13]

    gen = PINQ().From(data).Select(lambda x: (x+10)).Where(lambda x: x > 11)
    list(gen)
        => [12, 13]

    gen = PINQ().From(data).Select(lambda x: (x+10, x+100)).Where(lambda x: x[0] > 11)
    list(gen)
        => [(12, 102), (13, 103)]

    gen = PINQ().From(data).Select(lambda x: x*x).Select(lambda x: x+10).Where(lambda x: x > 11)
    list(gen.to_list())
        => [14, 19]

    gen = (PINQ()
        .From(data)
        .Select(lambda x: x*x)
        .Select(lambda x: x+10)
        .Where(lambda x: x > 11)
        .Select(lambda x: x-4))
    list(gen)
        => [10, 15]
```


### 👉 Project 'Moving Blizzard' — Part 5

> Continued from Part 4. Replace eager `read_all` with lazy generators. Build a full
pipeline: stream → filter → moving average → anomaly detection. Nothing is loaded into
memory all at once.

Topics: generator functions, `yield`, lazy evaluation, pipeline composition

Part 1
- Change `DataSource` so it has a `stream(sensor_id)` method that yields `Reading` objects
  one by one (instead of returning a list).
- Implement `ListSource.stream` using `yield`.

Part 2
- Write generator functions for a three-stage pipeline:
  - `filter_valid(readings, low, high)` — drop readings outside the valid range.
  - `moving_average(readings, window=3)` — yield `(reading, avg)` tuples using a sliding
    window buffer.
  - `detect_anomalies(stream, deviation=3.0)` — yield `(reading, avg, diff)` when a value
    deviates from the moving average by more than `deviation`.

Part 3
- Write `run_pipeline(source, sensor_id)` that chains all three stages.
- Run it on `"temp_north"` and `"water_lvl"` and print the anomalies.
- Verify that `type(raw_gen)` is a generator — nothing was fully materialised.

Check
- Compare your solution with the provided one from `solutions` and an AI-generated one.


### 👉 AI 'Off-By-One Imp'

You asked an AI to write a *"memory-efficient data processing pipeline"* and got this:

```python
def process_large_dataset(data):
    """Memory-efficient processing pipeline for large datasets."""
    filtered = [x for x in data if x > 0]              # step 1: keep positives
    transformed = [x ** 2 for x in filtered]            # step 2: square them
    top_10 = sorted(transformed, reverse=True)[:10]     # step 3: top 10
    return top_10
```

The AI commented: *"This is memory-efficient because we only return the top 10 at the end."*

Task
- How many full-size intermediate lists does this code create? Name each one.
- If `data` has 10 million elements, roughly how much memory do steps 1–3 use?
- Rewrite using generator expressions where possible. Which step *cannot* be lazy? Why?
- Measure the memory difference using `sys.getsizeof` or `tracemalloc` on a large input.

Discuss
- Why do AI tools frequently produce list comprehensions instead of generator expressions?
- When is eagerness actually the right choice?

[Hints](./solutions/hints.md)


### 👉 AI 'Off-By-One Imp'

An AI produced this iterator class and said *"Works perfectly"*:

```python
class Squares:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        result = self.i ** 2
        self.i += 1
        return result
```

Task
- Create `sq = Squares(5)`. Run `list(sq)`. Run `list(sq)` again. What happens?
- Explain why the second call returns `[]`.
- Fix the class so that each `for` loop or `list()` call starts fresh.
  (Hint: where should the counter live — in the class, or in `__iter__`?)
- Compare your fix to how a generator function handles this automatically.

Discuss
- This is one of the most common iterator bugs in AI-generated code. Why is it so
  common?
- What is the difference between an *iterator* and an *iterable*?

[Hints](./solutions/hints.md)


### 👉 80%-Exam 'RSA Cryptosystem'

#### Context — RSA

We want to model a generic cryptosystem for encrypting and decrypting messages
and, concretely, implement **RSA**: a scheme with a private key `d` (decrypt)
and a public key `e` (encrypt).

Everything is integers: `e`, `d`, the plaintext `m`, the ciphertext `c` are all
natural numbers. RSA is built on two given primes `p` and `q`; we also use
`N = p*q` and `φ = (p-1)*(q-1)`. Other details are out of scope here.

The exam has two parts: **A1** is about finding suitable keys `e` and `d`;
**A2** is the actual encryption / decryption.

---

#### A0 – Preliminaries

(a) **[1P]** Create a solution script containing a main guard calling two functions `A1`
and `A2` (filled in later).

(b) **[2P]** The script runs without errors (and contains significant code).

#### A1 — Finding the private key `d`

For a given public key `e` we find a matching `d` using the **Extended
Euclidean Algorithm** `egcd`. Like the classic Euclidean algorithm, it
computes the greatest common divisor `g = gcd(a, b)` of two integers `a`
and `b`, but additionally returns integers `s`, `t` with

```
(*)   g = gcd(a, b) = s*a + t*b
```

The result is a 3-tuple `(g, s, t) = egcd(a, b)`, modeled by the class
`EgcdResult`.

In the RSA setting (`a = e`, `b = φ`) we have
`gcd(e, φ) = s*e + t*φ ≡ 1 (mod φ)`, so we choose `d := s` (`t` is discarded).

**Example.** For `p = 11`, `q = 13`, `e = 23`, hence `N = 143`, `φ = 120`:

```
1 = gcd(23, 120) = 47*23 + (-9)*120  (mod 120)
=>  egcd(23, 120) = (1, 47, -9),  d := s = 47
```

The algorithm itself is implemented in (d).

(a) **[5P]** Implement a class `EgcdResult` (1P) holding `g`, `s` and `t`. 
  Instead of individual variables store the three `int`s in a
  *single private tuple* (1P) `_data` with type information (1P). 
  Design `__init__`  so that `EgcdResult(1, 47, -9)` works (1P).
  Create an instance `r` in `A1` with the example values from above (1P).

(b) **[4P]** Expose three **read-only properties** `g`, `s`, `t` returning
  positions 0, 1, 2 of `_data`, so that `r.g`, `r.s`, `r.t` work
  for an instance `r` (2P). Use type hints for the properties (1P) and
  print `r`, `r=` and all three values `r.g`, `r.s`, `r.t` to the console using
  string interpolation (1P).

(c) **[4P]** Implement appropriate **dunder** functions such that printing 
  `r` in (b) gives `(1,47,-9)` (2P) and `r=` gives `EgcdResult(g=1, s=47, t=-9)` (2P).

(d) **[8P]** Implement the recursive extended Euclidean algorithm (4P) in 
  a class function (1P) `egcd` with type hints (1P). The rule is

  ```
  egcd(a, b) = (a, 1, 0)                                if b == 0
             = (g, t, s - t * (a // b))                 otherwise,
                with (g, s, t) = egcd(b, a % b)
  ```
  Test it (as a class function) with the example values from the context example 
  above (2P).

(e) **[3P]** Assume `res` holds the result from calling `egcd(23, 120)`.
  According to the equation (*) above, `s*a + t*b - g` (the residual) should be 0.
  Check it by implementing an appropriate dunder function (2P) calculating the residual
  with `res[a,b]`. Call and print it in `A1` successfully (1P). 
  Hint: `a,b` leads to a tuple-parameter.

(f) **[3P]** Provide a **generic** equivalent of `EgcdResult`
  named `EgcdResultGen`. Create the generic class (1P) and adapt only the
  initializer from (a) (1P) and the property `g` (b) (1P) with correct types.

A1: 27 Points

#### A2 — RSA encryption / decryption

We first define a generic container class `CryptoText` (a vector of `int`
values), then a generic cryptosystem interface `ICryptoSystem`, then the
concrete class `RSA`.

*Note:* A2 does **not** require any code from A1.

Given `e`, `d`, `N`, encryption / decryption are

```
c ≡ m^e (mod N)        (encrypt)
m ≡ c^d (mod N)        (decrypt)
```

**Example** (same as A1): `p=11`, `q=13`, `N=143`, `e=23`, `d=47`,
`m = 7  =>  c = 7**23 mod 143 = 2`, and `c=2 => m = 2**47 mod 143 = 7`.

(a) **[7P]** Implement a class `CryptoText` that inherits from `list[int]` (1P).
  It supports these construction forms:
  (i) empty: `CryptoText()` (1P)
  (ii) single int: `CryptoText(7)` (1P)
  (iii) multiple ints: `CryptoText(7,8)` (1P)
  (iv),(v) iterable of ints: `CryptoText((1, 2, 3))` or `CryptoText([1, 2, 3])` (2P).
  Test all five forms in `A2` and print the instances to the console (1P).

(b) **[2P]** Define a protocol `ICryptoSystem` (1P) with two methods
  `encrypt(text: CryptoText) -> CryptoText` and
  `decrypt(text: CryptoText) -> CryptoText` (1P).

(c) **[1P]** Implement a class `RSA` satisfying `ICryptoSystem`. The constructor
  takes `p, q, e, d` and stores them, plus the derived `N = p*q` (1P). For the
  encryption / decryption see (d).

(d) **[6P]** Implement `encrypt` (2P) and `decrypt` (2P) per the formulas above. 
  Use the built-in three-argument `pow(x, y, n)` (this is Python's "discrete
  modular exponentiation"). 
  In `A2` test both functions for `m=7` and `m=23` and print the results (2P).

(e) **[2P]** Refactor `RSA.encrypt` (1P) and `RSA.decrypt` (1P) using only 
  comprehension or generator expression.

A2: 18 Points

#### Time and Points

Grand total is: 3+27+18 = 48 Points

This is not a full-time exam. There are topics missing. If you assume 2h for the
final exam, this is worth 80%.


### 👉 Homework 'Couch Potato'

- If you did not finish the essential tasks in the exercise, finish them at home.


## Comprehension Check

General
- Describe 'iterators' and 'generators.' What are the benefits?
- Are there any use cases you see for your projects or code?
- What is the difference between `iter()` and `next()`?
- What happens when a generator is exhausted?
- What is a generator expression?

[Hints](./solutions/hints.md)
