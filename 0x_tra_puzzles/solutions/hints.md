# Unit 0x_tra_puzzles – AI Hints

## Hints

### Task 'AI Snapshot' – Shortest Path

- Correct idea: BFS guarantees shortest path in unweighted graphs.
- Bug in Answer B: DFS can find a longer path first.
- Quick test: create a grid where DFS finds a longer route than BFS.

### Task 'AI Snapshot' – Grid Parsing

- Correct idea: `grid = [list(line) for line in lines]` creates a 2D list.
- Bug in Answer B: `list(lines)` produces a list of strings, not characters.
- Quick test: check `grid[0][0]` type.

### Task 'Comprehension Check'

- Q: Why refactor after solving Part 1 and Part 2? <br>
  A: To improve readability, performance, and maintainability.
- Q: When does a reusable grid or graph helper class pay off? <br>
  A: When multiple puzzles share traversal or graph logic.
- Q: Why are small custom test cases useful for puzzles? <br>
  A: They validate logic quickly and catch edge cases early.

