# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features
(it is not optimal in an algorithmic sense).

Please consider the code as an example of where we want to go.
You do not need to understand every detail right away.
"""

def collect_variables():
    """ collect variables from the console, format 'x=12' """

    print(" 1| Enter variables in the form 'x=1' one after the other (w.o. '', end with <return>)")
    variables = {}                                              # a dictionary
    while True:
        data = input(" 2| Input: ")
        idx = data.find("=")                                    # returns index or -1 if not found
        if idx>=0:                                              # if cond1 and cond2 or cond3; 'and' has higher precedence than `or`
            # two variables at once (variable destruction)
            # slicing [from..<until], strip removes trailing and leading whitespace
            name,number = data[:idx].strip(),int(data[idx+1:].strip())
            if name:                                            # short version of not null and not-empty
                if name in variables:                           # does key exist? get it with variables[name]
                    print(f" 3|   old value: {name}={variables[name]}")
                variables[name] = number                        # set value
                print(f" 4| Current (dictionary) {variables=}")
            else:
                print(" 5|   name empty")
        elif data:                                              # or len(data) > 0, or data != ""
            print(" 6|   format error")
        else:
            break
    print()
    return variables

def sum_all_positives(variables):
    print(" 7| sum values>0:")
    result = 0
    for k,v in variables.items():
        if v>0:
            result += v
            print(f" 8|   add {k}={v} => sum={result}")
    print(f" 9| total={result}")

if __name__ == "__main__":
    sum_all_positives(collect_variables())
