# Unit 0x06 – AI Hints

## Hints

### Task 'AI Snapshot' – Late Binding

- Correct result: `[2, 2, 2]` because each lambda captures the same `i`.
- Bug in Answer B: it assumes early binding per iteration.
- Quick fix: use `lambda i=i: i` to bind the current value.

### Task 'AI Snapshot' – `nonlocal`

- Correct fix: add `nonlocal n` inside `inc`.
- Bug in Answer B: it tries to assign to `n` without declaring scope.
- Quick test: calling `inc()` should increment without an `UnboundLocalError`.

### Task 'Comprehension Check'

- Q: What is the main reason behind a 'context manager'? <br>
  A: To guarantee setup/teardown and safe resource management with `with`.
- Q: What is a 'scope,' and what kind of scopes do you know? <br>
  A: A scope is where names are visible; local, enclosing, global, built-in.
- Q: What happens exactly when you import something? <br>
  A: Python executes the module once, caches it in `sys.modules`, and binds names.
- Q: What does `nonlocal` do inside a nested function? <br>
  A: It binds assignments to a variable in the nearest enclosing scope.
- Q: What does LEGB stand for? <br>
  A: Local, Enclosing, Global, Built-in.

