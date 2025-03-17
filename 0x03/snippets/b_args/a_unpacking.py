# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses various ways of unpacking.

Teaching focus
  - recap unpacking
  - introduce *, **, args and kwargs (as arguments)
"""


def play_with_unpacking():
    """ examples with unpacking """
    print("\nplay_with_unpacking\n===================")

    data1 = [2, 3, 4]
    data2 = (5, 6)
    data17 = [1, *data1, *data2, 7]
    print(f" 1| {data17=}")

    data15 = [1, 2, 3, 4, 5]
    a, *b, c = data15                                           # starred expression with variable unpacking, not greedy
    print(f" 2| {a=}, {b=}, {c=}, {type(b)=}")                  # unpacked b is (always) a list (not a tuple)

    # note, this is an error: 'a, *b, *c = data26' - Why?

    bc = {"b": 2, "c": 3}
    abcd = {"a": 1, **bc, "d": 4}                               # also unpacking, but now a dict
    print(f" 3| {abcd=}, {type(abcd)=}\n")

    print(" => What is a,b,c,...?\n----------------------\n")

    # Note: This is all questionable from a type safety perspective (or mypy),
    # but we're primarily concerned with the result to help understand.

    data26 = (2, 3, 4, 5, 6)
    a, b, *c, d, e = data26
    print(f" 4| {a=}, {b=}, {c=}, {d=}, {e=}\n")

    _, *b, c = data26
    print(f" 5| {b=}, {c=}\n")

    a, b, *_ = data26
    print(f" 6| {a=}, {b=}\n")

    *b, = data26                                                # difference to b=data26 ?
    print(f" 7| {b=}\n")

    # b = *data26,                                              # ',' necessary, but potential code readability issue
    b = (*data26,)
    print(f" 8| {b=}\n")

    b = [*range(4), 4]
    print(f" 9| {b=}\n")

    b = *range(4), 4                                            # from Python 3.5
    print(f"10| {b=}\n")


def make_number(c2, c1, c0):
    """ consider c_i as 10-digits """
    return c2*100+c1*10+c0

def summarize_function_calling():
    """ summarize standard callings """
    print("\nsummarize_function_calling\n==========================")

    print(f" 1| positional: {make_number(1,2,3)=}")
    print(f" 2| named:      {make_number(c2=7,c1=5,c0=3)=}")

    # positional arguments can be provided by a tuple
    five = (1,2,3)
    print(f" 3| from tuple: {five=}, {make_number(*five)=}")    # '*' unpacks args

    # this is a problem (4 args)
    # print(f" 4| from tuple: {args=}, {make_number(1,*args)=}")
    print(f" 4| from tuple: {five=}, {make_number(1,*five[1:])=}")

    # named arguments can be provided by a dictionary
    kwargs = {'c0':3, 'c1':5, 'c2':7 }
    print(f" 5| from dict:  {kwargs=}, {make_number(**kwargs)=}")   # '**' unpacks keyword-args

    # this is also a problem ('c2' twice)
    # print(f" 6| from tuple: {args=}, {make_number(c2=7,**kwargs)=}")
    del kwargs["c2"]
    print(f" 6| from dict:  {kwargs=}, {make_number(c2=7,**kwargs)=}")  # pylint: disable=repeated-keyword
    del kwargs["c1"]
    five = (5,)
    print(f" 7| mixed:      {five=}, {kwargs=}, {make_number(7,*five,**kwargs)=}")  # pylint: disable=redundant-keyword-arg
    # So in practice, mixing all these things might not seem so clever...


if __name__ == "__main__":
    play_with_unpacking()
    summarize_function_calling()


###############################################################################


"""
Summary

Topics
  - unpacking
  - starred expressions (* and **)

Starred expressions
  - They allow you to unpack or capture multiple elements from a sequence 
    (like a list, tuple, or other iterable) in a concise and flexible way. 
    The `*` operator can be used in various contexts, such as assignments, 
    function arguments, or list comprehensions.

See also
  - https://docs.python.org/3/reference/expressions.html#expression-lists
"""
