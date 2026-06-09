[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x07` – Decorators


## Overview

This unit focuses on decorators, including variations with parameters, return values, and
class-based usage.
The unit also covers the `match` pattern.


### Focus

Learn to wrap and enhance functions cleanly while preserving behavior and metadata.


## Topics

- Decorators (basics)
- Decorators with parameters and return values
- Class-based decorators
- Class decorators
- Pattern matching (`match`)


## Tasks

### 👉 Task 'Self-Study'

- Review all snippets from the lecture.
- Run and understand all content from scripts that start with `study_` (if any). 
- Ask if there are any outstanding questions, or if you miss an idea.


### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do
  or have questions about?


### 👉 Task 'Corside Sands' 

1) Write a 'debug' decorator function that prints all arguments and 
the result of a decorated function. Example: 
```
@debug
def concat(a: str, b: int) -> str:
    return f"{a}{b}"

def test_debug():
    result = concat("and the answer is: ", 42)
    print(f" 1| concat: '{result}'\n")
```
this prints
``` 
>>> called concat('and the answer is: ', 42)
<<< result 'and the answer is: 42'
 1| concat: 'and the answer is: 42'
```

2) ⭐ Now write the decorator as a class `Debug`.

Hint: See expert level snippet `xpert_decorator_classes.py`.


### 👉 Task 'Lonlet Strand' 

1) Write a timer decorator function `timer` that measures the execution time 
of a function and prints a label if one is given.

Usage examples
```
@timer
def quick():
    time.sleep(0.3)

@timer(label="slow!")
def slow():
    time.sleep(0.5)
```

2) ⭐ Use a decorator class `Timer` to implement the timer.

Hint: See expert level snippet `xpert_decorator_classes.py`.


### 👉 Task 'Hazel Cove'

Write a `deprecated` decorator that emits a `DeprecationWarning` whenever the
decorated function is called.

- The warning message should include the function name.
- The warning should point to the **caller's** line, not the inside of the wrapper.
- ⭐ Extend it to `@deprecated(message="use new_api instead")` with an optional custom message.

Usage:
```python
@deprecated
def old_api(x):
    return x * 2

def use_deprecated():
    old_api(5)   # DeprecationWarning: old_api is deprecated
```

Hint: `warnings.warn` has a `stacklevel` parameter — what value makes the warning
point at the caller?


### 👉 Task 'Ember Croft'

Write a `typecheck` decorator function that enforces type annotations at runtime.

- Check all annotated parameters against their declared types.
- Raise a `TypeError` with a clear message if a type mismatch is found.
- Skip parameters with no annotation.
- ⭐ Also check the return value annotation.

Usage:
```python
@typecheck
def add(a: int, b: int) -> int:
    return a + b

def use_typecheck():
    print(f" 1| {add(1, 2)}")        # ok: 3
    add(1, "2")                      # TypeError: arg 'b' expected int, got str
```

Hint: Use `inspect.signature` to map positional arguments to parameter names
and `sig.bind(*args, **kwargs)` to resolve them.


### 👉 Task 'Moon Collard'

1) Write an 'example' decorator function that 'registers' a function 
in a global dictionary. 
Here we use this idea to select a random test case.

```
EXAMPLES = dict()

# def example [...]

@example
def case1():
    return 23

# @example # skip this
def case2():
    return -1

@example
def case3():
    return 42

def call_example_cases():
    print(f" 1| call a random case: test value={random.choice(list(EXAMPLES.values()))()}")
    print(f" 2| {EXAMPLES.items()}")
```

This results in:
``` 
 1| call a random test case: test value=23
 2| dict_items([('test_case1', <function test_case1 at 0x106a1b2e0>),
    ('test_case3', <function test_case3 at 0x106a1b420>)])
```

2) ⭐ So this is a decorator with some sort of state (`EXAMPLES`). 
Why is this not an optimal solution? Find a better one.

Hint: See expert level snippet `xpert_decorator_classes.py`.


### ⭐ Task 'Diamond Bay' 

Write your own `functools.lru_cache`. This
[module](https://docs.python.org/3/library/functools.html#functools.lru_cache) comes with a
'@lru_cache' decorator, which gives you the ability to cache the result 
of your functions using the Least Recently Used (LRU) strategy. 
For more background see also [here](https://realpython.com/lru-cache-python/).


### 👉 Task 'Coral Ridge'

A log entry looks like this: `"ERROR:timeout after 30s"`, `"WARN:retry 2/3"`, `"INFO:started"`.

Write a `parse_log_entry(entry: str)` that uses **only** `match` to return:
- `("error", message)` for `ERROR`
- `("warning", message)` for `WARN`
- `("info", message)` for `INFO`
- `("unknown", entry)` for everything else

Then decorate it with `@debug` from Task 'Corside Sands' to see it in action.


### 👉 Task 'Eastern Rye'

The following function `from_chat` decides which formatter to create 
based on the arguments passed.

```
class Formatter: ...

class JsonFormatter(Formatter): ...

class XmlFormatter(Formatter): ...

def from_chat(text: str | None = None, force_json: bool = False, force_xml: bool = False) -> Formatter | None:
    if force_json or "json" in text:
        return JsonFormatter()
    elif force_xml or "xml" in text:
        return XmlFormatter()
    else:
        return None
```

Here are some test cases:
```
    print(f" 1| None? {from_chat('Lorem Ipsum')}")
    print(f" 2| json? {from_chat('Lorem json Ipsum')}")
    print(f" 3| json? {from_chat('Lorem Ipsum', force_json=True)}")
    print(f" 4| None? {from_chat('Lorem json', force_json=True, force_xml=True)}")
    print(f" 5| xml? {from_chat('Lorem xml Ipsum')}")
    print(f" 6| xml? {from_chat('Lorem Ipsum', force_xml=True)}")
    print(f" 7| None? {from_chat('Lorem xml', force_xml=True, force_json=True)}")
```

- Change the function implementation to use only the `match` command for selection.

Hint: The arguments can be part of the match condition.


### 👉 Project 'Moving Blizzard' — Part 7

> Continued from Part 6. Add decorators: `@timed` for profiling, `@retry` for flaky sources,
`@validate_readings` for filtering generators, and `@register` for an analyzer registry.

Topics: decorators, `functools.wraps`, parameterized decorators, decorator on generators

Part 1
- Write a `@timed` decorator that prints the execution time of the decorated function.
- Write a `@retry(max_attempts=3, delay=0.1)` parameterized decorator that retries on
  exception.

Part 2
- Create a `FlakySource` class whose `read_all` method randomly raises `ConnectionError`
  (use `random.Random` with a seed). Decorate it with `@retry`.
- Write a `@validate_readings(low, high)` decorator that wraps a generator function and
  drops any `Reading` whose value is out of range (i.e. the decorator itself yields).

Part 3
- Write a `@register` decorator that adds the decorated function to a global `ANALYZERS`
  dict. Register at least `count_readings`, `average_value`, and `max_value`.
- In `main()`, iterate over `ANALYZERS` and run each analyzer on the valid readings.
- Decorate the entire analysis run with `@timed` and observe the output.

Check
- Compare your solution with the provided one from `solutions` and an AI-generated one.


### 👉 AI 'Off-By-One Imp'

You asked three different AI models: *"Write a decorator `@logged` that prints before and
after a function call."*

Answer A
```python
def logged(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__}")
        return result
    wrapper.__name__ = func.__name__
    return wrapper
```

Answer B
```python
def logged(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__}")
        return result
    return wrapper
```

Answer C
```python
import functools

def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__}")
        return result
    return wrapper
