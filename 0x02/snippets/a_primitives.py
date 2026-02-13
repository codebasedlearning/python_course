# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses primitive types.

Teaching focus
  - primitive types, i.e. ints, bools, floats, and strings
  - treating 'things' as 'True' or 'False'
  - conversions
  - typical operations
  - short-circuiting
  - slicing, indexing, split, representation with encoding and decoding.
  - discussion of equality.

Ints
  - Ints can be of any length, i.e. "exact".
  - The memory requirement depends on the length, so short ints require
    less memory.

Bools
  - It is important to note that a conversion to a boolean variable
    essentially tests whether the value is some kind of zero or empty (false)
    or not, i.e. !=0 (true).
  - Boolean-operator precedence: not > and > or
  - https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not

Floats
  - Almost all Python variants implement 'float' according to IEEE-754
    "double precision", i.e. as a standard 'double'.
  - Constants like 'inf' can sometimes be used to initialize variables
    in algorithms.
  - Be aware that operations with 'nan' or 'inf' may result in strange
    or unexpected behavior.
    Any operation with 'nan' results in 'nan'. For 'inf' it depends.
  - Normal floating-point math often stays on the CPU’s fast path
    (vectorized, pipelined). As soon as 'inf' or 'nan' comes into play,
    CPUs and runtimes frequently have to take slow paths, do extra checks
    or sometimes raise or mask IEEE-754 exceptions.

Strings
  - Surprisingly, you can define strings, but also comments, with ''
    instead of "". The choice is free, and there is no recommendation.
    Some use "" for strings and '' for regular expressions or keys.
  - There are, of course, countless string operations. It is important to know
    that strings are immutable, i.e. all operations such as '+=', 'replace',
    'upper' etc. always return a new string.
  - https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
  - https://www.w3schools.com/python/python_strings_methods.asp

None
  - None is often used to represent an unspecified value, such as a parameter
    that is not set. It is most similar to a null reference and false
    if converted to a boolean variable.

Value Equality (`==`):
  - Checks if two objects have the same value.
  - For most built-in types, Python uses type-specific `__eq__` methods to
    implement value comparison.
  - Two different objects in memory may still be equal in terms of value.

Identity Equality (`is`):
  - Checks if two objects are the exact same instance, i.e., identical in memory.
  - `is` evaluates to `True` only if two variables refer to the same object.

See also
  - https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
"""

import math
import textwrap

from utils import print_function_header

"""
Topic: Primitive types
"""

@print_function_header
def using_ints():
    """ int basics. """

    n = 12                                  # 'n' references object 12.
    m: int = -3                             # Negative, with type hint.
    print(f" 1| {n=}, {type(n)=}, {m=}")

    n1 = int(23)                            # Calling the class to produce an instance. # noqa: UP018
    n2 = int(99.9)                          # Type conversion, cast float -> int (truncated toward zero).
    n3 = int("-42")                         # Cast str -> int, may throw.
    print(f" 2| int(23)={n1}, int(99.9)={n2}, int('-42')={n3}")

    lg = 1234567890123456789012345678901234567890
    print(f" 3| (long) int: {lg=}, {type(lg)=}")
    print(f" 4| {lg - 1=}")
    print(f" 5| {lg * lg=}")                # Do not name a long var 'l'.

@print_function_header
def using_bools():
    """ bool basics. """

    b = True
    not_b: bool = False                     # With type hint.
    print(f" 1| {b=}, {type(b)=}, {not_b=}")

    # If the value is some kind of zero or empty then it is false.
    print(f" 2| {bool(123)=}, {bool(0)=}\n"
          f"    {bool('xy')=}, {bool('0')=}, {bool('')=}\n"
          f"    {bool({1,2})=}, {bool(set())=}\n"
          f"    {bool([1])=}, {bool([])=}\n"
          f"    {bool(None)=}")

@print_function_header
def bool_ops():
    """ combining bools.  """

    b = True
    not_b = False
    print(f" 1| {not b=}, {not_b=}")        # not

    x1, x2, x3 = 1, 2, 3                    # and, or; operator precedence: not > and > or
    print(f" 2| {(x1 < x2)=}, {(x2 < x1)=}, {(x1 < x2 and x1 < x3)=}, {(x2 < x1 or x3 < x2)=}")

    def never_called():
        raise RuntimeError(" a| -> should never happen")

    # Short-circuiting means a boolean expression stops evaluating as soon as
    # the result is already determined, so later operands may never run.
    x = 1
    b1 = (x>0) or never_called()
    b2 = (x<0) and never_called()
    print(f" 3| {b1=}, {b2=}")

@print_function_header
def using_floats():
    """ float basics. """

    d = 2.5                                 # 'd' references a floating point number.
    f: float = 3.5                          # With type hint.
    print(f" 1| {d=}, {type(d)=}, {f=}")

    # cast to float
    print(f" 2| {float(23)=}, {float("3.1415")=}, {float(True)=}")

@print_function_header
def float_ops():
    """ Special floats 'nan' and 'inf'. """

    nan = float('nan')                      # 'nan' = not-a-number.
    print(f" 1| {nan=}, {math.isnan(nan)=}")

    inf = float('inf')                      # Also '-inf'.
    print(f" 2| {inf=}, {math.isinf(inf)=}")

    # Be careful with operations involving 'nan' or 'inf'.
    d = 2.5
    print(f" 3| {d=}, {(d == d)=}, {(nan == nan)=}, {(inf == inf)=}, {(d < inf)=}")
    print(f" 4| {(d+nan)=}, {(d+inf)=}, {(inf-inf)=}, {(1/inf)=}")

@print_function_header
def using_strings():
    """ string basics. """

    s = "Hello Python!"                     # A string, or s: str = "..." with type hint.
    print(f" 1| {s=}, {len(s)=}, {type(s)=}")

    print(f" 2| {str(12)=}, {str(34.8)}, {str(True)=}, {str(None)=}")
    smile = "smile 😀"                       # Python 3 uses Unicode to represent strings.
    print(f" 3| {smile=}")

    smile_utf8_bytes = smile.encode("utf-8") # Encode to utf-8 and decode back to string.
    smile_str = smile_utf8_bytes.decode("utf-8")
    print(f" 4| {smile_utf8_bytes=}, {type(smile_utf8_bytes)=}")
    print(f" 5| {smile_str=}, {type(smile_str)=}")

@print_function_header
def string_ops():
    """ Common string operations. """

    s = "  Simple Text  "
    print(f" 1| {s=}, {len(s)=}")
    print(f" 2| {s.upper()=}, {s.lower()=}")
    print(f" 3| {s.strip()=}, {s.replace('e', '3')=}")
    print(f" 4| {('Tex' in s)=}")

    t = "Lorem ipsum dolor sit amet"
    print(f" 5| {t=}, {len(t)=}")
    words = t.split()                       # The result is a list.
    print(f" 6| {words=}, {len(words)=}, {type(words)=}")

    data = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
      - Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
        nisi ut aliquip ex ea commodo consequat. 
    """
    lines = data.split('\n')
    print(f" 7| {lines=}")                  # Not optimal: first line empty, too much indent.

    with_indents = textwrap.dedent(data).lstrip().split('\n')
    print(f" 8| {with_indents=}")           # Leading indent gone, inner indent preserved.


