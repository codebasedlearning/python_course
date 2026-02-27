[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x06` – Scopes and language features


## Overview

This unit explores scopes and related language features, including lambdas, file IO, context
managers, and pattern matching.


### Focus

Understand how name resolution and resource management work, and apply these tools in small
utilities.


## Topics

- Scopes and the LEGB rule
- Lambdas and closures
- Context managers
- File I/O patterns
- Pattern matching (`match`)


## Tasks


### 👉 Task 'Self-Study'

- Review all snippets from the lecture.
- Run and understand all content from scripts that start with `study_` (if any). 
- Ask if there are any outstanding questions, or if you miss an idea.


### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do
  or have questions about?


### 👉 Task 'Ancestor Clove' 

- Think about how you could design a 'Timer' class implementing the 'ContextManager' protocol to
  measure time. Test it.
- What would a function 'timer' look like that uses '@contextmanager.' Also test it.

In both cases you can use the `fib(n)` function as a workload.
```
def fib(n):
    return fib(n-1)+fib(n-2) if n >= 3 else 1 if n >= 1 else 0
```


### 👉 Task 'Barren Grass' 

- Implement a context manager `Note` so that you get output indented by level. Example:

``` 
def show_loops():
    items = [2, 3, 5, 7, 11]
    number = 24
    with Note() as note:
        note(" 1| start loops")
        with note:
            for i in items:
                if number % i == 0:
                    note(f"{i} | {number}")
                    with note:
                        if i == 3:
                            note("found 3!")
                note.print(f"{i} checked")
        note.print(" 2| end")
```

Output:
```
 1| start loops
    2 | 24
    2 checked
    3 | 24
        found 3!
    3 checked
    5 checked
    7 checked
    11 checked
 2| end
```


### 👉 Task 'Moon Ragweed' 

- Write your own `my_closing` class and/or function so that this code works:
```
def close_a_context_manager():
    class Resource:
        def close(self):
            print(" a|   clean me")

    print(f" 1| use Resource with closing ver 1")
    with my_closing1(Resource()) as res:
        print(f"    type res: {type(res)}")
    print(f" 2| after using Resource")

    print(f" 3| use Resource with closing ver 2")
    with my_closing2(Resource()) as res:
        print(f"    type res: {type(res)}")
    print(f" 4| after using Resource")
```


### 👉 Task 'Drowsy Pudina'

- Create a context manager `readable_file` so that this code both opens and closes the file.

```
    with readable_file(filename) as reader:
        text = reader.readlines()
```


### 👉 Task 'Silver Fern' (Closures and Lambdas)

Topics: lambdas, closures, `nonlocal`, higher-order functions, LEGB in action

Part 1
- Given a list of tuples like `[(1, "banana"), (3, "apple"), (2, "cherry")]`, use `sorted` with a
  `lambda` as the `key` argument to sort by the second element (the string). Then sort again by the
  first element in descending order.

Part 2
- Write a function `make_multiplier(factor)` that returns a function which multiplies its argument
  by `factor`. This returned function is a closure — it captures `factor` from the enclosing scope.
- Test: `double = make_multiplier(2)`, then `double(5)` should return `10`.
- Use `map` with your `double` function on `range(1, 6)`.

Part 3
- Write a function `make_accumulator(start=0)` that returns a function `add(n)`. Each call to `add`
  adds `n` to a running total and returns it. You will need `nonlocal`.
- Test: `acc = make_accumulator()`, then `acc(10)` → `10`, `acc(5)` → `15`, `acc(20)` → `35`.
- Create a second accumulator `acc100 = make_accumulator(100)` and verify that the two accumulators
  maintain independent state.

Part 4
- Write a function `make_pipeline(*functions)` that returns a function applying each function in
  order. For example, `make_pipeline(add1, double, square)` applied to `3` gives `(3+1)*2 = 8`,
  then `8² = 64`.
- Define `add1`, `double`, and `square` as lambdas.

Check
- Compare your solution with the provided one from `solutions` and an AI-generated one.


### 👉 Task 'Eastern Rye'

The `match` snippet contains the `from_chat` function, which decides which 
formatter to create based on the arguments passed.
- Change the function implementation to use only the `match` command for selection.

Hint: The arguments can be part of the match condition.


### 👉 Project 'Moving Blizzard' — Part 6

> Continued from Part 5. Add file I/O, closures for alert thresholds, and `match` for sensor
type dispatch.

Topics: context managers, `@contextmanager`, closures, `match`, file I/O

Part 1
- Create a `CSVDataSource` whose `open_stream(sensor_id)` method is a context manager
  (use `@contextmanager`). It opens a CSV file, yields a generator of `Reading` objects
  for the requested sensor, and closes the file on exit.
- Write a helper `write_demo_csv(path)` that writes the raw data as CSV for testing.

Part 2
- Write `make_alert(label, min_val, max_val)` — a closure factory that returns a checker
  function. The checker takes a `Reading` and returns an alert string if the value is out of
  bounds, or `None` otherwise.
- Write `describe_sensor(sensor_id)` that uses `match` on the sensor name prefix
  (e.g. `"temp"` → `"Temperature sensor (°C)"`).

Part 3
- Write a `report_file(path)` context manager that opens a file, writes a header, yields the
  file handle, and writes a footer on exit.
- Combine everything: read data via `CSVDataSource`, check alerts via closures, write a
  report via the context manager.

Check
- Compare your solution with the provided one from `solutions` and an AI-generated one.


### 👉 AI 'Off-By-One Imp'

A fellow student asked an AI for help with this code:

```python
buttons = []
for i in range(5):
    buttons.append(lambda: print(f"Button {i}"))

for b in buttons:
    b()
# Expected: Button 0, Button 1, Button 2, Button 3, Button 4
# Actual:   Button 4, Button 4, Button 4, Button 4, Button 4
```

The AI diagnosed: *"The issue is that `range(5)` goes from 0 to 4, not 1 to 5. Change to
`range(1, 6)` if you want buttons numbered 1 through 5."*

Task
- The AI's diagnosis is completely wrong. What is the real problem?
- Explain why all five lambdas print `Button 4`. What does "late binding" mean here?
- Fix it using a default argument: `lambda i=i: ...` — why does this work?
- Fix it again using `functools.partial`. Which approach do you prefer?

Discuss
- Why did the AI get this so wrong? (Hint: the output *looks* like an off-by-one.)
- This is one of Python's most famous gotchas. Would you expect an AI to get it right
  every time?

[Hints](./solutions/hints.md)


### 👉 AI 'Off-By-One Imp'

A student wrote a counter using closures and got `UnboundLocalError`:

```python
def make_counter():
    count = 0
    def increment():
        count += 1
        return count
    def get():
        return count
    return increment, get

inc, get = make_counter()
inc()  # UnboundLocalError: cannot access local variable 'count'
```

The AI recommended: *"Use `global count` inside both `increment` and `get` to access the
outer variable."*

Task
- Apply the AI's fix (`global count`). It "works" — in a trivial sense. Now create two
  independent counters: `inc1, get1 = make_counter()` and `inc2, get2 = make_counter()`.
  Call `inc1()` three times, then check `get2()`. What went wrong?
- Apply the correct fix using `nonlocal`. Verify that both counters are independent.
- Explain the LEGB rule and which scope `count` lives in with each approach.

Discuss
- When is `global` the right tool? When is it a code smell?
- Why does `get()` work without `nonlocal` but `increment()` doesn't? (Hint: reading
  vs. writing.)

[Hints](./solutions/hints.md)


### 👉 Homework 'Couch Potato'

- If you did not finish the essential tasks in the exercise, finish them at home.


## Comprehension Check

General
- What is the main reason behind a 'context manager'?
- What is a 'scope,' and what kind of scopes do you know?
- What happens exactly when you import something?
- What does `nonlocal` do inside a nested function?
- What does LEGB stand for?

[Hints](./solutions/hints.md)
