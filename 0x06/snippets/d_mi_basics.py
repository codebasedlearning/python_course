# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses multiple inheritance - the basics.

Teaching focus
  - multiple inheritance
  - mro and mro fail
  - diamond problem
"""

# pylint: disable=missing-function-docstring, missing-class-docstring, multiple-statements, too-few-public-methods, unused-variable


def mro_class_names(cls: type[object]):                 # or typing.Type[object]
    return [item.__name__ for item in cls.__mro__]      # all classes in the MRO


def recap_single_inheritance():
    """ remember: C -> B -> A (-> object) """
    print("\nrecap_single_inheritance\n========================")

    class A:
        def __init__(self):
            print("A ", end='')
            super().__init__()

    class B(A):
        def __init__(self):
            print("B ", end='')
            super().__init__()

    class C(B):
        def __init__(self):
            print("C ", end='')
            super().__init__()              # same as 'super(C,self).__init__()'

    print(" 1| init order: ", end='')
    C()
    print()

    print(f" 2| A.mro={A.__mro__}\n"
          f"         ={mro_class_names(A)}\n"
          f"    B.mro={mro_class_names(B)}\n"
          f"    C.mro={mro_class_names(C)}")

    class D(C):
        def __init__(self):
            print("D (skip C) ", end='')    # this is _not_ best practice...
            super(B,self).__init__()        # look in mro, find 'Self' or here 'C', call next in mro

    print(" 3| init order: ", end='')
    D()
    print()
    print(f" 4| D.mro={mro_class_names(D)}\n")


def show_simple_multiple_inheritance():          # simplest form of multiple inheritance
    r"""
    B12 -> A1       B21 -> A2
         \ A2            \ A1
    """
    print("\nshow_simple_multiple_inheritance\n================================")

    class A1:
        def __init__(self): print("A1 ", end=''); super().__init__()

    class A2:
        def __init__(self): print("A2 ", end=''); super().__init__()

    class B12(A1, A2):
        def __init__(self): print("B12 ", end=''); super().__init__()

    class B21(A2, A1):
        def __init__(self): print("B21 ", end=''); super().__init__()

    print(f" 1| A1.mro={mro_class_names(A1)}\n"
          f"    A2.mro={mro_class_names(A2)}")

    print(" 2| init orders: ", end='')
    B12()
    print()
    print(" 3| init orders: ", end='')
    B21()
    print()
    # (1) children precede their parents
    # (2) the order of appearance in base classes is respected
    print(f" 4| B12.mro={mro_class_names(B12)}\n"
          f"    B21.mro={mro_class_names(B21)}")


def show_diamond_problem():
    r"""
    C12  -> B1 -> A      C21 -> B2 -> A
          \ B2 /              \ B1 /
    """
    print("\nshow_diamond_problem\n====================")

    class A:
        def __init__(self): print("A ", end=''); super().__init__()

    class B1(A):
        def __init__(self): print("B1 ", end=''); super().__init__()

    class B2(A):
        def __init__(self): print("B2 ", end=''); super().__init__()

    class C12(B1, B2):
        def __init__(self): print("C12 ", end=''); super().__init__()

    class C21(B2, B1):
        def __init__(self): print("C21 ", end=''); super().__init__()

    print(f" 1|  A.mro={mro_class_names(A)}\n"
          f"    B1.mro={mro_class_names(B1)}\n"
          f"    B2.mro={mro_class_names(B2)}")

    print(" 2| init orders: ", end='')
    C12()                                   # same as before, just with one more class
    print()
    print(" 3| init orders: ", end='')
    C21()
    print()
    # (1) children precede their parents
    # (2) the order of appearance in base classes is respected
    print(f" 4| C12.mro={mro_class_names(C12)}\n"
          f"    C21.mro={mro_class_names(C21)}")


def show_mro_c3_linearization():
    """ large mro example, see https://en.wikipedia.org/wiki/C3_linearization """
    print("\nshow_mro_c3_linearization\n=========================")

    class O:
        def __init__(self): print("O ", end=''); super().__init__()
    class A(O):
        def __init__(self): print("A ", end=''); super().__init__()
    class B(O):
        def __init__(self): print("B ", end=''); super().__init__()
    class C(O):
        def __init__(self): print("C ", end=''); super().__init__()
    class D(O):
        def __init__(self): print("D ", end=''); super().__init__()
    class E(O):
        def __init__(self): print("E ", end=''); super().__init__()

    class K1(C, A, B):
        def __init__(self): print("K1 ", end=''); super().__init__()
    class K3(A, D):  # cf. parents A and D in MRO
        def __init__(self): print("K3 ", end=''); super().__init__()
    class K2(B, D, E):
        def __init__(self): print("K2 ", end=''); super().__init__()

    class Z(K1, K3, K2):                    # pylint -> too-many-ancestors (>7)
        def __init__(self): print("Z ", end=''); super().__init__()

    print(" 1| init orders: ", end='')
    Z()
    print()

    # (1) children precede their parents
    # (2) the order of appearance in base classes is respected
    print(f" 2| Z.mro={mro_class_names(Z)}")


def show_mro_fail():
    """  MRO fail """
    print("\nshow_mro_fail\n=============")

    class A1: ...
    class A2: ...
    class K1(A1, A2): ...
    class K2(A2, A1): ...
    # class Z(K1, K2): ...

    # (1) children precede their parents
    # (2) the order of appearance in base classes is respected
    print(" 1| MRO cannot be realized")


if __name__ == "__main__":
    recap_single_inheritance()
    show_simple_multiple_inheritance()
    show_diamond_problem()
    show_mro_c3_linearization()
    show_mro_fail()


###############################################################################


"""
Summary

Topics
  - MRO, Method Resolution Order, Fail
  - diamond problem

MRO, Method Resolution Order
  - In multiple inheritance, we need an order in which elements of the 
    "base class(es)" are searched for, found, or called. This is the 
    Method Resolution Order, or MRO for short. It is determined by 
    a linearization algorithm and can be accessed via `__mro__`.
  - This algorithm is well described in the literature and will not be the 
    main topic here. We will just note two conditions that hold after 
    successful linearization:
      - children precede their parents (a class always appears in the MRO 
        before its parents), and
      - the order of appearance in __bases__ is respected, i.e. if there are 
        multiple parents, they keep the same order as the tuple of base classes.
  - Note that it is not guaranteed that the linearization was successful, 
    i.e. there are situations where the algorithms fail.
  - https://www.python.org/download/releases/2.3/mro/
  - https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
  - http://python-history.blogspot.com/2010/06/method-resolution-order.html
    
Diamond Problem
  - A constellation such as this is the real problem, namely having the same 
    base classes somewhere in the inheritance hierarchy. Because the inheritance 
    relationships look like a diamond, it is called the diamond problem.
    The question is what the MRO is going to do with it.
  - https://en.wikipedia.org/wiki/C3_linearization
"""