"""
Topic: Slicing and Indexing

Slicing works on all sequence types in Python. That includes strings, lists, 
tuples, and more.
"""

@print_function_header
def using_slicing():
    """ Slicing and indexing. """

    s = "0123456789abcdefghij"
    print(f" 1| {s=}, {len(s)=}")
    print(f" 2| {s[2]=}")                   # A single character (element).
    print(f" 3| {s[-3]=}")                  # char at end-pos=length-3
    print(f" 4| {s[2:4]=}")                 # start- (incl.), end-pos (excl.)
    print(f" 5| {s[:4]=}")                  # start=0, end-pos=4 (excl.)
    print(f" 6| {s[4:]=}")                  # start=4, end-pos=length
    print(f" 7| {s[-4:-2]=}")               # start=length-4, end-pos=length-2
    print(f" 8| {s[-1:]=}")                 # start=length-1, end-pos=length
    print(f" 9| {s[3:-2]=}")                # start=3, end-pos=-2
    print(f"10| {s[::2]=}")                 # start=0, end-pos=length, step=2

    # Slicing for lists (preview).
    fib = [1,1,2,3,5,8,13]
    print(f"11| {fib[2:4]=}")               # start- (incl.), end-pos (excl.)


"""
Topic: Equality

In Python, equality refers to the comparison between objects to determine if 
they have the same value (`==`) or if they are the same object in memory (`is`).
"""

@print_function_header
def what_means_equal():
    """ 'Value Equality' vs. 'Identity Equality'. """

    s = "123"                               # String literals are created at compile time, here Python sees "123" twice.
    t = "123"
    print(f" 1| {s=}, {t=}, {(s==t)=}, {(s is t)=} | {id(s)=}, {id(t)=}")

    s += '4'
    print(f" 2| {s=}, {t=}, {(s==t)=}, {(s is t)=} | {id(s)=}, {id(t)=}")

    a = [1, 2, 3]                           # Lists are mutable, so they are different objects.
    b = [1, 2, 3]
    print(f" 3| {a=}, {b=}, {(a==b)=}, {(a is b)=} | {id(a)=}, {id(b)=}")

    a.append(4)
    print(f" 4| {a=}, {b=}, {(a==b)=}, {(a is b)=} | {id(a)=}, {id(b)=}")

    # Preview ('study_int_ids') int-Objects: replace 1023 with 23.
    n = 1023
    m = n+1-int(math.fabs(-1))
    print(f" 5| {n=}, {m=}, {(n==m)=}, {(n is m)=} | {id(n)=}, {id(m)=}")


if __name__ == "__main__":
    # Primitives and ops
    using_ints()
    using_bools()
    bool_ops()
    using_floats()
    float_ops()
    using_strings()
    string_ops()

    # Slicing
    using_slicing()

    # Equality
    what_means_equal()
