# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses function calling.

Teaching focus
  - Call functions with positional and with named arguments is needed.
  - Default values are a common Pitfall.
"""


def sum_up(base, a, b, c=3):
    """ Sum up all parameters, c is optional with default value. """
    return base + a + b + c


def sum_up_positional():
    """ sum up with positional arguments """
    print("\nsum_up_positional\n=================")
    sum1 = sum_up(10, 1, 2, 3)                                  # all arguments given
    sum2 = sum_up(10, 1, 2)                                     # here c is default
    print(f" 1| {sum1=}, {sum2=}")


def sum_up_named():
    """ sum up with named arguments """
    print("\nsum_up_named\n============")
    sum1 = sum_up(base=10, a=1, b=2, c=3)                       # all arguments given
    sum2 = sum_up(10, b=2, c=3, a=1)                            # different order
    print(f" 1| {sum1=}, {sum2=}")


def add_positive_x_to_list(x, lst=[]):                          # # pylint: disable=dangerous-default-value
    """ add x to lst if x > 0 """
    if x > 0:
        lst.append(x)
    return lst


def strange_add():                                              # comments?
    """ where is the problem? """
    print("\nstrange_add\n===========")
    print(f" 1| 3+[1,2]={add_positive_x_to_list(3, [1, 2])}")
    print(f" 2| 0+[1,2]={add_positive_x_to_list(0, [1, 2])}")
    print(f" 3| 1+[]={add_positive_x_to_list(1)}")
    print(f" 4| 4+[1,2,3]={add_positive_x_to_list(4, [1, 2, 3])}")
    print(f" 5| 0+[]={add_positive_x_to_list(0)}")


if __name__ == "__main__":
    sum_up_positional()
    sum_up_named()
    strange_add()


###############################################################################


"""
Summary

Topics
  - function calling
  - positional and named arguments
  - default values

Parameters
  - When calling the function, the parameters can be specified with or without 
    names. 
  - Calling a function with named arguments usually improves readability 
    enormously. It is even strongly recommended if the context or function 
    does not immediately indicate which parameter has which meaning, for example 
        configure(12,"/path",true,true,15) ???
    On the other hand, if the context or the name of the function is clear, 
    this can be omitted, e.g.
        sin(12)
  - The ability to use named arguments affects the concrete manifestations 
    of certain patterns, e. g. the builder or factory pattern.
  - More on this topic such as 'args' and 'kwargs' will follow later.

Mutable Defaults
  - From JetBrains: You should avoid using mutable objects as default arguments 
    in Python functions. This is because default arguments in Python are evaluated 
    only once at the time of function definition, not each time the function is 
    called. If a mutable object like a list or a dictionary is used as a default 
    argument and that object is modified within the function, the modifications 
    will persist in subsequent calls to the function.

See also
  - https://docs.python.org/3/reference/compound_stmts.html#function-definitions
  - https://docs.python.org/3/tutorial/controlflow.html#defining-functions
  - https://peps.python.org/pep-0008/#function-and-method-arguments
"""
