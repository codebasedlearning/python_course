# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features
(it is not optimal in an algorithmic sense).

Please consider the code as an example of where we want to go.
You do not need to understand every detail right away.
"""

def read_data():
    variables = set()                                           # a set
    actions = []                                                # a list
    print(" 1| Collect numbers in a set and actions in a finite FIFO list")
    while (line := input(" 2| Please enter n: ")) != "":
        try:
            n = int(line)
            if n in variables:
                print(f" 3| {n} already exists")
            # else:
            variables.add(n)                                    # a set contains an element only once
            if len(actions) >= 5:
                # actions.pop(0)                                # returns the value
                del actions[0]                                  # discards the value
            actions.append(n)
            print(f" 5| {variables=}, {actions=}")
        except ValueError:
            pass

if __name__ == "__main__":
    read_data()
