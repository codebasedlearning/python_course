# Unit 0x03 – AI Hints

## Hints

### AI 'Off-By-One Imp' – Class vs Instance

- Correct result: `Counter.count` stays `0`, `c1.count` becomes `1`, `c2.count` stays `0`.
- Bug in Answer B: it assumes updating `c1.count` mutates the class attribute for all instances.
- Quick test: print `Counter.count`, `c1.count`, and `c2.count` after the increment.

### AI 'Off-By-One Imp' – Property Validation

- Correct idea: enforce the constraint in a property setter and raise `ValueError` below `-273.15`.
- Bug in Answer B: no validation; `Temperature(-300)` is allowed.
- Quick test: constructing `Temperature(-300)` should raise.

### Task 'Comprehension Check'

- Q: Any suggestions for working with an AI agent? <br>
  A: Give precise requirements, verify outputs, and test before trusting results.
- Q: What are `types` for in Python and do you use them? <br>
  A: They provide hints for readability and tooling; Python does not enforce them at runtime.
- Q: What are `args` and `kwargs`? <br>
  A: `*args` collects extra positional arguments; `**kwargs` collects keyword arguments.
- Q: Do you know the difference between a 'regular' member function, a static method and a class
  method? <br>
  A: Regular methods take `self`, static methods take no implicit arg, class methods take `cls`.
- Q: What kind of 'dunder' functions do you know and what are they for? <br>
  A: Special methods like `__init__`, `__str__`, `__len__` define object behavior.
- Q: What is the idea of a data class? <br>
  A: It auto-generates boilerplate like `__init__`, `__repr__`, and comparisons for data containers.
- Q: What is the difference between `__str__` and `__repr__`? <br>
  A: `__str__` is user-friendly; `__repr__` is developer-focused and unambiguous.
- Q: What is the difference between a class attribute and an instance attribute? <br>
  A: Class attributes are shared; instance attributes belong to each object.
- Q: What is a property and why would you use it? <br>
  A: A property lets you add validation or computed access while keeping attribute syntax.
