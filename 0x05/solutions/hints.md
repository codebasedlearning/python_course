# Unit 0x05 – AI Hints

## Hints

### Task 'AI Snapshot' – Lazy vs Eager

- Correct idea: `(x*x for x in range(10))` is lazy; `[x*x for x in range(10)]` is eager.
- Bug in Answer B: it ignores laziness and memory differences.
- Quick test: a generator does not compute values until iterated.

### Task 'AI Snapshot' – Iterator Output

- Correct result: `list(CountDown(3))` is `[2, 1, 0]`.
- Bug in Answer B: it assumes the first yield is the initial value.
- Quick test: print the list to see the off-by-one effect.

### Task 'Comprehension Check'

- Q: Describe 'iterators' and 'generators.' What are the benefits? <br>
  A: They produce values lazily, enabling low memory usage and streaming pipelines.
- Q: Are there any use cases you see for your projects or code? <br>
  A: Large files, streaming data, pipelines, or incremental computations.
- Q: What is the difference between `iter()` and `next()`? <br>
  A: `iter()` returns an iterator; `next()` retrieves the next item.
- Q: What happens when a generator is exhausted? <br>
  A: It raises `StopIteration` and cannot be iterated further unless recreated.
- Q: What is a generator expression? <br>
  A: A lazy expression like `(x for x in items)` that returns a generator.

