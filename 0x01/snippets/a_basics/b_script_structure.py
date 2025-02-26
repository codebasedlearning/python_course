# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
At this location this literal is a docstring, describing the script or module.
"""

import platform                                                 # hold mouse on 'platform'... (PyCharm)


# a typical function

def scale_if_positive(n):
    """ Scales n if positive, otherwise returns 0 """           # docstring, hold mouse on 'scale_if_positive'

    result = 0                                                  # spaces/indent and a local variable
    # result: int = 0                                           # type hints (not today)
    if n > 0:                                                   # code blocks, ':', indention level is crucial
        case = 1                                                # scope of 'case'?
        result = n*3
    else:
        case = 2
    print(f" 2| {n=}, {result=} | {case=}")                     # ' n=' self-documenting expression
    return \
        result                                                  # joined into logical line using backslash


# then do the main work in a 'main' function and call it

def my_main():                                                  # definition of a function
    """ Greets and prints some scaling examples """
    print("\nmy_main\n=======")

    print(f" 1| Hello World! (python {platform.python_version()})")

    n1 = scale_if_positive(10)                                  # local vars
    n2 = scale_if_positive(-1)
    print(f" 3| {n1=}, {n2=}")


if __name__ == "__main__":                                      # main guard, 'Pythonic way'
    my_main()                                                   # hold mouse on 'my_main'


"""
Summary

Doc-Strings
  - Many rules about formatting and naming can be found in 
    https://peps.python.org/pep-0008 'PEP 8 - Style Guide for Python Code'
    https://peps.python.org/pep-0257 'PEP 257 - Docstring Conventions'
  - The module description at the beginning may be presented in a slightly 
    different style to other block comments. 
    This description would be displayed in a tooltip in an IDE where you 
    import the script, i.e. on the 'import' command. You can try this for 
    example with the description of 'platform'. 
  - The function description follows the signature and is also shown in the 
    tooltip when called, i.e. 'main()'.

Indentation level
  - Python uses indentation instead of curly braces or begin/end blocks 
    to define blocks of code (after the ':'). This means that whitespace 
    is not ignored as usual, but is clearly part of the structure.
  - All commands at an indentation level (and lower if necessary) belong 
    to the code block, see 'if', for instance. 
  - https://docs.python.org/3.13/reference/lexical_analysis.html

Local variables
  - A local variable like 'result' is valid for the whole function, i.e. 
    'scale_if_positive'. And surprisingly, 'case' is also well defined until 
    the end of the function.
  - There are quite a few rules about the scope of a variable. We will look 
    at this in an upcoming lecture.

Self-documenting expression
  - Introduced in Python 3.8. "{x=}" prints "x=<value>" and "{f(1,2)=}" 
    prints "f(1,2)=<value>". 
  - We also number the outputs, e.g. " 1|..." and so on, in order to 
    associate the output with the calling line.

'main'
  - It should be noted that, unlike other languages, there is no explicit 'main' 
    as the starting point of execution. Code is executed from top to bottom, 
    and 'def my_main' this is just a definition (not the execution) of a function. 

'Pythonic way'
  - Defining the main functionality of the program in its own functions, which 
    are then called, is one example of best practice, as they say here, the 
    so-called 'Pythonic way'. This means, among other things: Do something right 
    from a Python point of view.
  - Variable shadowing is another reason. We will be looking at this in some of 
    the lectures to come.

'main guard'
  - If you want to write Python code that can be imported but also run as a standalone script, 
    this 'if' is important. The code protected by the if clause only runs when executed as 
    a script, because '__name__' is only then set to the value "__main__", see e.g.
    https://docs.python.org/3/reference/toplevel_components.html#complete-python-programs
    https://docs.python.org/3/reference/import.html?highlight=__name__#__name__
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    Otherwise  '__name__' is set to the name of the module.
  - This guard is more or less standard.
  - Doing more than calling the function, especially defining variables, can 
    lead to to shadow variables and warnings (discussed later).

Best practices
  - doc your code (short and concise)
  - define something like a 'main'-function
  - use a 'main guard'
  - use 'string interpolation' instead of concatenation
  - get a feeling for the 'Pythonic way'

Code Style (from Style Guide for Python Code, PEP 8)
  - spaces (no tabs) are the preferred indentation method
  - function names should be lowercase, with words separated 
    by underscores as necessary to improve readability
  - variable names follow the same convention as function names
  - no standard file header, use VCS instead (see discussion below)
  - use type hints if needed (later)
  - define something like 'main', avoid variable shadowing

File Header
  - This discussion always comes up when it comes to a 'common standard header'
    format of a Python script. Quoted from Jonathan Hartley, stackoverflow, 
    could not put it any better:
        I think all of this metadata after the imports is a bad idea. 
        The parts of this metadata that apply to a single file (e.g. author, 
        date) are already tracked by source control. Putting an erroneous & out 
        of date copy of the same info in the file itself seems wrong to me. 
        The parts that apply to the whole project (eg licence, versioning) 
        seem better located at a project level, in a file of their own, rather 
        than in every source code file.
  - That's why you don't find this information in the snippets.
"""
