[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x08` – Threads and Libs


## Overview

This unit introduces threads and selected libraries, covering concurrency concepts and practical
tooling.


### Focus

Build awareness of Python's concurrency model and apply libraries safely and effectively.


## Topics

- Threads and concurrency basics
- Locks and shared-state pitfalls
- Selected libraries (tests, databases, NumPy/SciPy, Exchange, ChatGPT)
- Timing and profiling


## Terms

Many terms and definitions related to multitasking, threading, or concurrency 
are language-independent (language agnostic or language neutral). If this is 
a new topic for you, do not miss the [video](https://www.youtube.com/watch?v=GNMDHr8hvSM) on
processes and threads.

You have to be careful about the peculiarities of the programming language or 
library you are using. For example, in Python a thread does not start when it is created; you must
call `start()` explicitly.

Python-specific information on threading can be found here:
[Python docs](https://docs.python.org/3/library/threading.html),
[Python glossary](https://docs.python.org/3/glossary.html),
[Realpython intro](https://realpython.com/intro-to-python-threading),
[Superfastpython guide](https://superfastpython.com/threading-in-python/).

Here are a couple of terms from [Realpython](https://realpython.com/intro-to-python-threading).


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


## Tasks


### 👉 Task 'Self-Study'

- Review all snippets from the lecture.
- Run and understand all content from scripts that start with `study_` (if any). 
- Ask if there are any outstanding questions, or if you miss an idea.


### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do
  or have questions about?


### 👉 Task 'Twin Tongue' 

Mathematical problems where either the algorithms or the data domains can 
be divided are a typical application of parallel algorithms. An example is the
[Trapezregel](https://de.wikipedia.org/wiki/Trapezregel)
or [Trapezoidal rule](https://en.wikipedia.org/wiki/Trapezoidal_rule).

Use the function given in the example and the range `[a=0.0, b=2.0]` as 
a benchmark.

```
    math.pow(3, 3 * x - 1))
    exact_0_2 = 728 / (9 * math.log(3))
```

1) Implement the algorithm once serially and once parallelly using a technique
   of your choice, e.g., a ThreadPoolExecutor with a set of Workers. 
2) Measure both solutions and try to find a configuration where the parallel 
   version is faster.


### 👉 Task 'Yellow Hemp' 

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

1) Read all the files and check that the given sum is correct in a serial 
   and a parallel version. Use different variants, e.g., a 'ThreadPoolExecutor.'


### 👉 Task 'Marsh Wintercress' 

Revise the `f_messaging` example to allow multiple producers and consumers 
to be involved in exchanging messages.

1) Design appropriate consumer, producer, and hold-my-messages classes. 
   Also allow more than one message to be ready to be picked up.
   - It is crucial that you take care of the thread safety of your data structures. 
   - Use so-called 'Condition Objects' (or 'Condition Variables') to synchronize. 
     Details can be found
     [here](https://docs.python.org/3/library/threading.html#condition-objects).


### 👉 Task 'Race Bark' (Race Condition Post-Mortem)

- Create or locate a small race condition in one of your thread exercises.
- Write a short reproduction guide: expected vs actual behavior.
- Fix the issue and document the synchronization primitive you used.


### 👉 Task 'Cave Betty' 

> Without a proposed solution.

  - See if you can come up with a nice and sensible way to parallelize 
    the prime sieve. 
  - Measure a serial and a parallel variant.


### 👉 Task 'Creepy Wineberry' 

> Without a proposed solution.

- Set up a database for your own and perform any SQL statements.


### 👉 Task 'Pest Cap' 

> Without a proposed solution.

  - Query mail, contact and/or calendar items from your (?) Microsoft 
    Exchange account, if available.


### 👉 Task 'Red Castle' 

> Without a proposed solution.

  - Design a class or a function and write some unit tests.


### 👉 Project 'Moving Blizzard' — Part 8

> Continued from Part 7. Sensor polling is IO-bound (network delay) — perfect for threads.
Compare serial vs. threaded performance.

Topics: `ThreadPoolExecutor`, `as_completed`, `threading.Lock`, serial vs. parallel

Part 1
- Write `poll_sensor(sensor_id, delay=0.3)` that simulates a network call with
  `time.sleep(delay)` and returns a list of `Reading` objects.
- Write `poll_serial(sensor_ids)` that polls sensors one by one and times the total.

Part 2
- Create a `SensorCollector` class with a `threading.Lock` to safely accumulate results
  from multiple threads.
- Write `poll_threaded(sensor_ids)` using `ThreadPoolExecutor` and `as_completed`.

Part 3
- Compare serial vs. threaded execution time. Compute the speedup factor.
- Verify that both versions return identical data.
- Explain why the GIL does not prevent the speedup here (hint: `time.sleep` releases the
  GIL).

Check
- Compare your solution with the provided one from `solutions` and an AI-generated one.


### 👉 AI 'Off-By-One Imp'

A student showed this code to an AI:

```python
import threading

