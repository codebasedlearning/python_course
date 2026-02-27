[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x01` – Introduction


## Overview

This introductory unit focuses on setting up your Python development environment and getting 
familiar with Python basics through hands-on tasks. 

You'll install and configure Python using `uv`, create your first project, and explore
fundamental Python concepts including data types, control flow, functions, and the 
"Pythonic way" of programming. 

The unit includes setup tasks and coding exercises that progressively build your understanding 
of core Python features. By the end, you'll have a working Python environment, understand how 
to manage dependencies, and have practical experience with essential Python programming patterns.


### Focus

> To get you started quickly, we will touch on many topics and leave the details for later units.
> Think of the examples in `snippets` as templates for various Python features.


## Topics

- Program structure (comments, imports, docstrings, indentation)
- Python basics (int, float, string, bool)
- Core collections (list, tuple, dict, set)
- Control flow and loops (if, while, for, try/except)
- Functions and parameters
- Console I/O (input, print)
- Unpacking and string formatting
- Pythonic style and conventions


## Tasks

Start with the following tasks from the [Info](../docs/python_info.pdf).


### ☝️ Task 'Windy Bank' – `git` setup
- [Learn git](https://www.w3schools.com/git) <BR>
- [Install git](https://git-scm.com)


### ☝️ Task 'Cocoa Coast' – Clone `python_course`
- [GitHub Repo](https://github.com/codebasedlearning/python_course)


### ☝️ Task 'Harmony Bay' – Python Setup
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/) <BR>
- [uv Commands](https://docs.astral.sh/uv/guides/) <BR>
- [uv Projects](https://docs.astral.sh/uv/guides/projects/)


### ☝️ Task 'Silent Strand' – Create Project


### ☝️ Task 'Alsano Shore' – Manage CBL Library


### 👉 Task 'Self-Study'

- Review all snippets from the lecture.
- Run and understand all content from scripts that start with `study_` (if any). 
- Ask if there are any outstanding questions, or if you miss an idea.


### ☝️ Task 'Hope Edge' – Your Solution Project

- Think about how you want to work, e.g. with an editor such as `Visual Studio Code` 
  or `Zed` or with an IDE like `PyCharm` or your favourite IDE. 
- Open the repository folder `python_course` and configure your IDE with regard to 
  the Python version and virtual environment used. 
- Try different Python configurations and check with `print_python_setup.py` that 
  the intended Python version is actually used.
- Decide how you want to organize your solutions, perhaps with an own task-project.
- Use, if you like, the `turtle_coast_a_task_template.py` from Unit `0x01` as a base
  for your solutions. Add your name as a copyright notice (top line).


### 👉 Task 'Eastern Sands'

Part 1
- Create (or copy) a `eastern_sands.py` file in your solutions project.
- Read a text from the console,
- and convert it to an integer `n`.
- Output `n`, e.g. "Your number was <n>". Use 'string interpolation.'
- Be aware of the 'Pythonic way' regarding `__main__`.
- Provide descriptions for the script and the implemented functions.

Part 2
- Catch possible exceptions from the conversion (`ValueError`) and print the error. 
- Repeat the whole input and output process until you have an empty text.

Check
- Compare your solution with an external one and ask yourself:
  - Is your solution correct and complete? 
  - Do you have any ideas on how to improve your solution?
  - Is there a detail where your solution is better or different? 
- Compare it with 
  - the provided one from `solutions` (`eastern_sands_one_solution.py`) and
  - an AI-generated solution, e.g. from 'Claude Code' or 'OpenAI Codex' 
    (or any other AI-based code generator).


### 👉 Task 'Sunny Coastline'

- Create a `sunny_coastline.py` file in your solutions project.
- Read a number `n` from the console and compute the nth Fibonacci number, see
  [Fibonacci](https://de.wikipedia.org/wiki/Fibonacci-Folge),
  - iteratively,
  - recursively,
  - recursively with Memoization, i.e. a dictionary containing all the values calculated so far, so
    that you can use these values if the number has already been calculated.

Check
- Compare your solution with the provided one from `solutions` and an AI-generated one.


### 👉 Task 'Bronze Strand'

- Create a `bronze_strand.py` file in your solutions project.
- Create three functions that operate on a dictionary, called 'counter.' Its keys are elements such
  as characters and the corresponding values are the counts. Example: After adding all characters
  from `banana` the dictionary looks like `{'b': 1, 'a': 3, 'n': 2}`.
  - Implement a function `counter_add(counter: dict, item)` that increases the count of `item` in
    the dictionary. If the `item` is not in the dictionary, it should be added with a count of 1. 
  - Implement a function `counter_sub(counter: dict, item)` that decreases the count of `item` in
    the dictionary. If the `item`’s count becomes zero or negative, remove it from the dictionary
    (with `del counter[item]`). 
  - Implement a function `counter_most_common(counter: dict)` that returns the element with the
    highest count. If the counter is empty, return `None`.
  - Test your functions with the characters from `banana`.
Note: There is a collection `Counter` working exactly like your functions.

Check
- Compare your solution with the provided one from `solutions` and an AI-generated one.


### 👉 Project 'Moving Blizzard' — Part 1

> A coastal research station monitors environmental sensors. This semester-long project starts
> with a simple temperature list and grows week by week — refactoring the same codebase with
> every new concept you learn.

Part 1
- Create a list `READINGS` with at least 10 temperature values (floats), e.g.
  `[18.2, 19.1, 17.8, 22.5, 18.9, 31.4, 19.0, 18.5, 20.1, 17.6]`.
- Write a function `average(data)` that computes the mean using a loop (no `sum` yet).
- Write `minimum(data)` and `maximum(data)` — again, no built-in `min`/`max`.

Part 2
- Write `detect_spikes(data, threshold=5.0)` that returns the indices where the reading
  jumps by more than `threshold` from the previous value.
- Write `summarize(data)` that prints count, average, min, max, and spike positions.
- Call `summarize(READINGS)` from a proper `main()` with `__main__` guard.

Check
- Compare your solution with the provided one from `solutions` and an AI-generated one.
- Does your `detect_spikes` handle an empty list?


### 👉 AI 'Off-By-One Imp'

Prompt 
```
Explain what `if __name__ == '__main__':` does and show a tiny example.
```

AI Answer A
```python
def main():
    print("run")

if __name__ == "__main__":  # runs only when executed directly
    main()
```

AI Answer B
```
It prevents all code in the file from running unless the file is imported.
```

Discuss
- Which answer is correct and why?
- What actually happens to top-level code when the file is imported?

[Hints](./solutions/hints.md)


### 👉 AI 'Off-By-One Imp'

Use the input loop idea from Task 'Eastern Sands' above.

Prompt 
```
Read integers until an empty line is entered. Print each number. Ignore invalid input.
```

AI Answer A
```python
while (line := input("n: ")) != "":
    try:
        n = int(line)
        print(n)
    except ValueError:
        print("invalid")
```

AI Answer B
```python
while (line := input("n: ")) != "":
    n = int(line)
    print(n)
```

Discuss
- Which answer is robust for invalid input?
- What is missing in the other answer?

[Hints](./solutions/hints.md)


### 👉 Homework 'Couch Potato'

- It is absolutely necessary to have a working Python environment before the next unit.
  If you have any issues with your Python configuration, try to solve them at home or
  reach out to the course staff.
- If you did not finish the essential tasks in the exercise, complete them at home.


## Comprehension Check

General
- What ways can you run a Python program (script, module, REPL, IDE, notebook)?
- What is `uv` used for in Python projects?
- What does the term “PEP” stand for, and why does it matter?
- Who created Python?
- What does indentation mean in Python code, and why is it important?
- What does “Pythonic” mean (the “Pythonic way”)?
- What’s the difference between `import x` and `from x import y`?

Language
- What comment styles can you use in Python?
- Which primitive/built-in scalar types do you know?
- Which container/collection types do you know?
- What is “unpacking” (e.g., tuple/list unpacking, `*args`, `**kwargs`)?
- What is string interpolation in Python (e.g., f-strings, `format`)?
- What is a named parameter / keyword argument?
- What does the `__name__` variable mean?
- How do you handle exceptions in Python (`try` / `except` / `else` / `finally`, raising)?
- What is the purpose of `if __name__ == "__main__":` compared to code that runs on import?
- How do you document modules and functions in Python (docstrings)?
- What is a virtual environment and why do we use it?
- What is `pyproject.toml` used for in a Python project?

[Hints](./solutions/hints.md)

