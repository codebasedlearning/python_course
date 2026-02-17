# Unit 0x02 – AI Hints

## Hints

### Task 'AI Snapshot' – Averages

- Correct idea: divide by `len(grades)` (each student’s subjects), not `len(GRADES)`.
- Bug in Answer A: uses `len(GRADES)` which is the number of students.
- Quick test: Alice should be `85.0`, Bob `47.0` (from the task description).

### Task 'AI Snapshot' – Sorting

- Correct idea: sort by values, not keys: `sorted(average_grades, key=average_grades.get,
  reverse=True)`.
- Bug in Answer A: `sorted(average_grades)` sorts by names.
- Quick test: first name should be `Charlie` (highest average).

### Task 'Comprehension Check'

- Q: What are the known primitive data types and containers? <br>
  A: Primitives: `int`, `float`, `bool`, `str`; containers: `list`, `tuple`, `dict`, `set`,
  `frozenset`, `range`.
- Q: What are some important differences between containers? <br>
  A: Mutability, ordering, uniqueness, and key/index access (e.g., list vs set vs dict).
- Q: What is the difference between '==' and 'is'? <br>
  A: `==` checks equality; `is` checks identity (same object).
- Q: What does 'short-circuiting' mean? <br>
  A: Boolean evaluation stops as soon as the result is known (`and`/`or`).
- Q: What is the difference between python-int and ints in other languages? <br>
  A: Python `int` is an arbitrary-precision object, not fixed-size primitive.
- Q: What does 'slicing' mean? <br>
  A: Selecting a subsequence with `seq[start:stop:step]`.
- Q: Is copying a list a shallow copy or a deep copy? <br>
  A: It is shallow; nested objects are shared unless deep-copied.
- Q: What is the difference between a list and a tuple? <br>
  A: Lists are mutable; tuples are immutable (and can be hashable).
- Q: What are 'frozensets' for? <br>
  A: Immutable sets; useful as dict keys or set elements.
- Q: What do I need to be aware of with a function's default arguments? <br>
  A: Defaults are evaluated once; mutable defaults can leak state.
- Q: Why is `range` not the same as a list? <br>
  A: `range` is a lazy sequence object, not a stored list.
- Q: When would you use `any()` versus `all()`? <br>
  A: `any()` for at least one true; `all()` for every element true.

