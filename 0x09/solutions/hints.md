# Unit 0x09 – AI Hints

## Hints

### Task 'AI Snapshot' – `asyncio.sleep`

- Correct idea: use `await asyncio.sleep(...)` inside async code.
- Bug in Answer B: `time.sleep(...)` blocks the event loop.
- Quick test: run two tasks; blocking sleep prevents concurrency.

### Task 'AI Snapshot' – Missing `await`

- Correct idea: `await fetch()` runs the coroutine.
- Bug in Answer B: it prints a coroutine object instead of a value.
- Quick test: add `await` and confirm `42` is printed.

### Task 'Comprehension Check'

- Q: What are the basic ideas behind 'async'? <br>
  A: Cooperative multitasking with awaitable operations and an event loop.
- Q: In what use cases can you expect to be faster than in a synchronous version? <br>
  A: IO-bound concurrency (network, disk, many simultaneous tasks).
- Q: Why should blocking calls be avoided inside `async` functions? <br>
  A: They block the event loop and prevent other tasks from running.
- Q: What does `await` do in an async function? <br>
  A: It suspends the coroutine until the awaited task completes.

