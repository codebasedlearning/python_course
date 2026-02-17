[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x08` – Threads and Libs

## Overview

This unit introduces threads and selected libraries, covering concurrency concepts and practical tooling.

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
a new topic for you, do not miss the [video](https://www.youtube.com/watch?v=GNMDHr8hvSM) on processes and threads.

You have to be careful about the peculiarities of the programming language or 
library you are using. For example, when you create a thread, sometimes it 
will be started directly, but sometimes it will not, and you will have 
to do it yourself.

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

---

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

---

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

---

### 👉 Task 'Marsh Wintercress' 

Revise the `f_messaging` example to allow multiple producers and consumers 
to be involved in exchanging messages.

1) Design appropriate consumer, producer, and hold-my-messages classes. 
   Also allow more than one message to be ready to be picked up.
   - It is crucial that you take care of the thread safety of your data structures. 
   - Use so-called 'Condition Objects' (or 'Condition Variables') to synchronize. 
     Details can be found [here](https://docs.python.org/3/library/threading.html#condition-objects).

---

### 👉 Task 'Cave Betty' 

> Without a proposed solution.

  - See if you can come up with a nice and sensible way to parallelize 
    the prime sieve. 
  - Measure a serial and a parallel variant.

---

### 👉 Task 'Creepy Wineberry' 

> Without a proposed solution.

- Set up a database for your own and perform any SQL statements.

---

### 👉 Task 'Pest Cap' 

> Without a proposed solution.

  - Query mail, contact and/or calendar items from your (?) Microsoft 
    Exchange account, if available.

---

### 👉 Task 'Red Castle' 

> Without a proposed solution.

  - Design a class or a function and write some unit tests.

---

### 👉 Task 'Self-Study'

- Review all snippets from the lecture. Ask if there are any outstanding questions.

---

### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do or have questions about?

---

### 👉 Task 'AI Snapshot' – Thread Safety

Prompt
- "Is this safe without a lock?"

```python
counter = 0

def worker():
    global counter
    for _ in range(100000):
        counter += 1
```

AI Answer A
Not safe; protect the increment with a `threading.Lock`.

AI Answer B
Safe because the GIL makes increments atomic.

Discuss
- Which answer is correct and why?
- Why is `counter += 1` not atomic?

---

### 👉 Task 'AI Snapshot' – Threads vs CPU

Prompt
- "Which workload benefits most from threads in Python: IO-bound or CPU-bound?"

AI Answer A
IO-bound workloads benefit most from threads.

AI Answer B
CPU-bound workloads benefit most from threads.

Discuss
- Which answer is correct?
- When would you choose processes instead?

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

## Comprehension Check

General
- What is special in Python concerning parallel execution?
- What is the difference between a process and a thread?
- What is a mutex for?
- What is a race condition in threaded code?
- What is the GIL and how does it affect CPU-bound threads in Python?

---
