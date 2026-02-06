# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about scopes and the 'globals' and 'locals' dictionary.

Teaching focus
  - 'globals' and 'locals'

Instead of running 'main', we will look at this script from top to bottom,
explaining the terms one by one. We will summarize everything at the end.
You can run the script by selecting Run from the context menu in the project
tree (as there is no 'main guard' here).
"""

"""
globals() - A dictionary implementing the current (global) module namespace.
Here you can find all objects defined globally in the module, e.g. the 
doc string from above, the file name etc.
"""
G = globals()
print(f" 1| globals ({type(G)}): {G}\n"
      f"    e.g. '__name__': '{G['__name__']}', '__file__': '{G['__file__']}'\n")


def non_dunder_names(dct):
    """ returns 'non-dunder' names from dictionary. """
    return [name for name in dct if not name.startswith('__')]


def non_dunder_items(dct):
    """ returns 'non-dunder' items as (name,type)-tuple from the dictionary. """
    return [(name, type(value)) for name, value in dct.items() if not name.startswith('__')]


"""
globals again. Here is a list of all the objects that have been defined so far.
"""
print(f" 2| 'non-dunder' global items with types: {non_dunder_items(G)}\n"
      f"    only names: {non_dunder_names(G)}\n")

"""
Add 'x'. 'id(x)' provides some sort of an identifier for the object 'x'. 
Same 'id' means same object in memory. In CPython 'id' returns the 
memory location (i.e. a pointer to the object).
"""
x = 123
globals()['xyz'] = "HiHo"                   # change globals is (tech.) ok (IDE is surprised...)
print(f" 3| define x: {non_dunder_names(G)}\n"
      f"    {x=}, {xyz=}\n"
      f"    id(x)==id(globals[x])? {id(x) == id(G['x'])} or, eq., x is globals[x]? {x is G['x']}\n")

"""
What exactly is done by the import command? In the first case ('math') it adds 
a new object of type 'module' and in the second case ('pi') it adds a reference 
to the object 'pi'.
We now know a number of ways to add objects to globals: x=, import, def f
"""
import math
from math import pi
print(f" 4| import math, pi: {non_dunder_items(G)}\n")


"""
From https://realpython.com/python-scope-legb-rule/#using-scope-related-built-in-functions:
  - Global (or module) scope is the top-most scope in a Python program, 
    script, or module. This Python scope contains all of the names that 
    you define at the top level of a program or a module. Names in this 
    Python scope are visible from everywhere in your code.
  - Python scopes are implemented as dictionaries that map names to objects. 
    These dictionaries are commonly called 'namespaces'. These are the 
    concrete mechanisms that Python uses to store names. 
    They’re stored in a special attribute called .__dict__ in a module.
"""
import sys
print(f" 5| id(globals)={id(globals())}, id(module.dict)={id(sys.modules[__name__].__dict__)}\n")


"""
Now to the local scope.

Again from https://realpython.com/python-scope-legb-rule/#using-scope-related-built-in-functions:
  - Local (or function) scope is the code block or body of any Python function 
    or lambda expression. The names that you define in this scope are only 
    available or visible to the code within the scope.
"""


def access_x_v1():
    # locals() implements the local scope.
    print(f" 6| locals type:{type(locals())}, locals={locals()}")

    # remember, x is global; defining 'x2' adds 'x2' to the local scope, seen in locals()
    x2 = x

    def f(): return 1

    if False:
        a = 1

    print(f"    define x2 and f: locals={locals()}, x2={locals()['x2']}\n")

    # x = 1  # technically ok, but IDE signals a warning...


access_x_v1()


def access_x_v2():
    global x  # comment out this line to create an error -> why?
    x = x + 1
    for i in range(5):
        pass


# btw. functions know their variables, even if they have not come across
print(f" 7| local vars in 'access_x_v1': {access_x_v1.__code__.co_varnames}\n"
      f"    local vars in 'access_x_v2': {access_x_v2.__code__.co_varnames}\n")

# finally

print(f" 8|   globals={globals()}\n"                    # globals()
      f"      non_dunder={non_dunder_names(G)}\n"
      f"       locals={locals()}\n"                     # at module level, locals and globals same dict.
      f"       id(locals)={id(locals())}, id(globals)={id(globals())}\n"
      f"         vars={vars()}\n"                       # here vars = globals = locals
      f"    vars.keys={sorted(vars().keys())}\n"
      f"          dir={sorted(dir())}")                 # here vars.key() = dir()

"""
Closing remarks (almost) 

From https://realpython.com/python-scope-legb-rule/#using-scope-related-built-in-functions
  - Python resolves names using the so-called LEGB rule, which is named after 
    the Python scope for names. 
  - The letters in LEGB stand for Local, Enclosing, Global, and Built-in.
      - Local (or function) scope is the code block or body of any Python 
        function or lambda expression.
      - Enclosing (or nonlocal) scope is a special scope that only exists 
        for nested functions.
      - Global (or module) scope is the top-most scope in a Python program, 
        script, or module. This Python scope contains all of the names that 
        you define at the top level of a program or a module. Names in this 
        Python scope are visible from everywhere in your code.
      - Built-in scope is a special Python scope that’s created or loaded 
        whenever you run a script or open an interactive session. This scope 
        contains names such as keywords, functions, exceptions, and other 
        attributes that are built into Python.

  - You’ll find some Python structures where name resolution seems not to 
    fit into the LEGB rule for Python scopes. These structures include:
      - Comprehensions
      - Exception blocks
      - Classes and instances
    We now (in a minute) look at these different scopes.

---
dir() and vars():

From https://docs.python.org/3/library/functions.html

vars(object):
  - Return the __dict__ attribute for a module, class, instance, or any other 
    object with a __dict__ attribute.

dir(object)
  - Without arguments, return the list of names in the current local scope. 
    With an argument, attempt to return a list of valid attributes for that 
    object.
  - The default dir() mechanism behaves differently with different types 
    of objects, as it attempts to produce the most relevant, rather than 
    complete, information:
      - If the object is a module object, the list contains the names of 
        the module’s attributes.
      - If the object is a type or class object, the list contains the names 
        of its attributes, and recursively of the attributes of its bases.
      - Otherwise, the list contains the object’s attributes’ names, the 
        names of its class’s attributes, and recursively of the attributes 
        of its class’s base classes.
"""
