[© 2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x0c` – Async and Descriptors


## Topics covered

- async, await
- Descriptors


## Terms

Many terms and definitions related to multitasking, threading, or concurrency 
are language-independent (language agnostic or language neutral). If this is 
a new topic for you, do not miss the [video](https://www.youtube.com/watch?v=GNMDHr8hvSM) on processes and threads.

You have to be careful where peculiarities of the programming language or 
library come into play. For example, when you create a thread, sometimes it 
will be started directly, but sometimes it will not, and you will have 
to do it yourself.

Python-specific information on threading can be found here:
[Python docs](https://docs.python.org/3/library/threading.html),
[Python gloassary](https://docs.python.org/3/glossary.html),
[Realpython intro](https://realpython.com/intro-to-python-threading),
[Superfastpython guide](https://superfastpython.com/threading-in-python/).

Here are a couple of terms from [Realpython](https://realpython.com/intro-to-python-threading), 
in particular in relation to `async`, `await` and AsyncIO.

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
2) Install a (free-threading-Python)[https://docs.python.org/3/howto/free-threading-python.html] in a virtual environment and compare
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

### 👉 Task 'Exam Preparation' 

Take a look at the topics covered and think about how you can prepare.

#### Course Content

#### Unit 0x01
- General structure of a Python program, e.g.
  - comments, imports and modules, doc-strings, role of whitespaces
- Examples with Python basics, e.g.
  - primitives (int, float, string, bool)
  - built-in containers (list, tuple, dict)
  - type hints
  - control flow (if, while, for, try-except)
  - function calls with named parameters
  - console input and output
  - variable destruction
- Pythonic way, e.g. 'main'-guard

#### Unit 0x02
- Primitives
- Collections
- Control-flow
- Function calling

#### Unit 0x03
- Classes
- Attributes
- Properties
- Member functions
- Class functions
- Operators
- Single inheritance

#### Unit 0x04
- Advent of Code-puzzles

#### Unit 0x05
- GroPro-tasks

#### Unit 0x06
- Typing, nominal typing, subtyping, duck typing, structural typing
- Single and multiple inheritance, method resolution order MRO
- Inheritance vs. composition

#### Unit 0x07
- Iterators
- Generators

#### Unit 0x08
- Scopes and LEGB rule
- Lambdas
- File io
- Context managers
- Match

#### Unit 0x09
- Test Exam

#### Unit 0x0a
- Decorators
  - with parameters
  - with return values
  - with default values
  - as classes
  - for classes

#### Unit 0x0b
- Threads
- Libs
  - Unit tests
  - Databases
  - SciPy and NumPy
  - MS Exchange
  - ChatGPT
  - Timing

#### Unit 0x0c
- async, await
- Descriptors

#### Unit 0x0d
- ast
- dis
- meta classes

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

### 👉 Comprehension Check – Talk with your Neighbor

General
- What are the basic ideas behind 'async'?
- In what use cases can you expect to be faster than in a synchronous version?

---

### 👉 Lecture Check - Online Questionare

- Please participate in the survey: [Slido](https://wall.sli.do)

---

End of `Unit 0x0c`
