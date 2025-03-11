# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses positional and keyword arguments.

Teaching focus
  - understand the calling mechanics
"""


def sum_iterables(iterable):
    """ sum up an iterable """
    # variant 1
    # result = 0
    # for x in iterable:
    #    result += x
    # return result
    #
    # variant 2
    return sum(iterable)

def sum_varying_number(*args):                                                     # (A) iterable
    """ sum up a varying number of positional arguments """
    print(f" a|   {type(args)=}")
    # variant 1 (as before)
    result = 0
    for x in args:
        result += x
    return result
    #
    # variant 2 (as before)
    # return sum(args)

def sum_with_base(base, *args):
    """ sum up base and a varying number of positional arguments """
    return base + sum(args)

def show_args():
    """ work with args """
    print("\nshow_args\n=========")

    result = sum_iterables([1, 2, 3])
    print(f" 1| {result=}")

    result = sum_varying_number(1,2,3,4,5)
    print(f" 2| {result=}")

    result = sum_varying_number(3,*[4,5],6)                     # unpacking as before
    print(f" 3| {result=}")

    # problem, why?
    # result = sum_varying_number(base=1,*[4,5])


def concat_dict(dct):
    """ concatenate a dictionary """
    # variant 1
    # result = ""
    # for value in dct.values():
    #    result += value
    # return result
    #
    # variant 2
    return "".join(dct.values())                                # ""=separator


def concat_kwargs(**kwargs):
    """ concatenate a varying number of keyword arguments """
    print(f" b|   {type(kwargs)=}")
    # result = ""
    # for arg in kwargs.values():
    #    result += arg
    # return result
    return "".join(kwargs.values())


def show_kwargs():
    """ work with keyword arguments """
    print("\nshow_kwargs\n===========")

    result = concat_dict({'a': 'one', 'b': 'two'})
    print(f" 1| {result=}")

    dct1 = {'a': 'one'}
    dct2 = {'b': 'two'}
    result = concat_kwargs(**dct1, **dct2)
    print(f" 2| {result=}")


def concat_mixed(a, b, *args, **kwargs):
    """ concatenate a varying number of arguments and keyword arguments """
    lst = [*args]
    dct = {**kwargs}
    return f"| {a=}, {b=}, args={lst}, kwargs={dct} |"


def show_mixed1():
    """ work with positional and keyword arguments """
    print("\nshow_mixed1\n===========")

    result = concat_mixed(1, 2, 3, 4, base=5)
    print(f" 1| {result=}")

    result = concat_mixed(a=1, b=2, base=5)
    print(f" 2| {result=}")

    result = concat_mixed(*(1,2,3), **{'base':5})
    print(f" 5| {result=}")

    # error: concat_mixed(1, 2, 3, 4, a=5)          multiple 'a'
    #        concat_mixed(a=1, b=2, 3, base=5)      positional argument follows keyword argument
    #        concat_mixed(1, c=1, d=2)              missing 1 required positional argument: 'b'
    #        concat_mixed(*(1,2,3), base=5, **{'base':6})   multiple 'base'

    result = concat_mixed(*(1,2,3), **{'base':5, **{'base':6}})
    print(f" 6| {result=}")


# '/' => all parameters before are "positional-only" (from Python 3.8)
# '*' => end of positional parameters, start of "keyword-only"

def concat_pos_or_kw(pos1, pos2, /, pos_or_kw, *, kw):
    """ concatenate positional and/or keyword arguments """
    return f"| {pos1=}, {pos2=}, {pos_or_kw=}, {kw=} |"


def show_mixed2():
    """ work with positional and keyword arguments """
    print("\nshow_mixed2\n===========")

    result = concat_pos_or_kw(1, 2, 3, kw='key')
    print(f" 1| {result=}")
    result = concat_pos_or_kw(1, 2, pos_or_kw=3, kw='key')
    print(f" 2| {result=}")
    # error: concat_pos_or_kw(1, pos2=2, pos_or_kw=3, kw='key') positional-only argument
    #        concat_pos_or_kw(1, 2, 3, 'key')                   4 pos. args


if __name__ == "__main__":
    show_args()
    show_kwargs()
    show_mixed1()
    show_mixed2()


###############################################################################


"""
Summary

Topics
  - (mix of) args and kwargs
  - positional-only and keyword-only arguments, '/' and '*'
  - starred expressions

iterable
  - From Python doc: The for statement is used to iterate over the elements of 
    a sequence (such as a string, tuple or list) or other iterable object.
  - https://docs.python.org/3/glossary.html#term-iterable

args
  - 'sum_varying_number' is a functions that takes a varying number of 
    input arguments, *args bundles these arguments.
  - Note that 'args' is just a name and could also be called something else. 
    The important thing is the '*'.
  - The type of 'args' is a tuple!
  - '*' is the unpacking operator.
  - https://realpython.com/python-kwargs-and-args/

kwargs
  - Similar to args, this time 'kwargs' collects all parameters given as 
    keyword:value.
  - https://realpython.com/python-kwargs-and-args/

mix of args and kwargs
  - The correct order is:
      - Standard arguments
      - *args arguments = positional args
      - **kwargs arguments = keyword arguments
  - '/': all parameters before are "positional-only" (from Python 3.8)
  - '*': end of positional parameters, start of "keyword-only"

starred expressions
  - Python splits the right-hand side, with the 'starred expression' taking 
    the expanded arguments. 
  - Overall, however, it must fit, i.e. there must not be several 
    starred expressions, nor too many or too few variables. In summary
      - *elements, = iterable       causes elements to be a list
      - elements = *iterable,       causes elements to be a tuple
  - https://realpython.com/python-kwargs-and-args/
  - https://book.pythontips.com/en/latest/args_and_kwargs.html#
  - https://peps.python.org/pep-0448/
  
'_'
  - Actually, there is nothing special here, because '_' is a quite normal 
    variable name. However, by convention, '_' stands for 'not needed' 
    ('discard').

See also
  - https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists
"""
