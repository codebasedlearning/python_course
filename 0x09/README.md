[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x09` – Async and Descriptors

## Overview

This unit introduces async programming with `async` and `await` and continues with descriptors as an
advanced language feature.

### Focus

Develop a working mental model of cooperative concurrency and attribute control.

## Topics

- Async programming (`async`/`await`)
- AsyncIO and task scheduling
- Descriptors


## Terms

Many terms and definitions related to multitasking, threading, or concurrency 
are language-independent (language agnostic or language neutral). If this is 
a new topic for you, do not miss the [video](https://www.youtube.com/watch?v=GNMDHr8hvSM) on
processes and threads.

You have to be careful about the peculiarities of the programming language or 
library you are using. In asyncio, creating a coroutine does not run it; you must `await` it or
schedule it as a task.

Python-specific information on asyncio can be found here:
[Python docs](https://docs.python.org/3/library/asyncio.html),
[Python glossary](https://docs.python.org/3/glossary.html).

Here are a couple of terms in relation to `async`, `await` and AsyncIO.

### Parallelism
Parallelism consists of performing multiple operations at the same time. 

### Multiprocessing
Multiprocessing is a means to affect parallelism, and it entails spreading 
tasks over a computer’s central processing units (CPUs, or cores). 
Multiprocessing is well-suited for CPU-bound tasks: tightly bound for loops 
and mathematical computations usually fall into this category.

### Concurrency
Concurrency is a slightly broader term than parallelism. It suggests that 
multiple tasks can run in an overlapping manner. It does not imply parallelism.

### Threading
Threading is a concurrent execution model whereby multiple threads take 
turns executing tasks. One process can contain multiple threads. Python 
has a complicated relationship with threading thanks to its GIL.

### AsyncIO Package
The asyncio package is described by the Python documentation as a library 
to write concurrent code. However, async IO is not threading, nor is it 
multiprocessing. It is not built on top of either of these.

In fact, async IO is a single-threaded, single-process design: it uses 
cooperative multitasking. 
It has been said in other words that async IO gives a feeling of 
concurrency despite using a single thread in a single process. Coroutines 
(a central feature of async IO) can be scheduled concurrently, but they 
are not inherently concurrent.

### asynchronous
What does it mean for something to be asynchronous? This isn’t a rigorous 
definition:
- Asynchronous routines are able to 'pause' while waiting on their ultimate 
  result and let other routines run in the meantime.
- Asynchronous code, through the mechanism above, facilitates concurrent 
  execution. To put it differently, asynchronous code gives the look and 
  feel of concurrency.

### Chess Example
Async IO may at first seem counterintuitive and paradoxical. How does something 
that facilitates concurrent code use a single thread and a single CPU core? 
This is from Miguel Grinberg’s 2017 PyCon talk, which explains everything quite
beautifully:

Chess master Judit Polgár hosts a chess exhibition in which she plays multiple 
amateur players. She has two ways of conducting the exhibition: synchronously 
and asynchronously.

Assumptions:
- 24 opponents
- Judit makes each chess move in 5 seconds
- Opponents each take 55 seconds to make a move
- Games average 30 pair-moves (60 moves total)

### Synchronous version
Judit plays one game at a time, never two at the same time, until the game 
is complete. Each game takes (55 + 5) * 30 == 1800 seconds, or 30 minutes. 
The entire exhibition takes 24 * 30 == 720 minutes or 12 hours.

### Asynchronous version
Judit moves from table to table, making one move at each table. She leaves 
the table and lets the opponent make their next move during the wait time. 
One move on all 24 games takes Judit 24 * 5 == 120 seconds, or 2 minutes. 
The entire exhibition is now cut down to 120 * 30 == 3600 seconds or just 
1 hour.

There is only one Judit Polgár, who has only two hands and makes only one 
move at a time by herself. But playing asynchronously cuts the exhibition 
time down from 12 hours to one. 
So, cooperative multitasking is a fancy way of saying that a program’s 
event loop (more on that later) communicates with multiple tasks to let 
each take turns running at the optimal time.

### Coroutines
At the heart of async IO are coroutines. A coroutine is a specialized version 
of a Python generator function. A coroutine is a function that can suspend 
its execution before reaching return, and it can indirectly pass control 
to another coroutine for some time.

### Event Loop 
You can think of an event loop as something like a 'while True' loop that 
monitors coroutines, taking feedback on what’s idle, and looking around for 
things that can be executed in the meantime. It is able to wake up an idle 
coroutine when whatever that coroutine is waiting on becomes available.

```
asyncio.run(main())  # Python 3.7+
```

Here are a few points worth stressing about the event loop.
- Coroutines do little on their own until they are tied to the event loop.
- By default, an async IO event loop runs in a single thread and on a 
  single CPU core. 
- Event loops are pluggable. That is, you could, if you really wanted, write
  your own event loop implementation and have it run tasks just the same. 


## Some Rules of Async IO

- The keyword `await` passes function control back to the event loop. 
  It suspends the execution of the surrounding coroutine.
- A function that you introduce with `async def` is a coroutine. 
- Using `await` creates a coroutine function. To call a coroutine function, 
  you must `await` it to get its results.
- Just like it’s a SyntaxError to use `yield` outside of a `def` function, 
  it is a SyntaxError to use `await` outside of an `async def` coroutine. 
  You can only use `await` in the body of coroutines.
- Finally, when you use `await f()`, it’s required that `f()` be an object 
  that is awaitable. 
- An awaitable object is either (1) another coroutine or (2) an object 
  defining an `.__await__()` dunder method.


## Tasks

---

### 👉 Task 'Yellow Hemp'—Again (see Unit 0x0b)

In the directory `data` you will find 120 small text files, all of which have 
the following structure (example `test001.txt`):
```
# data 001
8, 8, 3
19
```
The first line contains the example number in the comment. The second line 
contains the summands and the third line contains the sum. All files are 
constructed in this way, there are no syntax errors or other 'niceties.'

1) Read all the files and check that the given sum is correct in an 'async' version. 
2) Install a (free-threading-Python)[https://docs.python.org/3/howto/free-threading-python.html] in
a virtual environment and compare
your execution times.

---

### 👉 Task 'Judit' 

Create a serial and an 'async' version of the story of Judith. Use one second 
instead of one hour, so the serial version should take around 12 seconds and 
the asynchronous version one second.

---

### 👉 Task 'Colemark Cove'

Take any of your thread-based tasks from Unit 0x0b and create
an 'async' version of it.

---

### 👉 Task 'Cobalt Reef' (Descriptors)

Topics: descriptor protocol (`__get__`, `__set__`, `__set_name__`), data descriptors, reusable
validation

Part 1
- Create a descriptor class `Bounded` that enforces numeric min/max bounds on any attribute it
  guards. The descriptor should:
  - Accept `min_value` and `max_value` in `__init__`.
  - Use `__set_name__` to learn the attribute name automatically.
  - In `__set__`, raise `TypeError` if the value is not numeric and `ValueError` if it is out of
    bounds.
  - In `__get__`, return the stored value (use a private attribute on the instance).

Part 2
- Create a class `Sensor` with two descriptor-guarded attributes:
  - `temperature = Bounded(-40.0, 80.0)`
  - `humidity = Bounded(0.0, 100.0)`
- The `__init__` takes `name`, `temperature`, and `humidity`.
- Test: verify that valid values are accepted, and that out-of-range or non-numeric values raise the
  expected exceptions.

Part 3
- Create a second descriptor `Logged` that prints a message on every `__get__` and `__set__` access.
- Use it in a small `Config` class with attributes `debug` and `language`.
- Observe the log output when creating an instance and reading its attributes.

Check
- Compare your solution with `cobalt_reef_one_solution.py` in `solutions`.
  - Is your solution correct and complete?
  - Could you combine `Bounded` and `Logged` into one descriptor? Should you?

---

### 👉 Task 'Raven Stickweed' (Descriptor Method Binding)

Topics: non-data descriptors, `__get__`, `types.MethodType`, method binding

In Python, `@classmethod` gives you `cls` and regular methods give you `self` — but what
if you want *both*?

Part 1
- Write a descriptor class `ClassInstanceMethod` that, when used as a decorator, provides the
  decorated function with a single argument that bundles both the class and the instance.
  - Implement `__get__` so it returns a bound method via `types.MethodType`.
  - The bound argument should be the tuple `(cls, obj)`.

Part 2
- Use your descriptor in a class `C` with an `__init__` that stores a `base: int`.
- Decorate a method `mult(clsSelf, n_times)` that unpacks `cls, self = clsSelf` and returns
  a string like `"self.base*n_times=35 in <class '__main__...C'>"`.
- Test with `c7 = C(base=7)` and `c7.mult(5)`.

Part 3
- Create a subclass `D(C)` (no extra code needed) and verify that `d4 = D(base=4)` with
  `d4.mult(3)` correctly reports class `D`, not `C`.
- Why does this work without any changes to `ClassInstanceMethod`?

Check
- Compare your solution with `raven_stickweed_one_solution.py` in `solutions`.
  - What happens if `obj` is `None` (i.e. accessed on the class, not an instance)?
  - How does this relate to how Python implements regular methods internally?

---

### 👉 Task 'Exam Preparation' 

Take a look at the topics covered and think about how you can prepare.


---

### 👉 Task 'Self-Study'

- Review all snippets from the lecture. Ask if there are any outstanding questions.

---

### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do
  or have questions about?

---

### 👉 Task 'AI Snapshot' – Generate, Then Critique: Sync to Async

You need to convert this synchronous downloader to async. An AI produced the version below.

Original (synchronous):
```python
import time

def download(url):
    print(f"Starting {url}")
    time.sleep(1)       # simulate network delay
    print(f"Done {url}")
    return f"data from {url}"

def download_all(urls):
    return [download(url) for url in urls]

urls = [f"https://example.com/{i}" for i in range(5)]
results = download_all(urls)      # takes ~5 seconds
```

AI-generated async version:
```python
import asyncio
import time

async def download(url):
    print(f"Starting {url}")
    time.sleep(1)       # simulate network delay
    print(f"Done {url}")
    return f"data from {url}"

async def download_all(urls):
    tasks = [download(url) for url in urls]
    return await asyncio.gather(*tasks)

urls = [f"https://example.com/{i}" for i in range(5)]
results = asyncio.run(download_all(urls))   # should take ~1 second
```

Task
- Run the AI's version with 5 URLs. Does it take ~1 second or ~5 seconds?
- The AI made a classic mistake. Find it and fix it.
- After fixing, verify that all 5 downloads run concurrently (~1 second total).
- Write a short checklist (3–5 items) of things to look for when reviewing AI-generated
  async code.

Discuss
- Why is `time.sleep` inside `async def` such a common AI error?
- What other blocking calls might hide inside AI-generated async code? (Think: file I/O,
  `requests.get`, database queries.)

---

### 👉 Task 'AI Snapshot' – Generate, Then Critique: Your Own Code

This is an open-ended task. Use an actual AI tool for it.

Task
- Pick any synchronous function you wrote in a previous unit — for example, the timer
  from 'Ancestor Clove', file reading from 'Drowsy Pudina', or any solution from
  'Duck Corn'.
- Ask an AI to convert it to an async version.
- Review the AI's output using this rubric:

  1. **Correctness** — Does it actually run? Are all coroutines `await`ed?
  2. **Concurrency** — Does the code actually benefit from being async, or is it just
     syntactic decoration on sequential logic?
  3. **Blocking calls** — Are there hidden `time.sleep()`, synchronous file I/O, or
     other blocking calls lurking inside `async def`?
  4. **Error handling** — Does the async version handle exceptions properly, or do errors
     vanish silently into unawaited coroutines?

- Write down your findings and be prepared to share them with the group.

Discuss
- Was the AI's conversion useful, or did it introduce more problems than it solved?
- For which of your previous tasks does async actually make sense?

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

## Comprehension Check

General
- What are the basic ideas behind 'async'?
- In what use cases can you expect to be faster than in a synchronous version?
- Why should blocking calls be avoided inside `async` functions?
- What does `await` do in an async function?

---
