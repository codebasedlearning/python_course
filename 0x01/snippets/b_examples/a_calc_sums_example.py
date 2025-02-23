# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features
(it is not optimal in an algorithmic sense).

Please consider the code as an example of where we want to go.
You do not need to understand every detail right away.
"""

def calc_sum_iteratively(n):                                    # function with parameter(s)
    """calculates the sum iteratively"""                        # doc-string for the function
    result = 0                                                  # definition on-the-fly
    for i in range(1,n+1):                                      # for i=1; i<n+1; ++i
        result += i
    return result

def calc_sum_recursively(n):
    return 0 if n <= 0 else n + calc_sum_recursively(n - 1)     # recursive and conditional expression

def calc_sum_fast(n):
    return n * (n + 1) // 2                                     # integer division

def calculate_all_sums():
    """ calculate all sums in three ways """
    while True:                                                 # classical while-loop
        data = input(" 1| Enter n (end with <0): ")             # read a string
        end = int(data)                                         # convert it to int (possible exception)
        if end < 0: break                                       # if as one-liner
        sum_iteratively = calc_sum_iteratively(n = end)         # call with named parameter
        sum_recursively = calc_sum_recursively(n = end)
        sum_fast = calc_sum_fast(n = end)
        print(f" 2| sum 1..{end} =\n"
              f"      {sum_iteratively} (iteratively)\n"        # string interpolation
              f"      {sum_recursively=}\n"                     # short version for 'x={x}'
              f"      {sum_fast=}\n")

if __name__ == "__main__":                                      # main-guard
    calculate_all_sums()
