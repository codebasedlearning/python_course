# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Hello World! A module docstring. """

import platform  # a line comment

print(f"Hello World! (python {platform.python_version()})")

"""
Here this is a block comment, with three " " " (without spaces) before and after.
Actually it is a string literal, not a comment in Python. However, whether it 
behaves like a (doc)comment depends on how it is used (examples follow).
"""


###############################################################################


""" 
Summary

Comments
  - Using triple-quoted strings outside of docstrings can confuse tools (like 
    linters or Pylint) and readers because they're typically associated with 
    docstrings.
  - Single-line comments with `#` are more efficient. Triple-quoted strings are 
    still treated as strings by the interpreter, which could have a small 
    performance impact in extreme scenarios.
  - When working with writing tools such as spell checkers or grammar 
    improvement software, the leading `#` in Python comments can hinder the 
    tool's ability to process the text correctly. In such scenarios, using 
    Python's multiline string literals as comments is a practical alternative 
    because they don't have the leading `#`. Because of this the warning is 
    disabled in Pylint (see .pylintrc).
  - More on comments in the next section.
  - https://docs.python.org/3/tutorial/introduction.html#comments
  - https://docs.python.org/3.13/reference/lexical_analysis.html#comments

'import'
  - The 'platform' module is loaded. 
  - A lot of functionality comes in libraries, i.e. modules. In Python this is 
    called 'batteries included'. We will see more snippets about 'import' later.
  - https://docs.python.org/3.13/reference/import.html

'print'
  - Output function with string literal and prefix 'f'. 
  - This allows for expressions to be enclosed in a {}. This type of formatting is 
    also known as 'string interpolation' (or 'variable interpolation', 
    'variable substitution' or 'variable expansion').
  - https://docs.python.org/3.13/library/functions.html#print
    
Execution
  - Code is executed from top to bottom.
  
See also
  - https://docs.python.org/3.13/
  - https://docs.python.org/3/tutorial/introduction.html#hello-world
"""
