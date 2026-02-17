# Unit 0x_tra_unit – AI Hints

## Hints

### Task 'AI Snapshot' – Metaclass vs Decorator

- Correct idea: use metaclasses for class creation control; decorators for simple transforms.
- Bug in Answer B: adding methods does not require a metaclass.
- Quick test: show a class decorator that adds an attribute.

### Task 'AI Snapshot' – `ast` vs `dis`

- Correct idea: `dis` inspects bytecode; `ast` parses syntax trees.
- Bug in Answer B: it swaps their roles.
- Quick test: run `dis.dis` on a function to see bytecode.

### Task 'Comprehension Check'

- Q: What does `dis` show that `ast` does not? <br>
  A: `dis` shows bytecode; `ast` shows the syntax tree.
- Q: Why might you inspect bytecode during debugging? <br>
  A: To understand what the interpreter actually executes and spot overhead.
- Q: What is a metaclass in Python? <br>
  A: It is the class of a class and controls how classes are created.

