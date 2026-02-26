[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x03` – First Classes – Finalize Basics

## Overview

This unit completes the fundamentals by introducing classes, attributes, properties, methods,
operators, and single inheritance through several modeling tasks.

### Focus

Focus on solid OOP basics so you can design small class hierarchies and reason about object
behavior.

## Topics

- Classes and attributes
- Properties and encapsulation
- Instance, class, and static methods
- Operators and dunder methods
- Single inheritance
- Dataclasses (intro)

> This unit completes our basic knowledge. The aim is to model and solve simple algorithmic problems
in unit 0x04.
> - Unit 0x01: First Impression (examples)
> - Unit 0x02: First Steps (variables, control-flow, functions)
> - Unit 0x03: Finalize Basics (classes, inheritance)
> - Unit 0x04: Types, Inheritance, and Composition 


## Tasks

---

### 👉 Task 'Whale Coastline' (Pets)

An Age and Seniority Tracker – Warm Up.

Part 1
- Create a class `Pet` that represents a pet with a `name` and `age`. Your class should be able to:
	- Store the pet’s name and age.
    - Determine whether the pet is a senior (age 7 or older) using a `@property` called `is_senior`.
      
    - Provide a method `celebrate_birthday` which increases the pet’s age by 1.
- This `Pet("Fluffy", 6)` should create an instance and initialize the attributes.
- Change it to a `dataclass`.

Part 2
- Test your class.
- Send your code to 
  - pylint, mypy - any complaints?
  - an AI agent (e.g. ChatGPT) - any suggestions?

---

### 👉 Task 'Blue Strand' (Random Rolls)

Part 1
- Implement a class `Dice` that simulates rolling a customizable die. It should also support
  tracking how many rolls have been made in total across all instances.
- `__init__(self, sides)` sets the number of sides (default is 6). 
- Method roll() simulates a random roll and returns the result.
- Track the total number of rolls in a class variable `total_rolls`. 
- Store the roll history in a private instance attribute. 
- Expose the history through a read-only property `history`. 
- Add a static method `roll_multiple(n, sides)` that rolls n dice of a given size and returns the
  list of results. 
- Protect the internal roll history from modification.

Part 2
- Test your class.
- Send your code to 
  - pylint, mypy - any complaints?
  - an AI agent (e.g. ChatGPT) - any suggestions?

---

### 👉 Task 'Weymis Bay' (Spellbooks)

Part 1
- Create two classes: `Spell` and `Spellbook`. Spells have a `name`, `mana cost`, and `element`
  (e.g. fire, ice). 
- A Spellbook stores a collection of known spells and allows the user to:
	- `learn` and `forget` spells by name. 
    - `cast` a spell by name (returning a message). 
    - Use `in` to check if a spell is known. 
    - Use index access (`book["fireball"]`) to retrieve a spell. 
    - Iterate through all known spells in the spellbook.
- Change both classes to `dataclass`.

Part 2
- Test your class.
- Does it make sense to use a data class? For both? Any pros and cons?
- Send your code to 
  - pylint, mypy - any complaints?
  - an AI agent (e.g. ChatGPT) - any suggestions?

Hint: Use `__contains__`, `__getitem__`, and `__iter__` for intuitive access.

---

### 👉 Task 'Tall Leaf' (Figures)

Part 1:
- Implement a base class called `Figure`.
  - The constructor is given a description, which you store in a protected 
    member variable.
  - Create an appropriate read and write property `description`.
  - Implement a 'virtual' method `area` that returns the area of the figure.
  - Finally, give the class a nice `__str__` or `__repr__ `method for 
    appropriate output.
- Derive a class `Rectangle` from `Figure`.
  - In addition to the `description`, the constructor gets `width` and `length`, 
  - for which you also directly create two read properties.
  - Customise the output and use the functionality from the base class.

Part 2:
- Add a _private_ attribute `area_cache` to instances of the class `Figure`, which 
  is set to `None` at the beginning.
- When the function `area` is called, the first thing it does is to check whether 
  the 'cache' is still uninitialised (`None`). If it is, a virtual _protected_ 
  function `calc_area` is called in which each derived class performs the calculation
  of its area. The result is then stored in `area_cache` and returned. 
  Thus, each area is calculated only once.

Part 3
- Test your class.
- Send your code to 
  - pylint, mypy - any complaints?
  - an AI agent (e.g. ChatGPT) - any suggestions?

---

### 👉 Task 'Drift Pebble' (Vectors)

Topics: `__eq__`, `__hash__`, `__lt__`, `total_ordering`, `__add__`

Part 1
- Create a class `Vec2` representing a 2D vector with read-only properties `x`, `y`, and a computed
  property `length` (Euclidean norm).
- Implement `__eq__` so that two vectors with the same components are equal.
- Implement `__hash__` so that equal vectors produce the same hash. This allows `Vec2` instances to
  be used in sets and as dictionary keys.
- Test: create `a = Vec2(1, 0)` and `c = Vec2(1, 0)`. Verify `a == c` is `True`, `a is c` is
  `False`, and `{a, c}` has length 1.

Part 2
- Implement `__lt__` to compare vectors by their length.
- Use `@functools.total_ordering` to get `<=`, `>`, `>=` for free.
- Test: sort a list of vectors and verify the order.

Part 3
- Implement `__add__` to return a new `Vec2` with component-wise addition.
- Test: `Vec2(1, 0) + Vec2(0, 1)` should give `Vec2(1, 1)`.

Part 4
- Use your vectors as dictionary keys (counting occurrences) and in a set (deduplication).

Check
- Compare your solution with `drift_pebble_one_solution.py` in `solutions`.
  - Is your solution correct and complete?
  - Do you have any ideas on how to improve your solution?
  - Is there a detail where your solution is better or different? Tell us.

---

### 🤔 Task 'Canoe Hair' (Window)

> This is a relatively simple inheritance task. The principle is basically no
different in Python than in other OO-languages.

- Define a class `Window`. It serves as a superclass and has a (virtual) method `draw`.
- Derive a class `Button` and a class `Checkbox` from `Window`, both define `draw`.
- Create a list with one instance each of `Button` and `Checkbox`.
- Call `draw` on all elements of the list and test whether the correct function is called.


### 👉 Task 'Self-Study'

- Review all snippets from the lecture. Ask if there are any outstanding questions.
- Run and understand all content from scripts that start with `self_`. Ask if you miss an idea.

---

### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do
  or have questions about?

---

### 👉 Task 'AI Snapshot' – Class vs Instance

Prompt
- "After this code, what are `Counter.count`, `c1.count`, and `c2.count`?"

```python
class Counter:
    count = 0

c1 = Counter()
c2 = Counter()

c1.count += 1
```

AI Answer A
`Counter.count == 0, c1.count == 1, c2.count == 0`

AI Answer B
`Counter.count == 1, c1.count == 1, c2.count == 1`

Discuss
- Which answer is correct and why?
- Explain how instance attributes shadow class attributes.

---

### 👉 Task 'AI Snapshot' – Property Validation

Prompt
- "Implement a `Temperature` class that rejects values below `-273.15` using a property."

AI Answer A
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value
```

AI Answer B
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
```

Discuss
- Which answer enforces the constraint?
- What happens if `Temperature(-300)` is created in Answer B?

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

## Comprehension Check

General
- Any suggestions for working with an AI agent?

Language
- What are `types` for in Python and do you use them?
- What are `args` and `kwargs`?
- Do you know the difference between a 'regular' member function, a static method and a class
  method?
- What kind of 'dunder' functions do you know and what are they for?
- What is the idea of a data class?
- What is the difference between `__str__` and `__repr__`?
- What is the difference between a class attribute and an instance attribute?
- What is a property and why would you use it?

---
