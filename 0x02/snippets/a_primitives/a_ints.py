# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses integers and object equality.

Teaching focus
  - The 'using_ints' function is discussed in detail, as its structure is
    a template for the others.
  - A notable feature is the discussion of equality in 'what_means_equal'.
  - It is interesting to look at the internal representation of integers
    in the next snippet.
"""

import math


def using_ints():
    """ int basics """
    print("\nusing_ints\n==========")

    n = 12                                                      # 'n' references an object 12
    m: int = -3                                                 # negative, with type hint
    print(f" 1| {n=}, {type(n)=}, {m=}")

    n1 = int(23)                                                # calling the class to produce an instance
    n2 = int(99.9)                                              # type convertion, cast float -> int
    n3 = int("-42")                                             # str -> int
    print(f" 2| int(23)={n1}, int(99.9)={n2}, int('-42')={n3}")

    lg = 1234567890123456789012345678901234567890               # do not use 'l'
    print(f" 3| (long) int: {lg=}, {type(lg)=}")
    print(f" 4| {lg - 1=}")
    print(f" 5| {lg * lg=}")

# In Python, equality refers to the comparison between objects to determine
# if they have the same value (`==`) or if they are the same object in memory (`is`).

def what_means_equal():
    """ discuss 'Value Equality' vs 'Identity Equality' """
    print("\nwhat_means_equal\n================")

    # let's look at a list first when we discuss equality, this is as we expect
    a = [1, 2, 3]
    b = [1, 2, 3]                                               # the lists refer not to the same object
    print(f" 1| {a=}, {b=}, {(a==b)=}, {(a is b)=} | {id(a)=}, {id(b)=}")
    a.append(4)
    print(f" 2| {a=}, {b=}, {(a==b)=}, {(a is b)=} | {id(a)=}, {id(b)=}\n")

    # now the 'easy' ints...
    n = 1023
    print(f" 3| {n=} | {id(n)=}")

    m1 = 1023
    print(f" 4| {m1=}, {(n==m1)=}, {(n is m1)=}  | {id(m1)=}")  # same object

    m2 = 1024-1
    print(f" 5| {m2=}, {(n==m2)=}, {(n is m2)=}  | {id(m2)=}")  # Python knows that, same object

    m3 = 1024-int(math.fabs(-1))
    print(f" 6| {m3=}, {(n==m3)=}, {(n is m3)=} | {id(m3)=}\n") # at runtime, equal but not the same

    # same as before but with smaller int: 23
    n = 23
    print(f" 7| {n=} | {id(n)=}")

    m1 = 23                                                   # same object
    print(f" 8| {m1=}, {(n==m1)=}, {(n is m1)=}  | {id(m1)=}")

    m2 = 24-1                                                 # Python knows that
    print(f" 9| {m2=}, {(n==m2)=}, {(n is m2)=}  | {id(m2)=}")

    m3 = 24-int(math.fabs(-1))                                # at runtime, equal and the same!
    print(f"10| {m3=}, {(n==m3)=}, {(n is m3)=} | {id(m3)=}\n")

    # some ints are other than others... try to find out
    for n in (-7,-6,-5,-4,0,100,200,255,256,257,258):
        m3 = n+1-int(math.fabs(-1))
        print(f"11| {n=} {m3=}, {(n==m3)=}, {(n is m3)=} | {id(n)=}, {id(m3)=}")


if __name__ == "__main__":
    using_ints()
    what_means_equal()


###############################################################################


"""
Summary

Topics
  - ints
  - value and identity equality

Ints
  - Ints can be of any length, i.e. exact.
  - The memory requirement depends on the length, so short ints require less memory.

Value Equality (`==`):
  - checks if two objects have the same value;
  - for most built-in types, Python uses type-specific `__eq__` methods to implement value comparison;
  - two different objects in memory may still be equal in terms of value.

Identity Equality (`is`):
  - checks if two objects are the exact same instance, i.e., identical in memory;
  - `is` evaluates to `True` only if two variables reference the same object.

See also
  - https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
"""
