# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This snippet discusses bools. """


def using_bools():
    """ bool basics """
    print("\nusing_bools\n===========")

    b = True                                                    # a bool
    # b: bool = True                                            # with type hint
    print(f" 1| {b=}, {type(b)=}")

    # if the value is some kind of zero or empty then it is false
    print(f" 2| {bool(123)=}, {bool(0)=}\n"
          f"    {bool('xy')=}, {bool('0')=}, {bool('')=}\n"
          f"    {bool({1,2})=}, {bool(set())=}\n"
          f"    {bool([1])=}, {bool([])=}\n"
          f"    {bool(None)=}")


def boolean_operations():
    """ combining bools  """
    print("\nboolean_operations\n==================")

    b = True
    not_b = False
    print(f" 1| {not b=}, {not_b=}")                            # not

    x1, x2, x3 = 1, 2, 3                                        # and, or
    print(f" 2| {(x1 < x2)=}, {(x2 < x1)=}, {(x1 < x2 and x1 < x3)=}, {(x2 < x1 or x3 < x2)=}")

    def never_called():
        raise RuntimeError("should never happen")
    x = 1
    b1 = (x>0) or never_called()                                # short-circuiting, i.e. not evaluating the following
    b2 = (x<0) and never_called()                               # terms if the operation is already defined
    print(f" 3| {b1=}, {b2=}")


if __name__ == "__main__":
    using_bools()
    boolean_operations()


###############################################################################


"""
Summary

Topics
  - bools
  - conversions
  - short-circuiting

Conversion
  - It is important to note that a conversion to a boolean variable
    essentially tests whether the value is some kind of zero or empty (false)
    or not, i.e. !=0 (true).
    
None
  - None is often used to represent an unspecified value, such as a parameter
    that is not set. It is most similar to a null reference, and false
    if converted to a boolean variable.

Refs
  - https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not
"""
