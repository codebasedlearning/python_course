[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x_tra_gropros` – GroPro Setup


## Overview

This unit prepares you for GroPro-style tasks by emphasizing SOLID design principles and structured
problem solving.


### Focus

Focus on designing maintainable solutions before coding, using clear responsibilities and
abstractions.


## Topics

- SOLID design principles
- IPO approach to problem solving
- Designing maintainable solutions

> The aim is to model and solve GroPro (Grosse Programmieraufgabe IHK) problems.

> Note: the principles are not specific to Python, they must always be followed. But it's also about
what you can prepare now, so that you have a framework for the exam (IPO) and don't have to think
about everything from scratch.


## SOLID

> SOLID is a mnemonic for five fundamental principles of object-oriented software design, intended
to make code:
> - Flexible
> - Reusable
> - Maintainable
> - Scalable

It originated mainly with Robert C. Martin (Uncle Bob) and friends in the early 2000s.

> SOLID is not about writing more code. It’s about writing code that survives changes, extensions,
and teamwork.


### Definition

- S: Single Responsibility — A class should have only one reason to change.
- O: Open/Closed — Software should be open for extension, but closed for modification.
- L: Liskov Substitution — Subtypes must be substitutable for base types.
- I: Interface Segregation — Prefer many small, specific interfaces over one large one.
- D: Dependency Inversion — Depend on abstractions, not concrete implementations.


### Related to Python


#### S: Single Responsibility Principle (SRP)

A class (or function) should do one thing and do it well. In Python, this usually means:
- Keep classes focused.
- Split long functions into small helpers.
- Modules should also have a focused purpose.

('Doing just one thing' is not exactly the same as 'having one reason to change'—the former is about
behavior, and the latter is about responsibility, but the former is 95% correct and practical.)


#### O: Open/Closed Principle (OCP)

You should be able to extend a class’s behavior without modifying its source. In Python, this often
means:
- Use inheritance, composition, or higher-order functions.
- Prefer adding new classes/functions over editing old ones.


#### L: Liskov Substitution Principle (LSP)

Subclasses should behave like the parent class, without surprises. In Python:
- When you extend a base class or protocol, you must not break expectations.
- Inputs and outputs must still "make sense."

```
class Bird:
    def fly(self):
        print("Flying!")

class Duck(Bird):
    pass

class Ostrich(Bird):
    def fly(self):
        raise NotImplementedError("Ostriches can't fly!")  # BAD!
```

So `Duck` is fine, `Ostrich` violates LSP. Better design would be a `FlyingBird` and
`FlightlessBird` split, not a bad inheritance.


#### I: Interface Segregation Principle (ISP)

Users shouldn’t be forced to depend on interfaces they don’t use. In Python:
- Keep base classes small.
- Split large protocols (interfaces) into focused ones.


#### D: Dependency Inversion Principle (DIP)

Depend on abstractions, not concrete details." In Python:
- Inject dependencies via constructors or functions.
- Program to protocols / abstract classes, not implementations.

```
class Database(ABC):
    @abstractmethod
    def save(self, data): ...

class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to MySQL")

class Service:
    def __init__(self, db: Database):
        self.db = db

    def process(self, data):
        self.db.save(data)
```

This way it is easy to switch the database later. Hardcoding `MySQLDatabase` inside `Service` would
be a bad design.


### SOLID Design Checklist (Python Edition)

#### Single Responsibility
- Does this class only do one thing?
- Would I need to change this class for more than one reason?
- If yes → split it.

#### Open/Closed
- Can I extend behavior without modifying existing classes?
- Am I adding new classes/functions instead of hacking old ones?
- If not → refactor with inheritance or composition.

#### Liskov Substitution
- If I replace a parent class object with a child object, does the program still behave correctly?
- If I replace a child object with a parent object (using only parent features), does the program
  still behave correctly?
- Do all overridden methods behave consistently with expectations?
- If not → split classes or rethink inheritance.

#### Interface Segregation
- Is this interface or base class small and focused?
- Are users forced to implement methods they don’t need?
- If yes → split interfaces into smaller ones.

#### Dependency Inversion
- Is this class depending on abstractions (interfaces/protocols) rather than concrete classes?
- Can I swap implementations easily (e.g., MySQL ➔ Postgres ➔ Mock)?
- If not → introduce abstract base classes or protocols.


## Tasks


### 👉 Task 'IPO'

- Review all snippets from the lecture. Ask if there are any outstanding questions.


### 👉 Task 'GroPro'

- Choose one (or more) of the GroPros:
  - Crosswords
  - Service Stations
  - Wooden Puzzle

Try to solve the problem(s), but also try to take the SOLID principles into account.


### 👉 Task 'Tangled Reef' (Refactoring)

> The code in `solutions/tangled_reef_the_mess.py` is a small shop receipt system.
> It works. It prints correct results. It is also a disaster.

Run the file and verify that the output is correct. Then read the code carefully.

Part 1 — Identify

Find and name every SOLID violation in the `App` class. For each one:
- State which SOLID principle is violated (S, O, L, I, or D).
- Quote the specific lines or methods responsible.
- Explain *why* it is a problem (what breaks if requirements change?).

You should find violations of at least four of the five principles. Some methods
violate more than one.

Hints to get you started:
- How many *reasons to change* does the `calc` method have?
- What happens if you need a new tax category — say, "medical"?
- If you want to switch from file-based receipts to a database, how many
  methods need to change?
- What does the `do` method remind you of? Is there a better pattern?

Part 2 — Refactor

Restructure the code so that every SOLID principle is respected. Suggested
target classes (you are free to design differently):

- `Product` or a dataclass for items
- `TaxPolicy` (or a protocol) for tax calculation
- `DiscountPolicy` for discount handling
- `Receipt` or `ReceiptFormatter` for output formatting
- `ReceiptWriter` (protocol) for output destination (console, file, ...)
- `Shop` or `OrderProcessor` as the orchestrator

Rules:
- The **output must remain identical** — same numbers, same formatting.
- You may introduce abstract classes, protocols, dataclasses, or any
  pattern from the course.
- Each class should have a single, clear responsibility.

Part 3 — Reflect

- Compare the line count before and after. Is your version longer? Why is
  that acceptable (or not)?
- Pick one refactoring decision and explain how it makes the code
  *open for extension, closed for modification*.
- Could you now add a "medical" tax category without touching existing classes?


### 👉 AI 'Off-By-One Imp'

Prompt
```
Should a `ServiceStation` class handle pricing, IO, and reporting in one place?
```

AI Answer A
No. Split responsibilities into focused classes such as `PricingPolicy`, `Receipt`, and `Station`.

AI Answer B
Yes. Keep everything in one large `ServiceStation` class to reduce complexity.

Discuss
- Which answer aligns with the Single Responsibility Principle?
- What kinds of changes would break the one-class design?

[Hints](./solutions/hints.md)


### 👉 AI 'Off-By-One Imp'

Prompt
```
Should a service depend directly on `MySQLDatabase`?
```

AI Answer A
No. Depend on an abstraction (protocol/ABC) so the database can be swapped.

AI Answer B
Yes. Concrete dependencies are simpler and faster to build.

Discuss
- Which answer matches the Dependency Inversion Principle?
- What benefit do you get from depending on an abstraction?

[Hints](./solutions/hints.md)


### 👉 Homework 'Couch Potato'

- If you did not finish the essential tasks in the exercise, finish them at home.


## Comprehension Check

General
- How would you build a solution for a GroPro?
- What can you prepare in advance?
- How does the IPO approach help structure a solution?
- Give one example of a Single Responsibility Principle (SRP) violation.

[Hints](./solutions/hints.md)
