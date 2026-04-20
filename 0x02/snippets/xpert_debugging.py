# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet introduces Python's built-in debugger via `breakpoint()`.

Teaching focus
  - breakpoint() drops you into an interactive debugger (pdb by default).
  - You can inspect variables, step through code, and evaluate expressions
    — all without adding print() statements.
  - Think of it as print-debugging with superpowers.

Quick pdb cheat sheet (type these at the (Pdb) prompt):
  n     — next line (step over)
  s     — step into function call
  c     — continue until next breakpoint
  p x   — print the value of x
  pp x  — pretty-print x
  l     — list source code around current line
  w     — show call stack (where am I?)
  q     — quit the debugger
  h     — help (list all commands)

More sources:
    https://docs.python.org/3/library/pdb.html
    https://docs.python.org/3/library/functions.html#breakpoint
    https://realpython.com/python-debugging-pdb/

Note: In your IDE (PyCharm, VS Code), you can also set graphical breakpoints
by clicking next to the line number. The built-in `breakpoint()` function works
everywhere — terminal, scripts, tests, remote servers.
"""

from utils import print_function_header

"""
Topic: Inspect a simple calculation
"""


@print_function_header
def buggy_average():
    """ breakpoint() to inspect a subtle bug """

    def average(numbers):
        total = 0
        count = 0
        for n in numbers:
            total += n
        # Oops: count is never incremented inside the loop!

        # Uncomment the next line, run the script, and inspect `total` and `count`:
        # breakpoint()

        return total / count if count != 0 else 0

    nums = [10, 20, 30]
    avg = average(nums)
    print(f" 1| average of {nums} = {avg}")
    print(" 2| expected 20.0 — is it correct?")
    print(" 3| uncomment breakpoint(), then type: p total, p count")


"""
Topic: Step through a loop
"""


@print_function_header
def step_through_loop():
    """ stepping through iterations with breakpoint() """

    def find_first_duplicate(items):
        seen = set()
        for item in items:
            # Uncomment to pause on every iteration and inspect `seen` and `item`:
            # breakpoint()
            if item in seen:
                return item
            seen.add(item)
        return None

    data = ["a", "b", "c", "b", "d"]
    dup = find_first_duplicate(data)
    print(f" 1| data:            {data}")
    print(f" 2| first duplicate: {dup!r}")
    print( " 3| use 'n' to step, 'p seen' to inspect the set as it grows")


"""
Topic: Post-mortem debugging
"""


@print_function_header
def post_mortem_debugging():
    """ debugging *after* an exception with pdb.post_mortem() """

    data = [10, 20, 0, 30]

    try:
        results = [100 / x for x in data]
        print(f" 1| {results=}")
    except ZeroDivisionError:
        print(f" 2| exception caught! data was {data}")
        print( " 3| to debug: uncomment 'import pdb; pdb.post_mortem()' below")
        print( " 4| then type 'p data', 'p x', 'w' (where am I?), 'q' (quit)")
        # Uncomment to drop into the debugger at the point of failure:
        # import pdb; pdb.post_mortem()


"""
Topic: Conditional breakpoint
"""


@print_function_header
def conditional_breakpoint():
    """ break only on suspicious items """

    items = [5, 12, -3, 8, -1, 42]

    for i, item in enumerate(items):
        # Only break when the item is negative — skip the boring ones:
        # if item < 0:
        #     breakpoint()
        result = item * 2
        label = " <-- negative!" if item < 0 else ""
        print(f" {i+1}| item[{i}] = {item:4d}  ->  result = {result}{label}")

    print()
    print(" 7| uncomment the conditional breakpoint to pause only on negatives")


if __name__ == "__main__":
    buggy_average()
    step_through_loop()
    post_mortem_debugging()
    conditional_breakpoint()
