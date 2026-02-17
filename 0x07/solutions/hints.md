# Unit 0x07 – AI Hints

## Hints

### Task 'AI Snapshot' – `functools.wraps`

- Correct idea: use `@functools.wraps(fn)` to preserve `__name__` and `__doc__`.
- Bug in Answer B: metadata is lost without `wraps`.
- Quick test: check `decorated.__name__`.

### Task 'AI Snapshot' – Decorator Timing

- Correct idea: `decorating f` is printed at definition/import time.
- Bug in Answer B: it assumes decoration happens on call.
- Quick test: import the module and see output before any call to `f()`.

### Task 'Comprehension Check'

- Q: What kind of decorators do you know? <br>
  A: Simple function decorators, parameterized decorators, and class-based decorators.
- Q: What is the reason for using `functools`? <br>
  A: It provides utilities like `wraps`, `lru_cache`, and higher-order tools.
- Q: Why is `functools.wraps` recommended in decorators? <br>
  A: It preserves metadata like `__name__`, `__doc__`, and annotations.
- Q: When would you use a decorator with parameters? <br>
  A: When the decorator needs configuration, e.g., `@retry(times=3)`.

