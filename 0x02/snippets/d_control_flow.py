# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses elementary flow control structures.

Teaching focus
  - This topic is part of the self-study during the exercises or at home.
  - Most of the structures should be known.
  - if, elif, else
  - while, break, continue
  - for, range, enumerate
  - exceptions, else in try

'else' in Exception
  - The else clause is useful in cases where you want to run some code if the
    try block is successful and no exceptions occur, but you want this code to
    be separate from the try block to make clear that it isn't expected to throw
    exceptions. This can help improve the readability of your code.

Pattern Matching
  - This feature from Python 3.10 is discussed in a future unit.

See also
  - https://docs.python.org/3/library/exceptions.html
"""

from utils import print_function_header


@print_function_header
def using_if():
    """ if examples """

    n = 23
    m = -1
    if n == 12 or (n != 12 and m == -1) or (1 < n < 30):        # 'if' without brackets, with 'and' and 'or', a<x<b
        print(" 1| case 1")
    elif n == 23:                           # else-if
        print(" 2| case 2")                 # switch/case later
    else:
        print(" 3| case default")

    s = "True" if 1+1 == 2 else "False"     # the ternary operator :? does not exist here
    print(f" 4| {s=}")

    if (length := len(s)) > 0:              # Walrus-Op., do not forget () here
        print(f" 5| s not empty, {length=}")


@print_function_header
def using_while():
    """ while examples """

    print(" 1| while:", end='')
    i = 0
    while i < 9:                            # 'while' is known
        i += 1
        if i == 3:
            continue
        if i == 6:
            break
        print(f" {i=}", end='')
    print()

    # while True:                                               # if you absolutely want to have 'do-while
    #   ...                                                     # (there is no 'do')
    #   if condition:
    #     break


@print_function_header
def using_for():
    """ for examples """

    lst = [2, 3, 5]
    print(" 1| lst:", end='')
    for item in lst:                        # standard to iterate over a sequence
        print(f" {item=}", end='')
    print()
    print(" 2| enumerate(lst):", end='')
    for i, item in enumerate(lst):          # incl. index and unpacking
        print(f" [{i}]={item}", end='')
    print()

    s = "Hello"
    print(f" 3| {s=}:", end='')
    for c in s:
        print(f" {c=}", end='')
    print()

    print(" 4| [0,3):", end='')
    for i in range(3):
        print(f" {i=}", end='')
    print()

    print(" 5| [2,9) step 3:", end='')
    for i in range(2, 9, 3):
        print(f" {i=}", end='')
    print()


@print_function_header
def using_exceptions():
    """ for exceptions """

    print(" 1| conversion...", end='')
    try:
        n = int("no-number")
        print(f" {n=}")
    except ValueError as e:
        print(f" => value error: {e}")
        # raise                             # if you want to raise it again

    print(" 2| try again...", end='')
    try:
        n = int("12")
        print(f" {n=}")
    except ValueError as e:
        print(f" => value error: {e}")
    except (AssertionError, ArithmeticError) as e:
        print(f" => assertion error: {e}")
    else:                                   # runs if the try block is successful
        print(" 3| everything was ok")
    finally:
        print(" 4| in any case")

    print(" 5| assert...", end='')
    try:
        n = -1
        assert (n > 0), f"n ({n}) is not positive"
    except AssertionError as e:
        print(f" => assertion error: {e}")

    print(" 6| division by 0...", end='')
    try:
        n = int(1/0)
        print(f" {n=}")
    except Exception as e:                  # pylint: disable=broad-exception-caught
        print(f" => unknown error: {e}")    # optional: e.with_traceback()

    print(" 7| raise by myself...", end='')
    try:
        raise RuntimeError("something is wrong")
    except RuntimeError as e:
        print(f" => runtime error: {e}")


if __name__ == "__main__":
    using_if()
    using_while()
    using_for()
    using_exceptions()
