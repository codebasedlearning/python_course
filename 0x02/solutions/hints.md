# Unit 0x02 – AI Hints

## Hints

### AI 'Off-By-One Imp' – Averages

- Correct idea: divide by `len(grades)` (each student's subjects), not `len(GRADES)`.
- Bug in Answer A: uses `len(GRADES)` which is the number of students.
- Quick test: Alice should be `85.0`, Bob `47.0` (from the task description).

### AI 'Off-By-One Imp' – Sorting

- Correct idea: sort by values, not keys: `sorted(average_grades, key=average_grades.get,
  reverse=True)`.
- Bug in Answer A: `sorted(average_grades)` sorts by names.
- Quick test: first name should be `Charlie` (highest average).

### AI 'Off-By-One Imp' – Debug With AI: breakpoint() vs print

- The AI's diagnosis (operator precedence) is wrong — adding parentheses doesn't fix it.
- Real bug: `count` is never incremented inside the loop. It stays `0`.
- Using `breakpoint()` and typing `p count` reveals `0` instantly.
- When `breakpoint()` beats `print()`: when you need to inspect multiple variables
  interactively; when you need to step through code.

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
- Q: What is `pytest` and how does it discover test functions? <br>
  A: A test framework; it discovers functions named `test_*` in files named `test_*.py`.
- Q: What does `breakpoint()` do and when would you use it instead of `print()`? <br>
  A: It drops into pdb; use it to inspect multiple variables interactively or step through code.
