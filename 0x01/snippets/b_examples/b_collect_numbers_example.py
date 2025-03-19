# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features.

Teaching focus
  - Consider the code as an example of where we want to go.
  - You do not need to understand every detail right away.
  - Code it is not optimal in an algorithmic sense.
"""


def collect_numbers():
    """ collect numbers from the console """

    numbers = set()                                             # a set
    inputs: list[int] = []                                      # a list with type hint (better would be a deque)

    print(" 1| Collect numbers in a set and inputs in a 'finite' FIFO list")
    while (data := input(" 2| Enter number n: ")) != "":
        try:
            n = int(data)
            if n in numbers:
                print(f" 3| {n} already exists")
            # else:
            numbers.add(n)                                      # a set contains an element only once
            if len(inputs) >= 5:                                # if cond1 and/or cond2; 'and' higher than `or`
                # actions.pop(0)                                # removes and returns the value
                del inputs[0]                                   # discards the value
            inputs.append(n)
            print(f" 5| {numbers=}, {inputs=}")
        except ValueError as e:
            print(f" 6| error: {e}")


if __name__ == "__main__":
    collect_numbers()


###############################################################################


"""
Summary

Topics
  - walrus operator (:=)
  - try-except
  - if, and, or
  - set operations
  - list operations

See also
  - https://docs.python.org/3.13/
  - https://docs.python.org/3.13/reference/index.html
  - https://docs.python.org/3.13/library/index.html
"""
