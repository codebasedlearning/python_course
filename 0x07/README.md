[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x07` – Decorators

## Overview

This unit focuses on decorators, including variations with parameters, return values, and class-based usage.

### Focus

Learn to wrap and enhance functions cleanly while preserving behavior and metadata.

## Topics

- Decorators (basics)
- Decorators with parameters and return values
- Default values and metadata preservation
- Class-based decorators
- Class decorators


## Tasks

---

### 👉 Task 'Moon Collard' 

1) Write a 'debug' decorator that prints all arguments and the result of a 
decorated function. Example: 
```
@debug
def concat(a: str, b: int) -> str:
    return f"{a}{b}"

def test_debug():
    result = concat("and the answer is: ", 42)
    print(f"01| concat: '{result}'\n")
```
this prints
``` 
>>> called concat('and the answer is: ', 42)
<<< result 'and the answer is: 42'
01| concat: 'and the answer is: 42'
```

2) Write a 'slow_down_v1' decorator that prints a countdown from a given number 
with a delay of 1s between each step. 
Example:
```
@slow_down_v1
def countdown_v1(from_number):
    if from_number < 1:
        print("--- Liftoff")
    else:
        print(f"--- cnt: {from_number}...")
        countdown_v1(from_number - 1)

def test_slow_down():
    n = 3
    print(f"02| countdown from {n=} ...")
    countdown_v1(n)
```
this prints
```
02| countdown from n=3 ...
--- cnt: 3...
--- cnt: 2...
--- cnt: 1...
--- Liftoff
```
with 1s delay between each line. Use `time.sleep(1)` for 1s delay.

3) Extend the previous decorator to 'slow_down_v2'. You may or may not specify a time delay `dt` (default 1s).  
That means, both 
```
@slow_down_v2(dt=0.5)
def countdown_v2(from_number):
    ...
```
and
```
@slow_down_v2
def countdown_v2(from_number):
    ...
```
are valid. 

4) Write an 'example' decorator that 'registers' a function in a global dictionary. 
Here we use this idea to select a random test case (see `test_example_test_cases`).
```
EXAMPLES = dict()

@example
def test_case1():
    return 23

def other_function():
    return -1

@example
def test_case3():
    return 42

[...]

def test_example_test_cases():
    print(f"03| call a random test case: test value={random.choice(list(EXAMPLES.values()))()}")
    print(f"04| {EXAMPLES.items()}")

```
This results in:
``` 
03| call a random test case: test value=23
04| dict_items([('test_case1', <function test_case1 at 0x106a1b2e0>), ('test_case3', <function test_case3 at 0x106a1b420>)])
```

5) Write a timer decorator class (!) that measures the execution time of a function
and prints a label if one is given.

Usage examples
```
@Timer
def quick():
    time.sleep(0.3)

@Timer(label="slow!")
def slow():
    time.sleep(0.5)
```

6) ⭐ Write your own `functools.lru_cache`. This [module](https://docs.python.org/3/library/functools.html#functools.lru_cache) comes with a '@lru_cache' decorator, which gives you the ability 
to cache the result of your functions using the Least Recently Used (LRU) strategy. 
For more background see also [here](https://realpython.com/lru-cache-python/).

---

### 👉 Task 'Self-Study'

- Review all snippets from the lecture. Ask if there are any outstanding questions.

---

### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do or have questions about?

---

### 👉 Task 'AI Snapshot' – `functools.wraps`

Prompt
- "Which decorator preserves `__name__` and `__doc__`?"

AI Answer A
```python
import functools

def deco(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper
```

AI Answer B
```python
def deco(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper
```

Discuss
- Which answer preserves metadata and why?
- What breaks in tooling when metadata is lost?

---

### 👉 Task 'AI Snapshot' – Decorator Timing

Prompt
- "When is `decorating f` printed?"

AI Answer A
```python
def deco(fn):
    print("decorating", fn.__name__)
    def wrapper(*a, **k):
        print("calling")
        return fn(*a, **k)
    return wrapper

@deco
def f():
    print("f")

# Printed at definition/import time
```

AI Answer B
```python
# Printed only when `f()` is called
```

Discuss
- Which answer is correct?
- Why is this important for side effects at import time?

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

## Comprehension Check

General
- What kind of decorators do you know?
- What is the reason for using `functools`?
- Why is `functools.wraps` recommended in decorators?
- When would you use a decorator with parameters?

---
