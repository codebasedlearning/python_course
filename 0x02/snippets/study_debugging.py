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


# ---------------------------------------------------------------------------
# Example 1: Inspect a simple calculation
# ---------------------------------------------------------------------------

def buggy_average(numbers):
    """Computes the average — but has a subtle bug. Can you spot it?"""
    total = 0
    count = 0
    for n in numbers:
        total += n
    # Oops: count is never incremented inside the loop!

    # Uncomment the next line, run the script, and inspect `total` and `count`:
    # breakpoint()

    return total / count if count != 0 else 0


# ---------------------------------------------------------------------------
# Example 2: Step through a loop
# ---------------------------------------------------------------------------

def find_first_duplicate(items):
    """Returns the first item that appears more than once."""
    seen = set()
    for item in items:
        # Uncomment to pause on every iteration and inspect `seen` and `item`:
        # breakpoint()
        if item in seen:
            return item
        seen.add(item)
    return None


# ---------------------------------------------------------------------------
# Example 3: Post-mortem debugging
# ---------------------------------------------------------------------------

def demonstrate_post_mortem():
    """Shows how to debug *after* an exception has already been raised."""
    data = [10, 20, 0, 30]

    try:
        results = [100 / x for x in data]
    except ZeroDivisionError:
        print(" 3| Exception caught! Would enter post-mortem debugger...")
        print("    (type 'p data', 'p x', 'w', then 'q' to quit)\n")
        # Uncomment to drop into the debugger at the point of failure:
        # import pdb; pdb.post_mortem()
        print("    (post-mortem is commented out — uncomment to try it)")


# ---------------------------------------------------------------------------
# Example 4: Conditional breakpoint
# ---------------------------------------------------------------------------

def process_items(items):
    """Processes a list. We only want to break on the suspicious item."""
    for i, item in enumerate(items):
        # Only break when the item is negative — skip the boring ones:
        # if item < 0:
        #     breakpoint()
        result = item * 2
        print(f" 4| item[{i}] = {item:4d}  ->  result = {result}")


if __name__ == "__main__":
    print("=" * 60)
    print("Example 1: buggy_average")
    print("=" * 60)
    nums = [10, 20, 30]
    avg = buggy_average(nums)
    print(f" 1| average of {nums} = {avg}")
    print(f"    (expected 20.0 — is it correct?)\n")

    print("=" * 60)
    print("Example 2: find_first_duplicate")
    print("=" * 60)
    data = ["a", "b", "c", "b", "d"]
    dup = find_first_duplicate(data)
    print(f" 2| first duplicate in {data} = {dup!r}\n")

    print("=" * 60)
    print("Example 3: post-mortem debugging")
    print("=" * 60)
    demonstrate_post_mortem()
    print()

    print("=" * 60)
    print("Example 4: conditional breakpoint")
    print("=" * 60)
    process_items([5, 12, -3, 8, -1, 42])

    print()
    print("To try the debugger: uncomment the breakpoint() lines and run again!")