```

Task
- All three "work" — they print before and after. Rank them from worst to best.
- Decorate a function with a docstring using each version. Then check `help(your_func)`.
  What differs?
- Answer A manually copies `__name__`. What else does it miss that `functools.wraps`
  handles? (Hint: `__doc__`, `__module__`, `__qualname__`, `__wrapped__`)
- Answer B is the most common beginner version. Why does it break `pytest` discovery
  or `sphinx` documentation?

Discuss
- Why do most AIs produce Answer B or C, but rarely A?
- Is there a case where you deliberately *don't* want `@functools.wraps`?

[Hints](./solutions/hints.md)


### 👉 AI 'Off-By-One Imp'

An AI generated this decorator and said *"Ready to use"*:

```python
import functools
import logging

logging.basicConfig(level=logging.INFO)

def tracked(func):
    logging.info(f"Registered: {func.__name__}")
    call_count = 0
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        logging.info(f"{func.__name__} called {call_count} time(s)")
        return func(*args, **kwargs)
    return wrapper

@tracked
def process_data(data):
    """Crunches the numbers."""
    return sum(data)

@tracked
def send_report(msg):
    """Sends the report."""
    print(msg)
```

Task
- Run this file **without calling any function**. What gets printed? Why?
- When exactly does `logging.info(f"Registered: ...")` execute — at import time or at
  call time?
- Imagine this module is imported by 10 other modules. What happens?
- Is the `call_count` per-function or global? Trace through two calls to `process_data`
  and one to `send_report`.
- When are import-time side effects acceptable, and when are they a trap?

Discuss
- The 'example' decorator from Task 'Moon Collard' (task 4) *also* runs at definition
  time — but there it's intentional. What's the difference?

[Hints](./solutions/hints.md)


### 👉 Homework 'Couch Potato'

- If you did not finish the essential tasks in the exercise, finish them at home.


## Comprehension Check

General
- What kind of decorators do you know?
- What is the reason for using `functools`?
- Why is `functools.wraps` recommended in decorators?
- When would you use a decorator with parameters?
- What is the advantage of using `match`?

[Hints](./solutions/hints.md)
