# Unit 0x06 – AI Hints

## Hints

### AI 'Off-By-One Imp' – Debug With AI: Late Binding

- The AI's diagnosis (off-by-one in `range`) is completely wrong.
- Real problem: late binding — all lambdas capture the SAME `i` variable, which is `4` after the loop.
- Fix 1: `lambda i=i: print(...)` — default argument binds eagerly.
- Fix 2: `functools.partial(print, f"Button {i}")` — also binds eagerly.

### AI 'Off-By-One Imp' – Debug With AI: Scope Error

- The AI's fix (`global count`) "works" but breaks independent counters: both share one global.
- Correct fix: `nonlocal count` inside `increment`.
- `get()` works without `nonlocal` because it only READS `count`; `increment` tries to WRITE it.
- LEGB: `count` lives in the Enclosing scope; `global` moves it to Global scope.

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
