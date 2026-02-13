[© 2025, A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)
<hr>

# Python Course – Welcome

Good to have you here! 👍 

To get started, you should first clone this project and read the docs in this order:
- [Background](./docs/python_background.pdf)
- [Setup](./docs/python_setup.pdf)
- [IDE](./docs/python_ide.pdf)
- [Units](./docs/python_units.pdf)

Your first goal should be to have the Python ecosystem in place and a working Python installation at the end. After that, you can start following the README in the units.

<hr>

## Content

### Basics
- Unit 0x01 – Preparation Homework + Introduction + Examples
- Unit 0x02 – Types + Control Flow
- Unit 0x03 – Classes, single inheritance

### Practical
- Unit 0x_tra_gropros – GroPros
- Unit 0x_tra_puzzles – Puzzles incl. Exam

### More 
- Unit 0x04 – Typing + inheritance + protocol + mixin
- Unit 0x05 – iterators + generators
- Unit 0x06 – scope + lambdas + closures
- Unit 0x07 – Decorators

### Sophisticated
- Unit 0x08 – threads + libs
- Unit 0x09 – asyncio + descriptors

### Prep
- Unit 0x_tra_test – Exam

### Advanced
- Unit 0x_tra_unit – Ast + Dis + Meta Classes


## References

Usually you can find information about a specific Python feature in the 
official documentation.
  - https://docs.python.org/3/
  - https://docs.python.org/3/tutorial/introduction
  - https://docs.python.org/3/tutorial
  - https://docs.python.org/3/reference
  - https://docs.python.org/3/library
  - https://peps.python.org/pep-0000


## Interactive Python | REPL

The Python application `python` or `python3` has two modes: script and interactive. 
- In normal or script mode, the .py scripts are executed in the Python interpreter. 
- In interactive mode, or interactive shell, one can enter Python commands, 
  e.g. this easter egg `import this`.
- The whole process is also known as a REPL, standing for Reading (the input), 
  Evaluating (the code), Printing (any output), Looping back to step one.

With a view to professional product development, we focus on working with an IDE.


---
  Strong candidates — clearly optional for the core progression

  1. 0x06/a_globals_locals.py (178 lines, no functions in main)
  globals() and locals() dictionaries. This is metaprogramming/debugging
  knowledge, not core scope understanding. The essential scope material is
  already in c_scope_legb.py. Most programmers never call globals() directly.

  2. 0x06/d_scope_non_legb.py (102 lines, 3 functions)
  Comprehension scoping quirks — the fact that comprehension variables don't
  leak into the enclosing scope. Important edge case, but students can learn
  LEGB first and discover this later. It's a "gotcha" file, not a "how things
  work" file.

  3. 0x07/d_decorator_classes.py (103 lines, 1 function)
  Using classes as decorators (with __call__). Function-based decorators (files
  a–c) handle 95% of real-world use cases. This is a pattern, not a core
  concept. The one function in main is also a sign it's thin.

  4. 0x07/e_decorated_classes.py (75 lines, 2 functions)
  Decorating classes (singleton pattern, adding __str__). Interesting patterns,
  but @dataclass (already in 0x03) is the only class decorator most programmers
  encounter regularly. Singleton via decorator is a trivia question, not daily
  knowledge.

  5. 0x09/d_chains.py (99 lines, 1 sync + 1 async function)
  Callback hell → promise chains → async. The transformation is instructive but
  somewhat dated — the callback pattern is a JavaScript relic. The core async
  concepts are already solid in a_async_basics.py, b_task_group.py, and
  c_async_cooking.py.

  ---
  Medium candidates — depends on how tight you want the core

  6. 0x06/i_match.py (158 lines, 2 functions)
  Structural pattern matching (3.10+). Powerful feature, but experienced
  programmers already have if/elif muscle memory. Match is most useful for
  parsing ASTs and protocol messages — not beginner-to-intermediate territory.
  Could be study_ without losing the course arc.

  7. 0x06/f_reduce_filter_map_gen.py: the reduce part specifically
  filter() and map() are essential functional tools. But reduce is rarely used
  in modern Python — Guido himself argued against it, and it was moved from
  builtins to functools for that reason. The reduce section could live in a
  study_ file while filter/map stays.

  8. 0x03/a_class_basics.py: the monkey patching section (within the 431-line,
  10-function monster)
  Monkey patching is a controversial technique that most style guides actively
  discourage. It's in a_class_basics.py because it demonstrates dynamic
  attribute assignment, but students might get the wrong idea that it's an
  encouraged pattern. Better as a study_ "here's what you can do but probably
  shouldn't."

  9. 0x03/b_members.py: the backing field / name mangling deep dive
  The basic @property pattern is essential. But the deep dive into _name vs
  __name name mangling and the "Python has no real private" discussion is more
  cultural than practical. The core message ("use _ prefix as a convention")
  needs one paragraph, not a whole section.

  ---
  Observation on the heaviest files

  The real density problem is in 0x03:
  File: a_class_basics.py
  Lines: 431
  Functions: 10
  Issue: Covers creation, init, str/repr, class vs instance data, access
    modifiers, monkey patching — that's 3 files worth of content
  ────────────────────────────────────────
  File: b_members.py
  Lines: 316
  Functions: 5
  Issue: Properties, backing fields, name mangling, class internals
  ────────────────────────────────────────
  File: c_operations.py
  Lines: 270
  Functions: 4
  Issue: Operators, equality, hashing, total_ordering
  If you moved monkey patching and the str/repr deep dive from
  a_class_basics.py, and the name mangling deep dive from b_members.py, you'd
  shave ~150 lines off the two heaviest files without losing any core OOP
  knowledge.

  0x06 is the other dense unit — 10 main files is a lot. Moving
  a_globals_locals.py, d_scope_non_legb.py, and optionally i_match.py would
  bring it down to 7, which is more digestible.


