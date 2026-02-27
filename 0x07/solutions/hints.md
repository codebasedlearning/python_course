# Unit 0x07 – AI Hints

## Hints

### AI 'Off-By-One Imp' – Three Answers: @logged Decorator

- Ranking worst→best: B (no metadata), A (partial metadata copy), C (`functools.wraps`).
- Answer A manually copies `__name__` but misses `__doc__`, `__module__`, `__qualname__`, `__wrapped__`.
- Answer B breaks `pytest` discovery and `sphinx` documentation because `__name__` is `wrapper`.
- Most AIs produce B or C because A (manual partial copy) is uncommon in training data.

### AI 'Off-By-One Imp' – Import-Time Side Effects

- `logging.info("Registered: ...")` runs at IMPORT time, not call time — it fires when `@tracked` decorates.
- Running the file without calling anything prints two "Registered" lines.
- `call_count` is per-function (each decorator call creates its own closure).
- Import-time side effects are acceptable for registration (like `@example` in Moon Collard) but not for IO/logging.

### Task 'Comprehension Check'

- Q: What kind of decorators do you know? <br>
  A: Simple function decorators, parameterized decorators, and class-based decorators.
- Q: What is the reason for using `functools`? <br>
  A: It provides utilities like `wraps`, `lru_cache`, and higher-order tools.
- Q: Why is `functools.wraps` recommended in decorators? <br>
  A: It preserves metadata like `__name__`, `__doc__`, and annotations.
- Q: When would you use a decorator with parameters? <br>
  A: When the decorator needs configuration, e.g., `@retry(times=3)`.
