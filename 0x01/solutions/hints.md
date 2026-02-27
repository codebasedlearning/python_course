# Unit 0x01 – AI Hints

## Hints

### AI 'Off-By-One Imp'

- Correct idea: the guard runs only when the file is executed as a script, not when imported.
- Bug in Answer B: it claims the guard prevents all code from running; top-level code still runs on
  import.
- Quick test: importing the module should not run the guarded code, but top-level statements still
  execute.

### AI 'Off-By-One Imp'

- Correct idea: keep looping until an empty line and catch `ValueError`.
- Bug in Answer B: missing `try`/`except` for invalid input.
- Quick test: input `x` should not crash the program.

### 'Comprehension Check'

- Q: What ways can you run a Python program (script, module, REPL, IDE, notebook)? <br>
  A: Script with `python file.py`, module with `python -m pkg`, REPL/interactive shell, IDE run, or
  a notebook.
- Q: What is `uv` used for in Python projects? <br>
  A: It manages Python versions, virtual environments, dependencies, and runs scripts.
- Q: What does the term “PEP” stand for, and why does it matter? <br>
  A: Python Enhancement Proposal; it defines standards and language evolution decisions.
- Q: Who created Python? <br>
  A: Guido van Rossum.
- Q: What does indentation mean in Python code, and why is it important? <br>
  A: Indentation defines code blocks and is part of Python syntax.
- Q: What does “Pythonic” mean (the “Pythonic way”)? <br>
  A: Idiomatic, readable, and explicit Python style following common conventions.
- Q: What’s the difference between `import x` and `from x import y`? <br>
  A: `import x` brings in the module; `from x import y` binds a name directly in the current
  namespace.
- Q: What comment styles can you use in Python? <br>
  A: Use `#` for line comments; triple-quoted strings serve as docstrings and can be used as block
  comments.
- Q: Which primitive/built-in scalar types do you know? <br>
  A: `int`, `float`, `bool`, `str`, and `NoneType` (via `None`).
- Q: Which container/collection types do you know? <br>
  A: `list`, `tuple`, `dict`, `set`, `frozenset`, and `range`.
- Q: What is “unpacking” (e.g., tuple/list unpacking, `*args`, `**kwargs`)? <br>
  A: Assigning iterable elements to variables or expanding arguments with `*` and `**`.
- Q: What is string interpolation in Python (e.g., f-strings, `format`)? <br>
  A: Embedding values into strings using f-strings, `str.format`, or `%` formatting.
- Q: What is a named parameter / keyword argument? <br>
  A: Passing arguments by name (e.g., `f(x=1)`) for clarity and reordering.
- Q: What does the `__name__` variable mean? <br>
  A: It is the module name; it is `__main__` when the file runs as a script.
- Q: How do you handle exceptions in Python (`try` / `except` / `else` / `finally`, raising)? <br>
  A: Use `try/except` for handling, `else` for success path, `finally` for cleanup, and `raise` to
  throw.
- Q: What is the purpose of `if __name__ == "__main__":` compared to code that runs on import? <br>
  A: It runs code only when the file is executed directly, not when imported.
- Q: How do you document modules and functions in Python (docstrings)? <br>
  A: Use triple-quoted docstrings right after the module, class, or function definition.
- Q: What is a virtual environment and why do we use it? <br>
  A: An isolated environment for project dependencies to avoid conflicts.
- Q: What is `pyproject.toml` used for in a Python project? <br>
  A: It declares project metadata, dependencies, and build configuration.

