# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet introduces some simple lambda functions.

Teaching focus
  - lambdas
"""


def show_lambdas():
    """ show lambdas """
    print("\nshow_lambdas\n============")

    f_plus = lambda x, y: x+y                                       # (A) lambda
    print(f" 1| {f_plus(2,3)=}")

    a = 2
    f_mul = lambda x, y: a*x*y                                      # 'x','y' are bound, i.e. args of the lambda expr.
    a = 3                                                           # 'a' is a free var., referenced in the lambda body
    print(f" 2| {a}*f_mal(4,5)={f_mul(4, 5)}")                      # 'a' evaluated at runtime, enclosing scope of f_mul
    a = 4
    print(f" 3| {a}*f_mal(4,5)={f_mul(4, 5)}")

    result = (lambda x, y, z=1: x+y+z)(2, 3)                        # main application: local simple anonymous functions
    print(f" 4| 2+3+1={result}")


def twice_x(x): return x+x


def eval_x(x, f): return f(x)


def show_funcs_are_first_class():
    """ show funcs are first class """
    print("\nshow_funcs_are_first_class\n==========================")

    print(f" 1| 2*5={twice_x(5)}")
    print(f" 2| f(5)={eval_x(5, twice_x)}")

    def tripple_x(x): return 3*x
    print(f" 3| 3*5={tripple_x(5)}")

    print(f" 4| 2,3->2+3={(lambda x, y: x+y)(2, 3)}")


if __name__ == "__main__":
    show_lambdas()
    show_funcs_are_first_class()

"""
lambda

You know lambdas. More can be found here:
    https://realpython.com/python-lambda/
    https://docs.python.org/3/reference/expressions.html?highlight=lambda
We come to this topic later on.
"""
