[© 2025, A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x01` – First Impression

> To get you started quickly, we will touch on many topics and leave the details for later units. Think of the examples in `snippets` as templates for various Python features.


## Topics touched

- General structure of a Python program, e.g.
  - comments
  - imports and modules 
  - doc-strings
  - role of whitespaces
- Examples with Python basics, e.g.
  - primitives (int, float, string, bool)
  - built-in containers (list, tuple, dict)
  - type hints
  - control flow (if, while, for, try-except)
  - function calls with named parameters
  - console input and output
  - variable destruction
- Pythonic way, e.g.
  - `__name__`, `__main__`


## General Sources

- https://docs.python.org/3.13/
- https://docs.python.org/3.13/reference/index.html
- https://docs.python.org/3.13/library/index.html
- https://www.w3schools.com/python


## Tasks

Start with 'Cocoa Coast', then 'Harmony Bay' and then as you like. Finish with 'Comprehension' and 'Lecture' Checks.

---

### ☝️ Task 'Cocoa Coast' – Python Installation

All commands needed for this task can be found in [Setup](../docs/python_setup.pdf).

- Install at least two Python versions using `pyenv`, e.g. the latest stable release (>=3.13.2) and a development version (>=3.14.0a5). Check, also with `pyenv`, that multiple versions are actually installed.

- Start the scripts `hello_world.py` and `about_setup.py` (in `0x00/snippets` with `python3` or `python`) from the command line. Which Python version was used?

- Change the current Python version and repeat the step before, also from the command line.

- Create a virtual environment `venv` in `0x00` using the `venv`-module and install the `cbl` library in the latest version (0.4.2). Does `about_setup.py` show that the local environment is used? Remember to 'activate' the virtual environment.

- Uninstall `cbl` and install an older version (0.2.3) instead. Now upgrade `cbl`. All, of course, from the command line. 

- Think about how you want to work, e.g. with `Visual Studio Code` or with`PyCharm` or your favourite IDE. Open the folder `python_course` and configure your IDE with regard to the Python version and virtual environment used. Try different Python configurations, maybe a Docker variant; see [IDE](../docs/python_ide.pdf). Check with `about_setup.py` that the intended Python version is actually used.

---

### ☝️ Task 'Harmony Bay' – Your Solution Project

- Create a new project or folder for your exercise solutions. You can do this from within your IDE or from the command line.
- Configure a Python version and virtual environment that you want to work with. If you do not want to use the latest stable version of Python, use a version that is not too old.
- Decide how you want to organise your solutions, perhaps with a folder per unit.
- Copy the `turtle_coast.py` template from `c_templates` as an example into your new structure and try to run it.
- Create a new template or modify this one for your own solutions, e.g. by adding your name as a copyright notice (top line).
---

### 👉 Task 'Eastern Sands'

Topics: functions, loops, exceptions, input, conversions

Part 1
- Create (or copy) a `eastern_sands.py` file in your solutions project.
- Read a text from the console,
- and convert it to an integer `n`.
- Output `n`, e.g. "Your number was <n>". Use 'string interpolation'.
- Be aware of the 'Pythonic way' regarding `__main__`.
- Provide descriptions for the script and the implemented functions.

Part 2
- Catch possible exceptions from the conversion (`ValueError`) and print the error. 
- Repeat the whole input and output process until you have an empty text.

Check
- Compare your solution with `eastern_sands_one_solution.py` in `solutions`. 
  - Is your solution correct and complete? 
  - Do you have any ideas on how to improve your solution?
  - Is there a detail where your solution is better or different? Tell us.

---

### 👉 Task 'Sunny Coastline'

Topics: functions, loops, input, dictionaries, recursion

- Create (or copy) a `sunny_coastline.py` file in your solutions project.
- Read a number `n` from the console and compute the nth Fibonacci number, see [Fibonacci](https://de.wikipedia.org/wiki/Fibonacci-Folge),
  - iteratively,
  - recursively,
  - recursively with Memoization, i.e. a dictionary containing all the values calculated so far, so that you can use these values if the number has already been calculated.

Check
- Compare your solution with `sunny_coastline_one_solution.py` in `solutions`. 
  - Is your solution correct and complete? 
  - Do you have any ideas on how to improve your solution?
  - Is there a detail where your solution is better or different? Tell us.

---

### 👉 Task 'Bronze Strand'

Topics: functions, dictionaries, loops

- Create (or copy) a `bronze_strand.py` file in your solutions project.
- Create three functions that operate on a dictionary, called 'counter'. Its keys are elements such as characters and the corresponding values are the counts. Example: After adding all characters from `banana` the dictionary looks like `{'b': 1, 'a': 3, 'n': 2}`.
  - Implement a function `counter_add(counter: dict, item)` that increases the count of `item` in the dictionary. If the `item` is not in the dictionary, it should be added with a count of 1. 
  - Implement a function `counter_sub(counter: dict, item)` that decreases the count of `item` in the dictionary. If the `item`’s count becomes zero or negative, remove it from the dictionary (with `del counter[item]`). 
  - Implement a function `counter_most_common(counter: dict)` that returns the element with the highest count. If the counter is empty, return `None`.
  - Test your functions with the characters from `banana`.
Note: There is a collection `Counter` working exactly like your functions.

Check
- Compare your solution with `bronze_strand_one_solution.py` in `solutions`. 
  - Is your solution correct and complete? 
  - Do you have any ideas on how to improve your solution?
  - Is there a detail where your solution is better or different? Tell us.

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

### 👉 Comprehension Check - Talk with your Neighbor

General
- What are your options for running a Python program?
- What are the programmes or modules `python3`, `pip3`, `pyenv` and `venv` good for?
- What is behind the term 'PEP'?
- Who actually invented Python?
- What is the meaning of indentation in code?
- What is the 'Pythonic way'?

Language
- What are the options for comments in source code?
- What 'primitive' data types do you know?
- Which 'container' data types do you know?
- What do you understand by 'variable unpacking'?
- What do you understand by 'string interpolation'?
- What does 'named parameter' mean?
- What does the variable `__name__` mean?

---

### 👉 Lecture Check - Online Questionare

- Please participate in the survey: -link-

---

End of `Unit 0x01`
