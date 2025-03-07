# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features.

Teaching focus
  - Consider the code as an example of where we want to go.
  - You do not need to understand every detail right away.
  - Code it is not optimal in an algorithmic sense.
"""


def try_parse(value, target_type):
    """ converts value into target_type or None """
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return None


def collect_variables():
    """ collect variables from the console, format 'x=12' """

    print(" 1| Enter variables in the form 'x=1' one after the other (w.o. '', end with <return>)")
    variables = {}                                              # a dictionary

    # classical style (but skip)
    #
    #   while True:
    #       data = input(" 2| Input: ")
    #       # returns index or -1 if not found
    #       idx = data.find("=")
    #       if idx >= 0:
    #           # two variables at once (variable destruction)
    #           # slicing [from..<until], strip removes trailing and leading whitespace
    #           name, number = data[:idx].strip(), int(data[idx + 1:].strip())

    while (data := input(" 2| Enter variable: ")) != "":
        p1,p2,p3 = data.partition("=")                          # variable destruction
        if (name:=p1.strip())== "" or (p2 != "=") or (number:=try_parse(p3, int)) is None:
            print(f" 3|   format error ({name=},{number=})")    # where is the problem here?
            continue
        if name in variables:                                   # does key exist? get it with variables[name]
            print(f" 4|   old value: {name}={variables[name]}")
        variables[name] = number                                # set value
        print(f" 5| Current (dictionary) {variables=}")
    return variables


def sum_all_positives(variables):
    """ sum all values >0 """
    print(" 6| sum values>0:")
    total = 0
    for k,v in variables.items():
        if v>0:
            total += v
            print(f" 7| add {k}={v} => subtotal={total}")
    print(f" 8| {total=}")
    # variant, more Pythonic?
    # positive_values = {k: v for k, v in variables.items() if v > 0}
    # total = sum(positive_values.values())


if __name__ == "__main__":
    sum_all_positives(collect_variables())


###############################################################################


"""
Summary

Topics
  - None
  - slicing, strip, partition
  - try-except
  - dictionary
  - tuple
  - variable destruction

See also
  - https://docs.python.org/3.13/
  - https://docs.python.org/3.13/reference/index.html
  - https://docs.python.org/3.13/library/index.html
"""
