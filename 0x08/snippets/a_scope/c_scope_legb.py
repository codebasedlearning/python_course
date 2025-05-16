# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about scopes and the LEGB rule.

Teaching focus
  - import
  - LEGB
"""

# Recap: For the sake of clarity, let's look at the global namespace first,
# because there aren't that many elements at the moment.

x = 123


def non_dunder_names(dct):
    """ returns 'non-dunder' names from dictionary. """
    return [name for name in dct if not name.startswith('__')]


print(f" 1| globals={non_dunder_names(globals())}")     # globals() = dict. impl. current module namespace
globals()['xyz'] = "HiHo"                               # change globals is (tech.) ok (IDE is surprised...)
print(f" 2| def. xyz: xyz='{xyz}', globals={non_dunder_names(globals())}")


# application... to be discussed

def win32_print(): print(" a| printing from Windows...")
def darwin_print(): print(" b| printing from macOS...")
def linux_print(): print(" c| printing from Linux...")


import platform                                             # https://docs.python.org/3/library/platform.html
printer = globals()[platform.system().lower() + '_print']   # 'Linux', 'Darwin', 'Java', 'Windows'
printer()


# local

def show_local_scope():
    """ show local scope """
    print("\nshow_local_scope\n================")

    a = 1
    b = 2
    s = "hello"
    d = {1: 'one'}
    if True:
        e = 2.71                            # note, 'e' is known from here (compare with Java)
    from math import pi
    def f(): return 1
    print(f" 1|      locals={locals()}\n"
          f"    locals.keys={locals().keys()}\n"
          f"           vars={vars()}\n"
          f"            dir={dir()}")

    locals()['y'] = 1                       # changing locals is valid, but...
    # print(y)                              # (NameError: name 'y' is not defined)
    # ...the doc. says: note that the contents of this dictionary should not
    # be modified; changes may not affect the values of local and free variables
    # used by the interpreter.

# enclosing

def show_enclosing_scope():
    """ show local scope """
    print("\nshow_enclosing_scope\n====================")

    # 'local scope' of 'show_enclosing_scope' and 'enclosing scope' of 'f'
    y = 1

    def f():
        # 'local scope' of 'f'
        z = 2
        # accessing 'y' is interesting... comment in and out 'y=11'
        print(f" a| locals 'f': {locals()}, {y}")
        # y = 11  # shadows 'enclosing' y and 'y' becomes a local variable, existing from here
        print(f" b| def. y, locals 'f': {locals()}")
        # nonlocal y   # no explicit scope for 'nonlocal' vars -> appear in locals...
        # y = 13
        print(f" c| non.loc. y, locals 'f': {locals()}")
        # z local, y enclosing or local, x global -> LEG
        return y
    print(f" 1| f()={f()}, y={y} x={x}\n")


# closures

def doubled_power_factory(exp):             # closure fact., exp and scaling are free variables
    scaling = 2                             # "private", i.e. cannot be accessed from outside

    def power(base):
        return scaling * base ** exp        # a**b = 'a' to the power of 'b'
    return power                            # return a closure


def show_enclosing_application():
    """ show enclosing scope and application of a closure """
    print("\nshow_enclosing_application\n==========================")

    square = doubled_power_factory(2)
    cube = doubled_power_factory(3)
    print(f" 1| 2*5^2={square(5)}, 2*10^2={square(10)}\n"
          f"    2*5^3={cube(5)}, 2*10^3={cube(10)}\n")


def create_func_tuple():
    shared_state = 0

    def add_to_sum(who, _s):
        nonlocal shared_state
        shared_state += _s
        print(f" a| {who}, +={_s} => {shared_state}, {locals()=}, {id(locals())=}")

    # a form of currying
    return lambda _x: add_to_sum("f1", _x), lambda _x: add_to_sum("f2", _x + _x)


def show_enclosing_edge_case():
    """ show enclosing scope and application of a closure """
    print("\nshow_enclosing_edge_case\n========================")

    print(f" 1| create two closures with shared state")
    add_x, add_2x = create_func_tuple()
    add_x(1)
    add_2x(3)
    print()


# builtin

def show_builtin_scope():
    """ show builtin scope """
    print("\nshow_builtin_scope\n==================")

    print(f" 1| builtin: {non_dunder_names(__builtins__.__dict__)}\n")
    # change builtins ok
    __builtins__.__dict__['code_based'] = "CBL"         # similar to globals()
    print(f" 2| new def.: {code_based}")


def show_builtin_application():
    """ show builtin application """
    print("\nshow_builtin_application\n========================")

    import builtins as std                  # in case of name conflicts
    print(f" 1| {std.abs(-5)=}")


if __name__ == "__main__":
    show_local_scope()
    show_enclosing_scope()
    show_enclosing_application()
    show_enclosing_edge_case()
    show_builtin_scope()
    show_builtin_application()

"""

closures

From https://en.wikipedia.org/wiki/Closure_(computer_programming)
  - In programming languages, a closure, also lexical closure or function 
    closure, is a technique for implementing lexically scoped name binding 
    in a language with first-class functions. Operationally, a closure is 
    a record storing a function[a] together with an environment. 
  - The environment is a mapping associating each free variable of the function 
    (variables that are used locally, but defined in an enclosing scope) with 
    the value or reference to which the name was bound when the closure was 
    created. Unlike a plain function, a closure allows the function to access 
    those captured variables through the closure's copies of their values or 
    references, even when the function is invoked outside their scope.

See https://realpython.com/inner-functions-what-are-they-good-for/
"""
