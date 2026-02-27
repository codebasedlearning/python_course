# Unit 0x09 – AI Hints

## Hints

### AI 'Off-By-One Imp' – Generate, Then Critique: Sync to Async

- Classic mistake: the AI used `time.sleep(1)` inside `async def` — this blocks the event loop.
- Fix: replace `time.sleep(1)` with `await asyncio.sleep(1)`.
- After fixing, all 5 downloads run concurrently (~1 second total instead of ~5).
- Checklist for AI async code: (1) no blocking calls, (2) all coroutines awaited,
  (3) actual concurrency benefit, (4) proper error handling.

### AI 'Off-By-One Imp' – Generate, Then Critique: Your Own Code

- This is an open-ended task — no single answer.
- Common AI mistakes: blocking calls hidden in async def, unawaited coroutines,
  async that adds syntax overhead with no actual concurrency benefit.
- Not all code benefits from async — only IO-bound tasks with multiple concurrent operations.

### Task 'Comprehension Check'

- Q: What are the basic ideas behind 'async'? <br>
  A: Cooperative multitasking with awaitable operations and an event loop.
- Q: In what use cases can you expect to be faster than in a synchronous version? <br>
  A: IO-bound concurrency (network, disk, many simultaneous tasks).
- Q: Why should blocking calls be avoided inside `async` functions? <br>
  A: They block the event loop and prevent other tasks from running.
- Q: What does `await` do in an async function? <br>
  A: It suspends the coroutine until the awaited task completes.
