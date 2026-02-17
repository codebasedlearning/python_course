# Unit 0x08 – AI Hints

## Hints

### Task 'AI Snapshot' – Thread Safety

- Correct idea: `counter += 1` is not atomic; use `threading.Lock`.
- Bug in Answer B: the GIL does not make increments safe.
- Quick test: run multiple threads and compare expected vs actual count.

### Task 'AI Snapshot' – Threads vs CPU

- Correct idea: threads help with IO-bound workloads.
- Bug in Answer B: CPU-bound work is limited by the GIL; use processes instead.
- Quick test: compare CPU-heavy workloads with threads vs processes.

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

