# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features
(it is not optimal in an algorithmic sense).

Please consider the code as an example of where we want to go.
You do not need to understand every detail right away.
"""

def collect_numbers():
    """ collect numbers from the console """
    numbers = set()                                             # a set
    inputs = []                                                 # a list
    print(" 1| Collect numbers in a set and inputs in a 'finite' FIFO list")
    while (data := input(" 2| Enter number n: ")) != "":
        try:
            n = int(data)
            if n in numbers:
                print(f" 3| {n} already exists")
            # else:
            numbers.add(n)                                      # a set contains an element only once
            if len(inputs) >= 5:                                # if cond1 and/or cond2; 'and' higher than `or`
                # actions.pop(0)                                # remove and returns the value
                del inputs[0]                                   # discards the value
            inputs.append(n)
            print(f" 5| {numbers=}, {inputs=}")
        except ValueError:
            pass


if __name__ == "__main__":
    collect_numbers()


"""
Elements seen here
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
