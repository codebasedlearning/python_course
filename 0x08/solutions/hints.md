# Unit 0x08 – AI Hints

## Hints

### Task 'Race Bark'

- A shared counter without a lock is a classic race.
- Use `threading.Lock` or a `Queue` to protect shared data.
- Document the non-deterministic symptom and the fix you chose.

### AI 'Off-By-One Imp' – Debug With AI: Race Condition

- The AI's fix (plain `int` + `global`) does NOT fix the race condition — `+=` is still non-atomic.
- `counter["value"] += 1` decomposes to load → add → store; threads can interleave between steps.
- Correct fix: use `threading.Lock` to serialize the increment.
- The GIL protects Python internals, not YOUR data structures.

### AI 'Off-By-One Imp' – Debug With AI: Just Add More Threads

- Adding more threads (16, 32) does NOT help CPU-bound tasks because of the GIL.
- `fib(30)` is CPU-bound; threads take turns on the GIL, giving no speedup.
- Fix: use `multiprocessing.Pool` for CPU-bound work — each process has its own GIL.
- Replace `fib(30)` with `time.sleep(0.5)` (IO-bound) and threads DO help because sleep releases the GIL.

### Task 'Comprehension Check'

- Q: What is special in Python concerning parallel execution? <br>
  A: The GIL limits true CPU-bound parallelism in threads.
- Q: What is the difference between a process and a thread? <br>
  A: Processes have separate memory; threads share memory within one process.
- Q: What is a mutex for? <br>
  A: A lock to protect shared data from concurrent access.
- Q: What is a race condition in threaded code? <br>
  A: Unsynchronized access causes unpredictable results.
- Q: What is the GIL and how does it affect CPU-bound threads in Python? <br>
  A: The Global Interpreter Lock allows only one thread to run bytecode at a time, limiting
  CPU-bound threads.
