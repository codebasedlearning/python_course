# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Python basics meant as a starter.

Teaching focus
  - Printing.
  - Reading from the console, needed for examples and exercises.
  - Basic principles of Python.
  - Consider the code as an example of where we want to go.
  - You do not need to understand every detail right away.
  - Code is not optimal in an algorithmic sense.

Topics
  - docstrings
  - import
  - print, f-string, r-strings
  - input
  - decorator
  - function definition and call with or without a (named) parameter
  - type hints
  - conditional expression
  - for-loop
  - while-loop
  - try-except
  - range
  - tuple
  - casts
  - string operations, slicing, strip, partition
  - list, set, dictionary, and some typical operations
  - variable destructuring
  - preview list comprehension.

'main'-guard
  - If you want to write Python code that can be imported but also run as
    a standalone script, this 'if' is important. The code protected by the
    if-clause only runs when executed as a script, because '__name__' is only
    then set to the value "__main__", see e.g.
    https://docs.python.org/3/reference/toplevel_components.html#complete-python-programs
    https://docs.python.org/3/reference/import.html?highlight=__name__#__name__
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    Otherwise '__name__' is set to the name of the module.
  - This guard is more or less standard.
  - Doing more than calling the function, especially defining variables, can
    lead to shadow variables and warnings.
  - Put your main work in your 'main' function ('my_main') and call it
    (only this) or keep the logic simple (here). Avoid defining locals
    after the 'main'-guard, see comments below.

Docstrings
  - Many rules about formatting and naming can be found in
    https://peps.python.org/pep-0008 'PEP 8 - Style Guide for Python Code'
    https://peps.python.org/pep-0257 'PEP 257 - Docstring Conventions'
  - The module description at the beginning may be presented in a slightly
    different style to other block comments.
    This description would be displayed in a tooltip in an IDE where you
    import the script, i.e. on the 'import' command. You can try this for
    example with the description of 'platform'.
  - The function description follows the signature and is also shown in the
    tooltip when called, i.e. 'main()'.

Indentation level
  - Python uses indentation instead of curly braces or begin/end blocks
    to define blocks of code (after the ':'). This means that whitespace
    is not ignored as usual, but is clearly part of the structure.
  - All commands at an indentation level (and lower if necessary) belong
    to the code block, see 'if', for instance.
  - https://docs.python.org/3/reference/lexical_analysis.html

Printing
  - https://realpython.com/python-print/
  - https://docs.python.org/3/howto/unicode.html
  - https://realpython.com/python-print/#adding-colors-with-ansi-escape-sequences

Function
  - The function 'scale_if_positive' takes a single argument 'n'.
  - Type hints are optional, but recommended. Here it would be:
        def scale_if_positive(n: int) -> int:
    We skipped it here because we discuss type hints later.

Local variables
  - A local variable like 'result' is valid for the whole function, i.e.
    'scale_if_positive'. And surprisingly, 'case' is also well defined until
    the end of the function.
  - There are quite a few rules about the scope of a variable. We will look
    at this in an upcoming lecture.

Self-documenting expression
  - Introduced in Python 3.8. "{x=}" prints "x=<value>" and "{f(1,2)=}"
    prints "f(1,2)=<value>".
  - We also number the outputs, e.g. " 1|..." and so on, in order to
    associate the output with the calling line.

//
  - / true division, always returns a float
  - // floor division, returns the largest integer ≤ result
    (truncates toward negative infinity)
  - // only returns an int if both operands are int. If either operand is
    a float, the result is a float — even if the value is mathematically whole.

Tail-call optimization (TCO)
  - A function is tail-recursive if the recursive call is the last thing it
    does. So this is
        calc_sum_tail_recursively(n - 1, acc + n)
    but this is not (because the addition after)
        n + calc_sum_recursively(n - 1)
  - In languages that support tail-call optimization (TCO) the current stack
    frame is reused and the recursion becomes equivalent to a while loop.
  - Python, however, does not perform tail-call optimization. It is a design
    decision.

'main'
  - It should be noted that, unlike other languages, there is no explicit 'main'
    as the starting point of execution. Code is executed from top to bottom,
    and 'def my_main' this is just a definition (not the execution) of a function.

'Pythonic way'
  - Defining the main functionality of the program in its own functions, which
    are then called, is one example of best practice, as they say here, the
    so-called 'Pythonic way'. This means, among other things: Do something right
    from a Python point of view.

Best practices
  - Document your code (short and concise).
  - Define something like a 'main'-function or keep global logic small.
  - Use a 'main guard'.
  - Use 'string interpolation' instead of concatenation.
  - Get a feeling for the 'Pythonic way'.

Code Style (from Style Guide for Python Code, PEP 8)
  - Spaces (no tabs) are the preferred indentation method.
  - Function names should be lowercase, with words separated
    by underscores as necessary to improve readability.
  - Variable names follow the same convention as function names.
  - No standard file header, use VCS instead (see below).
  - Use type hints if needed (discussed again later).
  - Define something like 'main', avoid variable shadowing.

File Header
  - This discussion always comes up when it comes to a 'common standard header'
    format of a Python script. Quoted from Jonathan Hartley, stackoverflow,
    could not put it any better:
        I think all of this metadata after the imports is a bad idea.
        The parts of this metadata that apply to a single file (e.g. author,
        date) are already tracked by source control. Putting an erroneous & out
        of date copy of the same info in the file itself seems wrong to me.
        The parts that apply to the whole project (eg licence, versioning)
        seem better located at a project level, in a file of their own, rather
        than in every source code file.
    That's why you don't find this information in the snippets.
