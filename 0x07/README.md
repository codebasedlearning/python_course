[© 2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x07` – Iterators and Generators


## Topics covered

- Iterators
- Generators


## Tasks

---

### 👉 Task 'Rash Annie' 

- Implement a 'generator function' `factorial` (n!). It should generate this:
```
    list(factorial(8))
        => [1, 1, 2, 6, 24, 120, 720, 5040, 40320]
```
- Same task for `fibonacci`. Its result is:
``` 
    list(fibonacci(8))
        => [1, 1, 2, 3, 5, 8, 13, 21]
```

---

### 👉 Task 'Duck Corn' 

> Reprogram some existing functions/iterators/generators. Most of them come from `itertools` or `builtins`.

Remarks:
- To get a specific number of values from a generator you can use `list(islice(iterable,number))`, returning 
a list with `number` elements from `iterable`.
- Most functions are described in `itertools`, along with the task description and a "roughly equivalent" implementation.
Don't spoil yourself, try it first.

Tasks:

- Implement `count(start=0)`
  - Make a generator function that returns evenly spaced (+1) values starting with number `start`.
```
    list(islice(my_count(10), 6)) 
        => [10, 11, 12, 13, 14, 15]
```

- `repeat(object[, times])`
  - Make a generator function that returns `object` over and over again. Runs indefinitely unless the times argument 
is specified.
```
    list(my_repeat(10, 3)) 
        => [10, 10, 10]
    list(map(pow, range(10), my_repeat(2))) 
        => [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

- `chain(*iterables)`
  - Make a generator function that returns elements from the first iterable until it is exhausted, then proceeds to the 
next iterable, until all the iterables are exhausted. Used for treating consecutive sequences as a single sequence.
```
    def f_gen(): return (i*i for i in range(6))
    rg = range(2,5,2)
    list(my_chain(rg,f_gen())) 
        => [2, 4, 0, 1, 4, 9, 16, 25]
```

- `dropwhile(predicate, iterable)`
  - Make a generator function that drops elements from the iterable as long as the predicate is true; afterwards, 
returns every element. 
``` 
    data = [1, 4, 9, 16, 25]
    pred = lambda x: x < 10
    list(my_dropwhile(pred, data)) 
        => [16, 25]
```

- `takewhile(predicate, iterable)`
  - Make a generator function that returns elements from the iterable as long as the predicate is true. 
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
  - Make an iterator class that can be used in a similar way to `zip`, but taking elements from the second iterable 
in reverse order.
```
    chars = ['A', 'B', 'C']
    numbers = [1, 2, 3]
    list(cross(chars, numbers)) 
        => [('A', 3), ('B', 2), ('C', 1)]
```

- `compress(data, selectors)`
  - Make a generator function that filters elements from data returning only those that have a corresponding element in 
selectors that evaluates to True. Stops when either the data or selectors iterables has been exhausted 
(remember 'Sieve-Prime'-Task).
```
    sieve = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    numbers = range(0, len(sieve))
    list(my_compress(numbers, (1-i for i in sieve))) 
        => [2, 3, 5, 7, 11]
```

- ⭐`product(*iterables)`
  - Create a generator function that iterates the Cartesian product of input iterables. This is roughly equivalent 
to nested for-loops in a generator expression, e.g.
`product(A, B)` returns the same as `((x,y) for x in A for y in B)`.
  - It is allowed to consume the iterables first.
  - Can you implement a 'real' generator function that avoids consumption?
```
    major = [1, 2]
    minor = [5, 6]
    sub = ["alpha", "beta"]
    list(my_product(major, minor, sub))
        => [(1, 5, 'alpha'), (1, 5, 'beta'), (1, 6, 'alpha'), (1, 6, 'beta'), (2, 5, 'alpha'), (2, 5, 'beta'), (2, 6, 'alpha'), (2, 6, 'beta')]
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

- Create generator expressions `select_from(operation, iterable)` and `where(predicate, iterable)` such that 
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
- 'PINQ' is inspired by [LINQ](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) 😉.

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

    gen = PINQ().From(data).Select(lambda x: x*x).Select(lambda x: x+10).Where(lambda x: x > 11).Select(lambda x: x-4)
    list(gen)
        => [10, 15]
```

---

### 👉 Task 'Self-Study'

- Review all snippets from the lecture. Ask if there are any outstanding questions.

---

### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do or have questions about?

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

### 👉 Comprehension Check - Talk with your Neighbor

General
- Describe 'iterators' and 'generators.' What are the benefits?
- Are there any use cases you see for your projects or code?

---

### 👉 Lecture Check - Online Questionare

- Please participate in the survey: [Slido](https://wall.sli.do)

---

End of `Unit 0x07`
