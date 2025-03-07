# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
The aim of this snippet is to show simple input and output.

Teaching focus
  - Print all we need.
  - Read from the console, needed for examples and exercises.
"""


def using_print():
    """ various printings """
    print("\nusing_print\n===========")

    print(" 1| simple 'print'")                                 # nothing special
    print(" 2| print without", end='')                          # no new line
    print(" new line")

    print(f" 3| expressions in f-strings: {2*7=}")              # formatted string ('f')
    print(f" 4| {{ and }} in f-strings, e.g. a set: {{ 1,1,{1+1} }}")

    print(" 5| escaped chars, e.g. \", \', \\, \\n")            # with special chars
    print(r" 6| as r-string (raw), i.e. as it is '\n'")         # raw string ('r')


def using_input():
    """ read from the console """
    print("\nusing_input\n===========")

    name = input(" 1| your name: ")                                  # read as string
    print(f" 2| Hello '{name}'!")


if __name__ == "__main__":
    using_print()
    using_input()


###############################################################################


"""
Summary

Topics
  - formatted print
  - escape sequences
  - raw strings
  - input

See also
  - https://realpython.com/python-print/
  - https://docs.python.org/3/howto/unicode.html
  - https://realpython.com/python-print/#adding-colors-with-ansi-escape-sequences
"""