counter = {"value": 0}

def worker():
    for _ in range(100_000):
        counter["value"] += 1

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter["value"])  # expected: 400_000, got: 283_417
```

The AI diagnosed: *"The problem is that you're using a dictionary instead of a simple
integer variable. Dictionary operations are not thread-safe. Replace with a plain `int`
using `global counter` and the problem will disappear."*

Task
- Apply the AI's fix (plain `int` + `global`). Run it. Does the problem disappear?
- The AI's reasoning is wrong on multiple levels. Explain why:
  - Is `counter["value"] += 1` atomic? Decompose it mentally into load → add → store.
  - Does switching to `counter += 1` with `global` change the atomicity?
- Fix the original code properly using `threading.Lock`.
- Bonus: fix it without a lock using `queue.Queue` or `threading` primitives.

Discuss
- The GIL protects Python's *internal* data structures. Why doesn't it protect *your*
  data?
- When *is* a GIL-protected operation truly atomic? (Hint: single bytecode instruction.)

[Hints](./solutions/hints.md)


### 👉 AI 'Off-By-One Imp'

A student tried to speed up a CPU-bound task with threads and asked an AI for help:

```python
import threading, time

def fib(n):
    return fib(n-1) + fib(n-2) if n > 1 else n

def run_serial():
    start = time.time()
    for _ in range(4):
        fib(30)
    return time.time() - start

def run_threaded():
    start = time.time()
    threads = [threading.Thread(target=fib, args=(30,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.time() - start

print(f"Serial:   {run_serial():.2f}s")
print(f"Threaded: {run_threaded():.2f}s")
# Both take about the same time!
```

The AI suggested: *"You need more threads. Using 4 threads for 4 tasks is not enough for
parallelism — try 16 or 32 threads to better utilize your CPU cores."*

Task
- Run the code. Are the times similar? Now follow the AI's advice and use 16 threads.
  Does it help?
- Explain why threads do not speed up CPU-bound work in CPython. What is the GIL's role?
- Rewrite `run_threaded` using `multiprocessing.Pool` instead. Measure the difference.
- Replace `fib(30)` with `time.sleep(0.5)` (simulating IO). Now compare serial vs.
  threaded. What changed and why?

Discuss
- Why is "add more threads" such a common (and wrong) AI suggestion for Python?
- When *should* you use threads in Python? Give two concrete examples.

[Hints](./solutions/hints.md)


### 👉 Homework 'Couch Potato'

- If you did not finish the essential tasks in the exercise, finish them at home.


## Comprehension Check

General
- What is special in Python concerning parallel execution?
- What is the difference between a process and a thread?
- What is a mutex for?
- What is a race condition in threaded code?
- What is the GIL and how does it affect CPU-bound threads in Python?

[Hints](./solutions/hints.md)