"""

# Imports function into global namespace.
from unittest.mock import patch

from utils import print_function_header

"""
Topic: Console IO
"""

@print_function_header                      # Preview: A decorator printing the function's name.
def using_print():
    """ Various printings. """              # Docstring for the function, hold the mouse on 'using_print'.

    print(" 1| simple 'print'")
    print(" 2| print without", end='')      # Print without line-feed.
    print(" new line")

    print(f" 3| expressions in f-strings: {2*7=}")              # Formatted string ('f').
    print(f" 4| {{ and }} in f-strings, e.g. for a set: {{ 1,{1+1} }}")

    print(" 5| escaped chars, e.g. \" \' \\ \\n")               # With special chars ('escaped').
    print(r" 6| as r-string (raw), i.e. as it is, e.g. '\n'")   # Raw string ('r').

@print_function_header
def using_input():
    """ Reads from the console. """

    name = input(" 1| Enter your name: ")   # Read a string into a (string) variable.
    print(f" 2| Hello '{name}'!")


"""
Topic: Python structure
"""

def scale_if_positive(n):                   # A typical function with one parameter.
    """ Scales n if positive, otherwise returns 0. """

    result = 0                              # Spaces/indent and definition of a local variable with implicit type.
    factor: int = 0                         # Definition with type hints. They are optional but recommended if helpful.
    if n > 0:                               # Code blocks after ':', indention level is crucial.
        factor = 3
        case = 1                            # What is the scope of 'case'?
    else:
        factor = 1                          # Why are 'result' and 'factor' displayed gray before?
        case = 2

    result = n * factor
    print(f" a| -> {n=}, {result=} | {case=}, {factor=}")       # 'x=' self-documenting expression.
    return \
        result                              # This is one logical line, the backslash continues it.

@print_function_header
def calling_a_function():
    """ Prints some results from calling a function. """

    n1 = scale_if_positive(23)              # Local var, initialized with the return value.
    n2 = scale_if_positive(-7)
    print(f" 1| {n1=}, {n2=}")

def calc_sum_iteratively(n):
    """ Calculates 1+..+n iteratively. """

    result = 0
    for i in range(1,n+1):                  # Same as: for i=1; i<n+1; ++i
        result += i

    return result                           # or: return sum(range(1, n + 1))

def calc_sum_recursively(n):
    """ Calculates 1+..+n recursively. """

    # Preview: Note the conditional expression, e.g. 'if'-'else' as expression.
    return 0 if n <= 0 else n + calc_sum_recursively(n - 1)

def calc_sum_tail_recursively(n, acc = 0):
    """ Tail-recursive sum calculation. """

    # Tail-recursive because the recursive call is the last thing it does.
    return acc if n <= 0 else calc_sum_tail_recursively(n - 1, acc + n)

def calc_sum_directly(n):
    """ Calculates 1+..+n directly. """

    return n * (n + 1) // 2                 # '//' Integer division.

@print_function_header
def calculate_all_sums():
    """ Calculates all sums differently. """

    n = 5
    print(" 1| Sum 1..n:")

    sum_iteratively = calc_sum_iteratively(n = n)       # Call with a named parameter.
    sum_recursively = calc_sum_recursively(n = n)       # Pros/cons of named parameters?
    sum_tail = calc_sum_tail_recursively(n = n)
    sum_directly = calc_sum_directly(n = n)
    print(f" 2| 1+..+{n} =\n"
          f"  |    {sum_iteratively} (iteratively)\n"
          f"  |    {sum_recursively} (recursively)\n"
          f"  |    {sum_tail} (tail recursively)\n"
          f"  |    {sum_directly} (directly)")


"""
Topic: Collections
"""

@print_function_header
def collect_items():
    """ Collects items. """

    # A local function with exception handling.
    # Preview: Types as parameter.
    def try_parse(value, target_type):
        """ Converts value into target_type or None. """
        try:
            return target_type(value)
        except (ValueError, TypeError):
            return None

    print(" 1| Sort items: numbers in a set, positives in a list and assignments in a dictionary.")

    # Assume these inputs are from console input, file read or database query.
    inputs = ["1", "2", "3", "2", "-5", "a=Alice", "b=Bob", "eof"]

    numbers = set()                         # A set of unique numbers.
    positives: list[int] = []               # A list of positive numbers.
    variables: dict[str, str] = {}          # A dictionary of assignments.

    # preview: Walrus operator (:=) and inputs.pop(0) removes and returns at index.
    while (data := inputs.pop(0)) != "eof": # while-loop
        if (n:=try_parse(data, int)) is not None:
            print(f" 2| number: {n=}")
            numbers.add(n)
            if n > 0:
                positives.append(n)
        elif '=' in data:
            name, _, value = data.partition("=")  # Preview: Variable destructuring.
            print(f" 3| key-value: {name=}, {value=}")
            variables[name] = value
    print(f" 4| sorted: {numbers=}, {positives=}, {variables=}")

    for k,v in variables.items():           # Preview: Dictionary iteration.
        print(f" 5| {k}={v}")


if __name__ == "__main__":                  # 'main'-guard.
    # Console IO
    using_print()

    # Preview: context manager for (simple) input simulation (Monkey Patching, tests and teaching)
    # with patch("builtins.input", side_effect=["Bob"]):
    using_input()

    # Python structure
    calling_a_function()
    calculate_all_sums()

    collect_items()
