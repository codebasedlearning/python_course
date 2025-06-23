# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about descriptor functions.

Teaching focus
  - descriptor functions
"""

import types

"""
Most from https://docs.python.org/3/howto/descriptor.html#functions-and-methods

  - Functions stored in class dictionaries get turned into methods when invoked. 
  - Methods only differ from regular functions in that the object instance is prepended to the other arguments. 
  - By convention, the instance is called 'self' but could be called 'this' or any other variable name.
"""


# start with the conversion of a function into a method,
# see https://docs.python.org/3/library/types.html#types.MethodType

def bound_methods():
    """ ... """
    print("\nbound_methods\n=============")

    class MyMethodType:                                 # similar Objects/classobject.c
        def __init__(self, func, obj):
            self.__func__ = func
            self.__self__ = obj

        def __call__(self, *args, **kwargs):
            func = self.__func__
            obj = self.__self__
            return func(obj, *args, **kwargs)           # here the object becomes the first arg.

    class C:
        def __init__(self, n: int):
            self.n = n
            self.n_as_str_v2 = types.MethodType(lambda this: f"n3: {this.n=}", self)
            self.n_as_str_v3 = MyMethodType(lambda this: f"n2: {this.n=}", self)

        def n_as_str_v1(self):
            return f"n1: {self.n=}"

    c = C(n=23)
    print(f" 1| c.n_as_str_v1: {c.n_as_str_v1()}, {type(c.n_as_str_v1)}\n"
          f"    c.n_as_str_v2: {c.n_as_str_v2()}, {type(c.n_as_str_v2)}\n"
          f"    c.n_as_str_v3: {c.n_as_str_v3()}, {type(c.n_as_str_v3)}")


"""
To support automatic creation of methods, functions include the __get__() method for binding methods during 
attribute access (as in c.f() ).
This means that functions are _non-data descriptors_ that return bound methods during dotted lookup from 
an instance. That looks like:

class Function:                                                     # similar Objects/funcobject.c
    ...
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return MethodType(self, obj)
"""


def functions_are_non_data_descriptors():
    """ ... """
    print("\nfunctions_are_non_data_descriptors\n==================================")

    # consider a regular function
    def f():
        ...
    print(f" 1| {type(f)=}, get exists? {f.__get__ is not None}\n")  # todo hasattr

    class C:
        def f(self, x):
            return x

    # Accessing the function through the class dictionary does not invoke __get__().
    # Instead, it just returns the underlying function object:
    print(f" 2| {C.__dict__['f']=}")

    # Dotted access from a class calls __get__() which just returns the underlying function unchanged:
    print(f" 3| {C.f=}")

    # The dotted lookup calls __get__() which returns a bound method object:
    c = C()
    print(f" 4| {c.f=}\n"
          f"    call: {c.f(23)}")

    # cf. MethodType - the bound method stores the underlying function and the bound instance:
    print(f" 5| {c.f.__func__=}, {c.f.__self__}\n"
          f"    __self__ is c? {c is c.f.__self__}")


"""
Static methods return the underlying function without changes. 
Unlike static methods, class methods prepend the class reference to the argument list before calling the function. 
"""


def simulate_static_and_class_methods():
    """ ... """
    print("\nsimulate_static_and_class_methods\n=================================")

    class MyStaticMethod:                                             # not complete
        def __init__(self, f):
            self.f = f

        def __get__(self, obj, objtype=None):
            return self.f

        # def __call__(self, *args, **kwds):
        #     return self.f(*args, **kwds)

    class C:
        # instead of @staticmethod
        @MyStaticMethod
        def f(x):
            return x

    c = C()
    print(f" 1| static method: {c.f(12)=}")                         # same for C.f(12)

    class MyClassMethod:                                              # not complete
        def __init__(self, f):
            self.f = f

        def __get__(self, obj, cls=None):
            if cls is None:
                cls = type(obj)

            return types.MethodType(self.f, cls)

    class D:
        # instead of @classmethod
        @MyClassMethod
        def f_str(cls, x):
            return f"{x=} in {cls}"

    d = D()
    print(f" 2| class method:  {d.f_str(23)}")                      # same for D.f_str(12)


if __name__ == "__main__":
    bound_methods()
    functions_are_non_data_descriptors()
    simulate_static_and_class_methods()


"""
Most comments are embedded in the script. References:

https://docs.python.org/3/howto/descriptor.html
https://realpython.com/python-descriptors/
https://python-reference.readthedocs.io/en/latest/docs/dunderdsc/

https://towardsdatascience.com/python-descriptors-and-how-to-use-them-5167d506af84
https://elfi-y.medium.com/python-descriptor-a-thorough-guide-60a915f67aa9
https://blog.peterlamut.com/2018/11/04/python-attribute-lookup-explained-in-detail/
"""
