[© 2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x06` – Types, Inheritance, and Composition


## Types

> Python typing is primarily a static, opt-in system layered over a dynamic runtime.
- Static: Type hints are used by static analysis tools (like mypy, pyright, IDEs) to catch type errors before running the code—without affecting how the code runs.
- Opt-in: Type annotations are completely optional. You can write a fully functional Python program without using any types at all.
- Layered over: The type system is not enforced by the Python interpreter. It’s an additional layer for developers, linters, and tools — not the runtime engine.
- Dynamic runtime: Python still behaves as a dynamically typed language at runtime. Variables and objects can be reassigned to different types, and type errors only occur when you try something invalid — not when you declare it.

**Please have a look at the snippet 'a_intro/a_typing'.**


> At runtime, Python uses duck typing — objects are valid if they respond to the right methods, regardless of declared types.
At 'compile time' (static analysis time with tools like mypy or Pyright), Python supports nominal and structural typing via type hints, abstract base classes, and protocols.
These annotations don’t change program behavior but let type checkers catch bugs early and guide tooling—they describe what should work, not what will work.

### Overview

| Concept | Definition                                                       | Python Mechanism | Checked At | Use Case |
|---------|------------------------------------------------------------------|------------------|------------|----------|
| Nominal Typing | Types are identified by name (class declarations)                | Class inheritance | Static (mypy) | Ensure only explicitly related types are used
Subtyping | A class inherits from another (OOP-style hierarchy) | class Dog(Animal)                                                 |  Static & runtime | Classic inheritance behavior, isinstance and issubclass
| Duck Typing | 'If it quacks like a duck' - no type hints, just trust           | Regular Python (no hints) | Runtime | Idiomatic Python, dynamic typing without static safety |
| Structural Typing | Types are compatible if they look right (method signatures match) | typing.Protocol | Static (mypy) | Flexible duck typing with static checking
| Protocols | Structural interfaces: define what methods/attrs a type must have | Protocol (optionally @runtime_checkable) | Static + runtime | Use with mypy and optionally isinstance

### Summary in One-Liner Definitions
- Nominal Typing: "Are you explicitly declared to be this thing?"
- Subtyping: "Are you a child of this thing?"
- Duck Typing: "Can I just try calling your methods and hope?"
- Structural Typing: "Do you look like this thing?"
- Protocols: "You look like the thing — and I checked that at compile time."


## Inheritance

> Inheritance lets a class reuse behavior and structure from another class. A subclass inherits methods and attributes from its parent, optionally overriding or extending them.
> Python supports multiple inheritance, meaning a class can inherit from more than one parent.
> Python resolves conflicts via the method resolution order (MRO), which uses the C3 linearization algorithm.

### Relationship between Inheritance and Typing

Inheritance is tied closely to nominal typing and subtyping:
- A subclass is always a valid instance of its superclass.
- Abstract base classes (ABC) enforce method implementations in subclasses, supporting nominal typing contracts.
- Multiple inheritance with Protocols (i.e., structural typing) is also valid and lets you define capabilities without needing inheritance trees.


## Composition

Inheritance, and especially multiple inheritance, is controversial and can 
quickly lead to a class explosion. If the primary goal is to provide classes
with special functionality, interfaces or policies in the form of protocols or
specialized abstract classes or mixins are a way of keeping the class
hierarchy, and thus the complexity, small and manageable. The same can be
achieved with composition, which also opens up the possibility of fine-tuning
the interface of the individual class. A nice discussion can be found 
[here](https://realpython.com/inheritance-composition-python). 
The 'self*'-snippets are associated code to try out.


## Topics covered

- Typing (nominal typing, subtyping, duck typing, structural typing)
- single and multiple inheritance, method resolution order MRO
- inheritance vs. composition


## Tasks

---

### 👉 Task 'Shrimp Edge' (Protocol)

> You are writing a logging system. You don’t care what kind of object is being
logged — as long as it can produce a log message.

Part 1 (Duck Typing, no Protocols)

Write a function `log(obj)` that works with any object that has a method called
`log_message`. In detail:
- Define two classes (`User` and `Server`) that both have a `log_message` method.
- Implement a `log(obj)` function that calls `obj.log_message()` and prints the result.
- Call it with a `User` and `Server` instance.
- Try passing something without a `log_message` method — see what happens.

Part 2 (with Protocol)

Convert your code to use a `Protocol` for static type safety:
- Define a `Loggable` Protocol with a method `log_message() -> str`.
- Annotate the `log` function to require a `Loggable`.
- Test as in part 1.
- Use `mypy` (or any checker) to confirm type conformance.

Part 3 / Bonus (Optional)

Try making `Loggable` `@runtime_checkable` and use `isinstance` to enforce the interface dynamically.
See https://docs.python.org/3/library/typing.html#typing.runtime_checkable

Key Points from the Docs
- `@runtime_checkable` can only be applied to Protocols.
- It enables the use of `isinstance(obj, Protocol)` and `issubclass(cls, Protocol)`.
- The Protocol must not contain non-method members (e.g., attributes without default values) to be runtime-checkable.

| Version | Type Safe? | Runtime Safe? | Notes |
|---------|------------|------------|-|
| Duck Typing | no | no | Fast and loose |
| Protocol | yes | no | Best for static checking |
| Protocol + @runtime_checkable | yes | yes | Safest for real-world use |

---

### 👉 Task 'Cornwin Bay' (Mixin)

> You’re designing a system where various objects should be printable in a custom
format. You want to use a mixin to provide a reusable .print() method and use
multiple inheritance to apply it across different base classes.

- Create two base classes `User` and `Server` as in task 'Shrimp Edge.' Both
implement `__str__`.
- Define a mixin class `PrintableMixin` that adds a method `print` which prints
`[PRINT] ` and then the result of `__str__`.
- Define two subclasses of `User` and `Server` and mix-in `PrintableMixin` 
using multiple inheritance to add printing behavior.
- Test your mixin with appropriate instances of the subclasses.

---

### 👉⭐ Task 'Butterfly Hops' (inheritance, composition, and class design)

> The general goal is to model an amphibious vehicle consisting of a car and 
a boat. It is to be solved once by composition (part 1, completely without
inheritance) and once by inheritance (part 2, as far as possible). It should
also be possible to create and parameterize individual cars and boats.

Requirements for the classes:
- A car (class `Car`) has wheels and an engine (class `Engine`) that can reach 
a certain maximum speed.
- Similarly, a boat (class `Boat`) has an engine and is either a hovercraft 
or not. 
- Both a car and a boat have a cabin (class `Cabin`) with a number of seats. 
- An amphibious vehicle (class `amphibian`) has two (!) engines altogether 
(car and boat), but only one (!) cabin.

A quick look at the tests illustrates the structure. Note that these three
tests look the same for both parts!

#### Tests

Since we have not yet discussed unittests, we will use a simple `assertEqual`
method here:

```
def assertEqual(first, second):
    if first != second:
        raise AssertionError(f"{first} != {second}")
```

Here are the tests you can run from 'main'-guard. The `car` and `boat` tests
simply check the properties, while the `amphibian` test also checks that the
engines are different but the cabin is the same.

```
def test_car():
    print(f"\n 1| {Car.__mro__=}")
    car = Car(seats=3, max_speed_car=350, wheels=4)

    assertEqual(car.cabin.seats, 3)
    assertEqual(car.engine_car.max_speed, 350)
    assertEqual(car.wheels, 4)

def test_boat():
    print(f"\n 2| {Boat.__mro__=}")
    boat = Boat(seats=2, max_speed_boat=75, hovercraft=True)

    assertEqual(boat.cabin.seats, 2)
    assertEqual(boat.engine_boat.max_speed, 75)
    assertEqual(boat.hovercraft, True)

def test_amphibian():
    print(f"\n 3| {Amphibian.__mro__=}")
    amphibian = Amphibian(seats=4, max_speed_car=250, max_speed_boat=50, wheels=4, hovercraft=True)

    assertEqual(amphibian.cabin.seats, 4)
    assertEqual(amphibian.car.engine_car.max_speed, 250)
    assertEqual(amphibian.car.wheels, 4)
    assertEqual(amphibian.boat.engine_boat.max_speed, 50)
    assertEqual(amphibian.boat.hovercraft, True)

    assertEqual(id(amphibian.car.cabin)==id(amphibian.boat.cabin),True)
    assertEqual(id(amphibian.car.engine_car)==id(amphibian.boat.engine_boat),False)
```


#### Preparation
- Create a separate solution file for Part 1 and Part 2.

#### Constraints
- The tests can, of course, be commented in and out, but they will not be
changed in any other way.
- Of course, you are free to use properties as well.

#### Parts

Part I (Composition)

- Model the five classes (`Cabin`, `Engine`, `Car`, `Boat`, `Amphibian`) 
using only compositions, i.e., a car has a cabin and an engine, and 
an amphibian has a car and a boat, etc.
- Design the class, its attributes, properties, and methods according to the tests.

> The MROs for `Car`, `Boat` and `Amphibian` are as follows
> - 'Car', 'object'
> - 'Boat', 'object'
> - 'Amphibian', 'object'
 
Part II (Inheritance)

- Model the five classes using (multiple) inheritance, i.e., 
  - an amphibian is a car and a boat and, with a bit of imagination, 
  - a car 'is' a kind of extension of a cabin, and
  - a boat is also an extension of a cabin, but
  - the car and the boat share the cabin (diamond problem), but not the engine!
- Design the classes, attributes, properties, and methods according to the
tests, taking into account the MRO (hint: `kwargs`). 

> The MROs for `Car`, `Boat` and `Amphibian` are as follows
> - 'Car', 'Cabin', 'object'
> - 'Boat', 'Cabin', 'object'
> - 'Amphibian', 'Car', 'Boat', 'Cabin', 'object'

---

### 👉 Task 'Self-Study'

- Review all snippets from the lecture. Ask if there are any outstanding questions.

---

### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do or have questions about?

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

### 👉 Comprehension Check - Talk with your Neighbor

General
- Characterize 'single inheritance', 'multiple inheritance' and 'composition'.
- Characterize 'abstract classes', 'mixins' and 'protocols'.
- What is 'nominal typing', 'structural typing' and 'duck typing'?
- What is the famous phrase for 'duck typing'? And what does it mean?
- What is the problem with the 'MRO' and calling the `super` function?

---

### 👉 Lecture Check - Online Questionare

- Please participate in the survey: [Slido](https://wall.sli.do)

---

End of `Unit 0x06`
