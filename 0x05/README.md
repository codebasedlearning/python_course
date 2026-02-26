[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x05` – Iterators and Generators

## Overview

This unit covers iterators and generators, with exercises that build lazy sequences and reimplement
common iterator utilities.

### Focus

Practice lazy evaluation and custom iteration patterns to control performance and memory usage.

## Topics

- Iterator protocol
- Generators and generator expressions
- Lazy evaluation and memory usage
- Reimplementing iterator utilities (itertools/builtins)


## Tasks

---

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

---

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

---

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

---

### 👉 Task 'Self-Study'

- Review all snippets from the lecture. Ask if there are any outstanding questions.

---

### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do
  or have questions about?

---

### 👉 Task 'AI Snapshot' – AI Said It's Fine: Memory-Efficient Pipeline

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

---

### 👉 Task 'AI Snapshot' – AI Said It's Fine: Iterator Reuse

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

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

## Comprehension Check

General
- Describe 'iterators' and 'generators.' What are the benefits?
- Are there any use cases you see for your projects or code?
- What is the difference between `iter()` and `next()`?
- What happens when a generator is exhausted?
- What is a generator expression?

---
