# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This script is intended as a first look at various Python features
(it is not optimal in an algorithmic sense).

Please consider the code as an example of where we want to go.
You do not need to understand every detail right away.
"""

def calc_sum_iteratively(n):                                    # function with parameter(s)
    """ calculates the sum iteratively """                      # doc-string for the function
    result = 0                                                  # definition on-the-fly
    for i in range(1,n+1):                                      # for i=1; i<n+1; ++i
        result += i
    return result

def calc_sum_recursively(n):
    """ calculates the sum recursively """
    return 0 if n <= 0 else n + calc_sum_recursively(n - 1)     # recursive and conditional expression

def calc_sum_directly(n):
    """ calculates the sum directly """
    return n * (n + 1) // 2                                     # integer division

def calculate_all_sums():
    """ calculate all sums in three ways """
    print(" 1| Sum 1..n (end with n<0)")
    while True:                                                 # classical while-loop
        data = input(" 2| Enter n: ")                           # read a string
        n = int(data)                                           # convert it to int (possible exception)
        if n < 0: break                                         # if as one-liner (enabled for Pylint)
        sum_iteratively = calc_sum_iteratively(n = n)           # call with named parameter
        sum_recursively = calc_sum_recursively(n = n)
        sum_directly = calc_sum_directly(n = n)
        print(f" 3| 1+..+{n} =\n"
              f"      {sum_iteratively} (iteratively)\n"        # string interpolation
              f"      {sum_recursively} (recursively)\n"        # short version for 'x={x}'
              f"      {sum_directly} (directly)")


if __name__ == "__main__":                                      # main-guard
    calculate_all_sums()


"""
Elements seen here
  - function definition and call
  - (named) parameter
  - conditional expression
  - for-loop
  - while-loop
  - range
  - input
  - int-cast
  
See also
  - https://docs.python.org/3.13/
  - https://docs.python.org/3.13/reference/index.html
  - https://docs.python.org/3.13/library/index.html
"""
